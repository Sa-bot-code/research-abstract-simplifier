"""Test suite for Research Paper Abstract Simplifier (PS7).

Covers required test cases:
1. Short AI research abstract
2. Complex machine learning research abstract
3. Healthcare research abstract
4. Environmental science abstract
5. Empty input and invalid input handling
6. Schema validation, JSON parsing, and report generation
"""

import json
import os
import pytest
from unittest.mock import MagicMock, patch

from ai_service import (
    DifficultTerm,
    InvalidInputError,
    MissingApiKeyError,
    SimplificationResult,
    SimplificationServiceError,
    build_simplification_prompt,
    clean_json_response,
    get_configured_api_key,
    parse_and_validate_response,
    simplify_abstract,
)
from export_service import generate_pdf_report, generate_txt_report
from sample_abstracts import SAMPLE_ABSTRACTS


# -----------------------------------------------------------------------------
# Fixtures and Sample Data for 5 Test Cases
# -----------------------------------------------------------------------------

SHORT_AI_ABSTRACT = (
    "Convolutional neural networks have achieved remarkable success in visual recognition. "
    "However, their high computational cost restricts deployment on mobile devices. "
    "We propose MobileNet, an efficient architecture based on depthwise separable convolutions "
    "that significantly reduces parameter count and latency while maintaining competitive accuracy."
)

COMPLEX_ML_ABSTRACT = SAMPLE_ABSTRACTS["Artificial Intelligence"]["abstract"]
HEALTHCARE_ABSTRACT = SAMPLE_ABSTRACTS["Healthcare & Biotechnology"]["abstract"]
ENVIRONMENTAL_ABSTRACT = SAMPLE_ABSTRACTS["Environmental Science"]["abstract"]


def make_sample_response_json(
    simplified_text: str,
    terms: list[tuple[str, str]],
    takeaways: list[str],
) -> str:
    """Helper to create valid JSON for mock responses."""
    payload = {
        "simplified_abstract": simplified_text,
        "difficult_terms": [{"term": t[0], "meaning": t[1]} for t in terms],
        "key_takeaways": takeaways,
    }
    return json.dumps(payload)


# -----------------------------------------------------------------------------
# Test Case 1: Short AI Research Abstract
# -----------------------------------------------------------------------------
def test_case_1_short_ai_abstract():
    """Verify processing and response structure for a short AI abstract."""
    assert len(SHORT_AI_ABSTRACT.split()) >= 15
    prompt = build_simplification_prompt(SHORT_AI_ABSTRACT)
    assert "MobileNet" in prompt
    assert "depthwise separable convolutions" in prompt

    simulated_json = make_sample_response_json(
        simplified_text=(
            "Traditional computer vision models require huge computer power, making them slow on phones. "
            "This study introduces MobileNet, a lightweight AI model that uses a smart technique called "
            "depthwise separable convolutions. This makes the model much smaller and faster without losing "
            "much image recognition accuracy."
        ),
        terms=[
            ("Convolutional neural networks", "AI algorithms designed to recognize images"),
            ("Depthwise separable convolutions", "A math technique that speeds up AI calculations"),
            ("Latency", "The time delay before a system responds"),
            ("Parameter count", "The number of adjustable variables inside an AI model"),
            ("Accuracy", "How often the AI makes correct predictions"),
        ],
        takeaways=[
            "Standard image recognition AI models are too bulky for mobile phones.",
            "MobileNet solves this by splitting math operations into smaller, faster steps.",
            "The model achieves fast performance with minimal drop in prediction quality.",
        ],
    )

    result = parse_and_validate_response(simulated_json)
    assert isinstance(result, SimplificationResult)
    assert "MobileNet" in result.simplified_abstract
    assert len(result.difficult_terms) >= 5
    assert len(result.key_takeaways) >= 3

    # Check terms structure
    for item in result.difficult_terms:
        assert item.term
        assert item.meaning


