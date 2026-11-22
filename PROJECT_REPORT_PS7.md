# ACADEMIC PROCEDURE & LAB REPORT

**Course:** B.Tech Computer Science & Engineering (Final Year)  
**Course Code / Evaluation:** CSE499 / Generative AI Mini Project (10 Marks)  
**Problem Statement ID:** PS7  
**Project Title:** Research Paper Abstract Simplifier  
**Submission Date:** November 2026  

---

## 1. ABSTRACT & INTRODUCTION

Research publications in artificial intelligence, biomedical sciences, and environmental engineering are the primary medium for communicating scientific breakthroughs. However, research abstracts are dense, highly specialized, and syntax-heavy. First-year undergraduate engineering students frequently encounter severe cognitive friction when trying to comprehend academic papers due to unfamiliar terminology, compound mathematical formulations, and domain jargon.

To solve this challenge, this project implements the **Research Paper Abstract Simplifier (PS7)**, an end-to-end Generative AI academic application. Utilizing Google Gemini API via the official `google-genai` Python SDK and a Streamlit web interface, the system parses authentic abstracts, generates plain-English simplifications grounded in the source text, extracts 5 to 10 difficult technical terms with beginner-friendly definitions, and summarizes key takeaways.

---

## 2. PROBLEM STATEMENT & OBJECTIVES

### Problem Statement (PS7)
> *"Research paper abstracts contain difficult technical terms, complex sentences, and academic jargon that are hard for first-year students to understand."*

### Key Objectives
1. **Plain-English Transformation:** Synthesize research abstracts into clear, intuitive language accessible to a first-year college student.
2. **Fact Preservation & Hallucination Elimination:** Ground the generative model to maintain all experimental findings without introducing unverified or fabricated facts.
3. **Automated Lexicon Extraction:** Dynamically extract 5–10 domain-specific terms from the input abstract and explain them in everyday analogies.
4. **Distillation of Key Takeaways:** Extract 3–5 bullet points representing research goals, methods, and outcomes.
5. **Academic UI/UX & Multi-Format Reporting:** Design a modern dual-card comparison interface with word-count analytics and one-click export to TXT and PDF.

---

## 3. SYSTEM ARCHITECTURE & METHODOLOGY

```
+-------------------------------------------------------------+
|                     User Interaction Layer                  |
|    - Research Abstract Text Area                            |
|    - Domain Sample Abstract Loaders (AI, Health, Climate)   |
|    - Real-Time Word & Character Counter                     |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                   Input Validation Engine                   |
|    - Non-empty validation & minimum length threshold (>=15w)|
|    - Exception handling: InvalidInputError                  |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  Gemini Prompt Engineering                  |
|    - Zero-Shot In-Context Grounding Instructions            |
|    - Temperature: 0.2 (Low variance for factual accuracy)   |
|    - Pydantic Schema (SimplificationResult)                 |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|             Google Gemini API (google-genai SDK)            |
|    - Model: gemini-2.5-flash / gemini-1.5-flash             |
|    - Native response_schema & application/json MIME         |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 Structured Output Parsing                   |
|    - Markdown code-fence stripping                          |
|    - Pydantic validation (DifficultTerm, KeyTakeaways)      |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                Presentation & Export Pipeline               |
|    - Side-by-Side Original vs. Simplified Comparison Cards  |
|    - Difficult Terms Interactive Data Table                 |
|    - Key Research Takeaways Highlights                      |
|    - Multi-format Export (TXT & fpdf2 PDF Report)           |
+-------------------------------------------------------------+
```

### Algorithmic Procedure

1. **Step 1 (Ingestion):** User inputs an academic abstract manually or clicks one of the three preloaded sample buttons (*Artificial Intelligence*, *Healthcare & Biotechnology*, *Environmental Science*).
2. **Step 2 (Sanitization & Guardrails):** The input text is trimmed of irregular whitespace. The system verifies that the text contains at least 15 words and 40 characters.
3. **Step 3 (Prompt Compilation):** The text is injected into the prompt template specifying constraints: zero-hallucination policy, targeted grade-level vocabulary, and mandatory JSON schema.
4. **Step 4 (Inference Execution):** `ai_service.py` invokes `client.models.generate_content` via the official `google-genai` SDK using `gemini-2.5-flash`.
5. **Step 5 (Validation):** The returned JSON is validated through Pydantic's `SimplificationResult` model, ensuring types and counts match.
6. **Step 6 (Rendering & Reporting):** The Streamlit engine displays dual comparison cards with word-count reduction percentages, formats extracted terms into a table, and compiles exportable TXT and PDF documents via `export_service.py`.

---

## 4. EXPERIMENTAL VERIFICATION & TEST CASES

The system was evaluated against 8 automated test cases covering diverse scientific disciplines:

| Test ID | Abstract Domain | Input Size | Difficult Terms Extracted | Takeaways | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **TC-01** | Computer Vision (MobileNet) | 48 words | 5 terms (*CNN, Separable Convolutions, Latency, Parameter Count, Accuracy*) | 3 points | **PASSED** |
| **TC-02** | Deep Learning (ResNet) | 134 words | 6 terms (*Residual learning, Degradation, Vanishing gradient, Identity shortcut, ImageNet, Classification*) | 3 points | **PASSED** |
| **TC-03** | Biotechnology (CRISPR-Cas9) | 126 words | 7 terms (*CRISPR-Cas9, Endonuclease, sgRNA, T-lymphocytes, PD-1, Indel, Off-target*) | 3 points | **PASSED** |
| **TC-04** | Marine Ecology (Ocean Acidification) | 119 words | 6 terms (*Anthropogenic emissions, Acidification, Aragonite, Calcification, Mesocosm, Trophic cascades*) | 3 points | **PASSED** |
| **TC-05** | Empty / Short Input Handling | 0–3 words | Correctly raised `InvalidInputError` with actionable user guidance | N/A | **PASSED** |
| **TC-06** | Missing API Key Handling | N/A | Correctly raised `MissingApiKeyError` with sidebar instructions | N/A | **PASSED** |
| **TC-07** | Markdown Fence JSON Parsing | N/A | Stripped ```json fences and validated schema without exceptions | N/A | **PASSED** |
| **TC-08** | TXT & PDF Document Export | N/A | Validated sections and generated compliant `%PDF` binary output | N/A | **PASSED** |

---

## 5. ACADEMIC VIVA QUESTIONS & ANSWERS

**Q1: How does your application ensure that scientific facts are preserved during simplification?**  
*Answer:* We constrain the LLM using a low temperature (`0.2`) to minimize stochastic drift, combine explicit zero-shot system instructions prohibiting unverified claims, and structure the output via Pydantic to ensure factual correspondence.

**Q2: What is the advantage of the official `google-genai` SDK over deprecated libraries?**  
*Answer:* The new `google-genai` SDK is Google's official unified standard. It supports Gemini 2.x models natively, handles typed `GenerateContentConfig`, and supports direct `response_schema` bindings with Pydantic.

**Q3: Why is JSON schema enforcement critical in this project?**  
*Answer:* Unstructured text outputs frequently combine definitions and text unpredictably. Strict schema enforcement guarantees programmatic extraction of `simplified_abstract`, `difficult_terms`, and `key_takeaways` for independent UI rendering and PDF generation.

---

## 6. CONCLUSION

The **Research Paper Abstract Simplifier (PS7)** demonstrates a practical and effective application of Generative AI in education. By bridging the linguistic gap between cutting-edge scientific literature and undergraduate students, the application accelerates literature reviews, demystifies complex jargon, and provides accessible multi-format learning aids. All functional and architectural requirements have been implemented and verified with automated test suites.
