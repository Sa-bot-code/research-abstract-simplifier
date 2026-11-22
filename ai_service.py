"""AI Service Module for Research Paper Abstract Simplifier.

Handles integration with Google Gemini API using the official `google-genai` SDK,
prompt construction, structured JSON validation, and error management with automatic
model fallback when encountering 503 demand spikes.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

# Load environment variables from .env file
load_dotenv()

# Reliable default model (gemini-3.1-flash-lite has optimal availability and speed)
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# Candidate fallback models in priority order
FALLBACK_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
]

logger = logging.getLogger(__name__)


class DifficultTerm(BaseModel):
    """Schema for technical term and beginner-friendly explanation."""

    term: str = Field(
        ...,
        description="The technical term or academic jargon found directly in the abstract",
    )
    meaning: str = Field(
        ...,
        description="A simple, concise explanation of the term in everyday language",
    )


class SimplificationResult(BaseModel):
    """Structured output schema returned by the Gemini API."""

    simplified_abstract: str = Field(
        ...,
        description="The simplified abstract rewritten in plain, beginner-friendly English",
    )
    difficult_terms: List[DifficultTerm] = Field(
        ...,
        description="5 to 10 difficult technical terms extracted from the abstract and their meanings",
    )
    key_takeaways: List[str] = Field(
        ...,
        description="3 to 5 key takeaways highlighting research objective, methods, and findings",
    )


class SimplificationServiceError(Exception):
    """Base exception for simplification service."""


class MissingApiKeyError(SimplificationServiceError):
    """Raised when the Gemini API key is not provided."""


class InvalidApiKeyError(SimplificationServiceError):
    """Raised when the provided Gemini API key is invalid."""


class NetworkConnectivityError(SimplificationServiceError):
    """Raised when unable to reach the Gemini API service."""


class RateLimitError(SimplificationServiceError):
    """Raised when the Gemini API rate limit or quota is exhausted."""


class InvalidInputError(SimplificationServiceError):
    """Raised when input abstract is empty or insufficient."""


def get_configured_api_key(api_key: Optional[str] = None) -> str:
    """Retrieve the API key from parameter, environment, or raise MissingApiKeyError."""
    key = api_key or os.getenv("GEMINI_API_KEY", "")
    key = key.strip()
    if not key or key == "your_gemini_api_key_here":
        raise MissingApiKeyError(
            "Gemini API key is missing. Please provide your API key in the sidebar "
            "or set GEMINI_API_KEY in your .env file."
        )
    return key


def build_simplification_prompt(abstract_text: str) -> str:
    """Construct the academic simplification prompt according to project specifications."""
    return f"""You are an expert academic research assistant who specializes in explaining complex scientific research to first-year college students.

Your task is to simplify the research abstract provided by the user.

Instructions:

1. Rewrite the abstract using simple, clear, beginner-friendly English.
2. Preserve the original research meaning and important findings.
3. Avoid complex technical language wherever possible.
4. Explain difficult concepts in everyday words.
5. Identify 5–10 important technical terms actually present in the abstract.
6. Provide a short and simple meaning for each term.
7. Generate 3–5 key takeaways from the abstract.
8. Do not introduce information that is not present in the original abstract.
9. If the abstract does not contain results, do not invent them.
10. Return the output in valid structured JSON.