# -----------------------------------------------------------------------------
# Test Case 2: Complex Machine Learning Research Abstract
# -----------------------------------------------------------------------------
def test_case_2_complex_ml_abstract():
    """Verify processing for deep residual learning (ResNet) abstract."""
    assert "residual learning" in COMPLEX_ML_ABSTRACT.lower()
    assert "degradation problem" in COMPLEX_ML_ABSTRACT.lower()

    simulated_json = make_sample_response_json(
        simplified_text=(
            "As neural networks get deeper with more layers, they become much harder to train because signals "
            "fade away. The researchers created 'residual networks' (ResNets) that use shortcut connections, "
            "allowing information to skip layers directly. This breakthrough allowed training networks up to "
            "152 layers deep, drastically reducing image recognition errors and winning first place in the "
            "ILSVRC competition."
        ),
        terms=[
            ("Residual learning", "A technique where networks learn differences instead of full mappings"),
            ("Degradation problem", "Accuracy drops as a network gets deeper even though it should perform better"),
            ("Vanishing gradient", "A problem where learning signals become too small in deep layers"),
            ("Identity shortcut connections", "Direct bypass pathways that let information skip layers"),
            ("ImageNet", "A huge benchmark database of labeled images used to test AI models"),
            ("Classification task", "Assigning an image to its correct category"),
        ],
        takeaways=[
            "Very deep neural networks traditionally struggle with training degradation.",
            "Shortcut connections allow deep networks to train easily by skipping layers.",
            "ResNet achieved a record low error rate of 3.57% on ImageNet.",
        ],
    )

    result = parse_and_validate_response(simulated_json)
    assert len(result.difficult_terms) == 6
    assert len(result.key_takeaways) == 3
    assert any("shortcut" in t.meaning.lower() or "bypass" in t.meaning.lower() for t in result.difficult_terms)


# -----------------------------------------------------------------------------
# Test Case 3: Healthcare Research Abstract
# -----------------------------------------------------------------------------
def test_case_3_healthcare_abstract():
    """Verify processing for CRISPR-Cas9 oncology research abstract."""
    assert "CRISPR" in HEALTHCARE_ABSTRACT
    assert "endonuclease" in HEALTHCARE_ABSTRACT

    simulated_json = make_sample_response_json(
        simplified_text=(
            "CRISPR-Cas9 is a molecular tool that works like scissors to cut and edit DNA inside cells. "
            "In this medical study, researchers modified immune cells (T-cells) from cancer patients to "
            "turn off the PD-1 gene, which tumors normally use to hide from the immune system. The modified "
            "immune cells lasted longer in the body, attacked tumors better, and caused minimal side effects."
        ),
        terms=[
            ("CRISPR-Cas9", "A gene editing tool that can cut DNA at exact locations"),
            ("Endonuclease", "An enzyme protein that cuts DNA chains like scissors"),
            ("Single-guide RNA (sgRNA)", "A short genetic guide that directs Cas9 to the target DNA spot"),
            ("T-lymphocytes", "White blood cells that fight diseases and infections"),
            ("PD-1 locus", "A specific gene that cancer cells exploit to shut down immune attacks"),
            ("Indel frequency", "The rate of successful insertions or deletions created in the DNA"),
            ("Off-target cleavage", "Unintended cuts made at the wrong DNA locations"),
        ],
        takeaways=[
            "CRISPR-Cas9 was safely used to edit the immune cells of cancer patients.",
            "The edits successfully targeted the PD-1 gene with 78.4% efficiency and rare off-target cuts.",
            "The modified cells showed strong anti-tumor activity without harmful immune reactions.",
        ],
    )

    result = parse_and_validate_response(simulated_json)
    assert "CRISPR-Cas9" in result.simplified_abstract
    assert len(result.difficult_terms) == 7
    assert len(result.key_takeaways) == 3


# -----------------------------------------------------------------------------
# Test Case 4: Environmental Science Abstract
# -----------------------------------------------------------------------------
def test_case_4_environmental_science_abstract():
    """Verify processing for Ocean Acidification ecology abstract."""
    assert "ocean acidification" in ENVIRONMENTAL_ABSTRACT.lower()

    simulated_json = make_sample_response_json(
        simplified_text=(
            "Human activities release massive amounts of carbon dioxide, which dissolves into the oceans "
            "and makes the water more acidic. This study tested marine organisms like corals under water "
            "conditions predicted for the year 2100. The acidic water caused a 34% drop in coral skeleton "
            "building and dissolved existing shells, demonstrating that marine food chains could suffer "
            "permanent damage if carbon emissions continue."
        ),
        terms=[
            ("Anthropogenic emissions", "Pollution and greenhouse gases caused by human activities"),
            ("Ocean acidification", "The ongoing decrease in the pH of Earth's oceans caused by CO2 uptake"),
            ("Aragonite saturation", "A measure of how easily marine creatures can build calcium carbonate shells"),
            ("Calcification rates", "The speed at which corals and shellfish construct their hard skeletons"),
            ("Mesocosm experiments", "Outdoor experimental systems that simulate natural environmental conditions"),
            ("Trophic cascades", "Chain-reaction disruptions spreading through an entire food web"),
        ],
        takeaways=[
            "Burning fossil fuels is making ocean waters significantly more acidic.",
            "Acidic water reduced coral growth by 34.2% and dissolved existing shells.",
            "Crossing these environmental thresholds threatens global marine ecosystems and fisheries.",
        ],
    )

    result = parse_and_validate_response(simulated_json)
    assert "ocean" in result.simplified_abstract.lower()
    assert len(result.difficult_terms) >= 5
    assert len(result.key_takeaways) >= 3


# -----------------------------------------------------------------------------
# Test Case 5: Empty Input and Invalid Input Handling
# -----------------------------------------------------------------------------
def test_case_5_empty_and_invalid_inputs():
    """Verify appropriate validation errors are raised for invalid inputs."""
    # Empty string
    with pytest.raises(InvalidInputError) as exc_empty:
        simplify_abstract("")
    assert "enter or load" in str(exc_empty.value).lower()

    # Whitespace only
    with pytest.raises(InvalidInputError) as exc_ws:
        simplify_abstract("     \n\t   ")
    assert "enter or load" in str(exc_ws.value).lower()

    # Too short text (< 10 words or < 40 chars)
    with pytest.raises(InvalidInputError) as exc_short:
        simplify_abstract("This is too short.")
    assert "too short" in str(exc_short.value).lower()


# -----------------------------------------------------------------------------
# Test Case 6: Missing API Key Handling
# -----------------------------------------------------------------------------
def test_missing_api_key_handling():
    """Verify MissingApiKeyError is raised when no API key is provided."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
        with pytest.raises(MissingApiKeyError):
            get_configured_api_key(None)

    with patch.dict(os.environ, {"GEMINI_API_KEY": "your_gemini_api_key_here"}):
        with pytest.raises(MissingApiKeyError):
            get_configured_api_key(None)


# -----------------------------------------------------------------------------
# Test Case 7: Clean JSON and Markdown Code Fences Parser
# -----------------------------------------------------------------------------
def test_json_fence_cleaner():
    """Verify markdown code fences and whitespace are stripped properly."""
    raw_markdown = "```json\n{\"simplified_abstract\": \"Simple\", \"difficult_terms\": [], \"key_takeaways\": []}\n```"
    cleaned = clean_json_response(raw_markdown)
    assert cleaned.startswith("{") and cleaned.endswith("}")

    # Malformed text raises SimplificationServiceError
    with pytest.raises(SimplificationServiceError):
        parse_and_validate_response("Not valid JSON at all")


# -----------------------------------------------------------------------------
# Test Case 8: Report Generation (TXT and PDF)
# -----------------------------------------------------------------------------
def test_report_generation_txt_and_pdf():
    """Verify both TXT and PDF reports are generated with complete sections."""
    sample_result = SimplificationResult(
        simplified_abstract="This is a simple explanation of the study.",
        difficult_terms=[
            DifficultTerm(term="Neural Network", meaning="A computer system that learns from data"),
            DifficultTerm(term="Gradient Descent", meaning="An optimization algorithm for finding minimum error"),
            DifficultTerm(term="Epoch", meaning="One complete pass through the training dataset"),
            DifficultTerm(term="Hyperparameter", meaning="A parameter set prior to training"),
            DifficultTerm(term="Overfitting", meaning="When a model memorizes rather than generalizes"),
        ],
        key_takeaways=[
            "Deep learning requires significant optimization.",
            "Gradient descent iteratively reduces prediction errors.",
            "Generalization is essential for production deployment.",
        ],
    )

    # 1. Test TXT generation
    txt_output = generate_txt_report(
        original_abstract=SHORT_AI_ABSTRACT,
        result=sample_result,
        model_name="gemini-2.5-flash",
    )
    assert "1. ORIGINAL ABSTRACT" in txt_output
    assert "2. SIMPLIFIED ABSTRACT" in txt_output
    assert "3. KEY TAKEAWAYS" in txt_output
    assert "4. DIFFICULT TECHNICAL TERMS & MEANINGS" in txt_output
    assert "Neural Network" in txt_output

    # 2. Test PDF generation
    pdf_bytes = generate_pdf_report(
        original_abstract=SHORT_AI_ABSTRACT,
        result=sample_result,
        model_name="gemini-2.5-flash",
    )
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")