Research Abstract:
{abstract_text.strip()}"""


def clean_json_response(raw_text: str) -> str:
    """Clean markdown code fences (```json ... ```) and extract raw JSON."""
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def parse_and_validate_response(response_data: Any) -> SimplificationResult:
    """Validate JSON or dict response against SimplificationResult schema."""
    if isinstance(response_data, str):
        cleaned = clean_json_response(response_data)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as err:
            raise SimplificationServiceError(
                f"Failed to parse JSON response from Gemini: {err}"
            ) from err
    elif isinstance(response_data, dict):
        data = response_data
    else:
        raise SimplificationServiceError(
            f"Unexpected response type: {type(response_data).__name__}"
        )

    try:
        return SimplificationResult.model_validate(data)
    except ValidationError as err:
        raise SimplificationServiceError(
            f"Response failed schema validation: {err}"
        ) from err


def simplify_abstract(
    abstract_text: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.2,
) -> SimplificationResult:
    """Send research abstract to Gemini API with automatic model fallback for 503 demand spikes.

    Args:
        abstract_text: Raw abstract text entered by user.
        api_key: Optional Gemini API key. Defaults to GEMINI_API_KEY env var.
        model_name: Gemini model name.
        temperature: Sampling temperature (default: 0.2 for high fidelity).

    Returns:
        SimplificationResult containing simplified_abstract, difficult_terms, and key_takeaways.
    """
    # 1. Input validation
    if not abstract_text or not abstract_text.strip():
        raise InvalidInputError("Please enter or load a research paper abstract.")

    cleaned_text = abstract_text.strip()
    words = cleaned_text.split()
    if len(words) < 10 or len(cleaned_text) < 40:
        raise InvalidInputError(
            f"The provided text is too short ({len(words)} words). "
            "Please paste a complete research paper abstract (at least 15-20 words) for meaningful simplification."
        )

    # 2. Key resolution
    active_key = get_configured_api_key(api_key)
    preferred_model = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

    # Prepare ordered model attempts: preferred model first, followed by remaining fallbacks
    models_to_try = [preferred_model]
    for fb in FALLBACK_MODELS:
        if fb not in models_to_try:
            models_to_try.append(fb)

    # 3. Import and initialize google-genai client
    try:
        from google import genai
        from google.genai import types
        from google.genai.errors import APIError
    except ImportError as err:
        raise SimplificationServiceError(
            "The 'google-genai' SDK is not installed. Please run `pip install google-genai`."
        ) from err

    client = genai.Client(api_key=active_key)
    prompt = build_simplification_prompt(cleaned_text)

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=SimplificationResult,
        temperature=temperature,
        system_instruction=(
            "You are an expert academic research assistant who excels at simplifying complex "
            "scientific and technical research for first-year undergraduate students."
        ),
    )

    last_error = None

    # 4. Attempt generation across fallback models if demand spike (503) occurs
    for current_model in models_to_try:
        try:
            response = client.models.generate_content(
                model=current_model,
                contents=prompt,
                config=config,
            )

            if response and response.text:
                return parse_and_validate_response(response.text)

        except APIError as api_err:
            err_msg = str(api_err).lower()
            if "api_key" in err_msg or "unauthenticated" in err_msg:
                raise InvalidApiKeyError(
                    "Invalid Gemini API Key. Please verify the key in your .env or sidebar."
                ) from api_err

            # If 503 (demand spike) or 404/not available, try next fallback model
            if "503" in err_msg or "demand" in err_msg or "unavailable" in err_msg or "404" in err_msg:
                last_error = api_err
                time.sleep(0.5)
                continue

            if "quota" in err_msg or "resource_exhausted" in err_msg or "429" in err_msg:
                raise RateLimitError(
                    "Gemini API rate limit or quota exceeded. Please wait a moment before retrying."
                ) from api_err

            raise SimplificationServiceError(
                f"Gemini API Error ({api_err.code or 'unknown'}): {api_err.message}"
            ) from api_err

        except Exception as ex:
            ex_str = str(ex).lower()
            if "nameresolutionerror" in ex_str or "connection" in ex_str:
                raise NetworkConnectivityError(
                    "Network error: Could not reach Google Gemini API servers. Please check your internet connection."
                ) from ex
            raise SimplificationServiceError(f"Unexpected error communicating with Gemini API: {ex}") from ex

    # If all models failed with 503
    raise SimplificationServiceError(
        f"All Gemini models are temporarily experiencing high server demand. Error: {last_error}. "
        "Please wait a minute or select 'gemini-3.1-flash-lite' in the sidebar."
    )
