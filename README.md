# Research Paper Abstract Simplifier (PS7)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash-8E75C4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Academic%20Project-PS7%20Submission-10B981?style=for-the-badge)](#)

> **Final-Year BTech Computer Science & Engineering (CSE) Mini Project**  
> **Problem Statement Code:** `PS7`  
> **Topic:** Generative AI for Academic Document Comprehension

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement (PS7) & Objectives](#2-problem-statement-ps7--objectives)
3. [Key Features](#3-key-features)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture & Workflow](#5-system-architecture--workflow)
6. [Project Folder Structure](#6-project-folder-structure)
7. [Installation & Setup](#7-installation--setup)
8. [Obtaining and Configuring Google Gemini API Key](#8-obtaining-and-configuring-google-gemini-api-key)
9. [Running the Application](#9-running-the-application)
10. [Sample Inputs and Expected Outputs](#10-sample-inputs-and-expected-outputs)
11. [Testing Suite & Test Cases](#11-testing-suite--test-cases)
12. [Academic Viva & Evaluation Guide](#12-academic-viva--evaluation-guide)
13. [Future Enhancements](#13-future-enhancements)

---

## 1. Project Overview

Research papers are primary sources for scientific discoveries; however, their abstracts are dense, heavily laden with domain-specific jargon, and structured with convoluted sentence patterns. For first-year undergraduate students, novice researchers, and interdisciplinary scholars, deciphering these abstracts presents a significant cognitive barrier.

**Research Paper Abstract Simplifier** is an end-to-end Generative AI application powered by Google Gemini (using the official `google-genai` SDK) and an interactive Streamlit frontend. It translates complex academic abstracts into plain, accessible, beginner-friendly English while strictly maintaining scientific accuracy, extracting domain technical terms with definitions, and outlining core research takeaways.

---

## 2. Problem Statement (PS7) & Objectives

### Problem Statement (PS7)
> *"Research paper abstracts contain difficult technical terms, complex sentences, and academic jargon that are hard for first-year students to understand."*

### Core Objectives
1. **Plain-English Simplification:** Rewrite complex research abstracts into clear, beginner-friendly English suitable for first-year college students.
2. **Factual Fidelity:** Preserve original research findings, methodologies, and conclusions without inventing facts or hallucinating results.
3. **Automated Lexicon Extraction:** Dynamically identify 5–10 domain-specific technical terms from the abstract and generate concise, understandable explanations.
4. **Structured Key Takeaways:** Distill 3–5 high-impact bullet points covering the research objective, methodology, and outcome.
5. **Interactive Academic UI:** Provide side-by-side comparative visualization, word-count analytics, and multi-format export capabilities (TXT and PDF).

---

## 3. Key Features

| Feature | Description |
| :--- | :--- |
| **Input & Word Analytics** | Large text area with character and word counters, auto-cleaning, and instant input clearing. |
| **Preloaded Samples** | 3 built-in domain abstracts: *Artificial Intelligence* (ResNet), *Healthcare & Biotechnology* (CRISPR-Cas9), and *Environmental Science* (Ocean Acidification). |
| **Zero-Hallucination Prompting** | Tailored system prompt instructing Gemini to avoid external additions and ground explanations strictly on user input. |
| **Side-by-Side Comparison** | Equal-width dual cards comparing original abstract against simplified output with brevity/reduction metrics. |
| **Difficult Term Glossary** | Dynamic extraction of 5–10 challenging terms formatted into a structured data table. |
| **Executive Takeaways** | 3–5 bullet points summarizing objectives, methods, and results. |
| **Multi-Format Export** | One-click copy to clipboard, structured plain-text report (`.txt`), and formatted academic document (`.pdf`). |
| **Configurable AI Engine** | Sidebar controls for model selection (`gemini-2.5-flash`, `gemini-1.5-flash`, etc.), temperature adjustment, and runtime API key input. |

---

## 4. Technology Stack

- **Programming Language:** Python 3.11+
- **Frontend / UI:** Streamlit (Custom CSS with Blue/Purple modern academic theme)
- **Generative AI Model:** Google Gemini 2.5 Flash / Gemini 1.5 Flash
- **API SDK:** `google-genai` (Official Google GenAI Python SDK)
- **Data Validation:** Pydantic v2 (Strict Schema Enforcement)
- **Environment Management:** `python-dotenv`
- **Document Export:** `fpdf2` (Lightweight, pure-Python PDF rendering)
- **Testing Framework:** `pytest`
- **Database:** None required (Stateless architecture)

---

## 5. System Architecture & Workflow

### Architectural Pipeline

```
[ User Abstract Input / Sample Selector ]
                    │
                    ▼
          [ Input Validation ] (Length, emptiness checks)
                    │
                    ▼
     [ Gemini Prompt Engineering ] (ai_service.py)
                    │
                    ▼
      [ Google Gemini API Engine ] (google-genai SDK)
                    │
                    ▼
         [ Structured JSON Response ]
                    │
                    ▼
       [ Pydantic Schema Validator ]
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 [ Side-by-Side Cards ]   [ Technical Glossary Table ]
 [ Word Count Metrics ]   [ Key Takeaways Bullets   ]
        │
        ▼
 [ Export Engine (TXT & PDF Reports) ]
```

### Prompt Engineering Architecture
The LLM prompt strictly constrains Gemini using instructions:
1. Explain in simple, clear, beginner-friendly English.
2. Preserve original research findings.
3. Eliminate unnecessary academic jargon.
4. Dynamically identify 5–10 technical terms actually present in the input.
5. Generate 3–5 core takeaways.
6. Forbid introducing unsubstantiated claims or hallucinatory metrics.
7. Enforce JSON schema output through `response_schema` and `response_mime_type="application/json"`.

---

## 6. Project Folder Structure

```
research-abstract-simplifier/
│
├── app.py                      # Main Streamlit web application & UI
├── ai_service.py               # Gemini API client, prompts & schema validation
├── export_service.py           # TXT and PDF report generation utilities
├── sample_abstracts.py         # Built-in authentic abstracts across 3 domains
├── requirements.txt            # Python package dependencies
├── .env.example                # Template for environment variables
├── .env                        # Local API key configuration (git-ignored)
├── .gitignore                  # Git ignore rules
├── README.md                   # Complete academic project documentation
│
└── tests/
    └── test_samples.py         # Pytest suite with 8 tests covering 5 test cases
```

---

## 7. Installation & Setup

### Prerequisites
- Python 3.11 or higher installed on your computer.
- Git (optional, for cloning).

### Step-by-Step Installation

1. **Navigate to the Project Directory:**
   ```bash
   cd "c:\Users\saksh\OneDrive\Desktop\Research Paper Abstract"
   ```

2. **(Optional) Create and Activate a Virtual Environment:**
   ```bash
   # On Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. Obtaining and Configuring Google Gemini API Key

1. Visit **Google AI Studio**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account.
3. Click **"Create API Key"** and copy your generated key string.
4. Create a `.env` file in the project root by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Open `.env` and paste your key:
   ```ini
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   GEMINI_MODEL=gemini-2.5-flash
   ```

> *Tip:* You can also enter the Gemini API key directly into the application's sidebar password field during a live demonstration!

---

## 9. Running the Application

Execute either of the following commands in your terminal:

```bash
# Recommended (runs via Python module even if Scripts is not on PATH):
python -m streamlit run app.py

# Or if streamlit is on your system PATH:
streamlit run app.py

# On Windows, you can also simply double-click or run:
.\run_app.bat
```

Streamlit will launch local server:
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```
Open your browser at `http://localhost:8501` to use the application.

---

## 10. Sample Inputs and Expected Outputs

### Built-in Sample 1: Artificial Intelligence (Deep Learning)
- **Paper:** *Deep Residual Learning for Image Recognition (He et al.)*
- **Original Jargon:** *Residual functions, degradation problem, vanishing gradient, identity shortcut connections, ILSVRC.*
- **Simplified Explanation:** "As deep neural networks grow larger, they become very hard to train because learning signals fade away. The authors introduced 'ResNets' with shortcut connections that allow information to skip layers, solving the training problem and winning the world's top image recognition competition."
- **Key Terms Identified:** *Residual learning, Degradation problem, Vanishing gradient, Identity shortcuts, ImageNet.*

### Built-in Sample 2: Healthcare & Genomics
- **Paper:** *CRISPR-Cas9 Gene Editing for Targeted Therapeutics in Oncology*
- **Original Jargon:** *Single-guide RNA (sgRNA), Cas9 endonuclease, double-strand breaks, autologous T-lymphocytes, PD-1 locus.*
- **Simplified Explanation:** "CRISPR-Cas9 acts like molecular scissors to cut and edit DNA. In this clinical study, doctors modified cancer patients' own immune cells to disable a gene (PD-1) that tumors use to hide, helping the immune cells destroy cancer cells with very few side effects."
- **Key Terms Identified:** *CRISPR-Cas9, Endonuclease, sgRNA, T-lymphocytes, PD-1 locus, Off-target cleavage.*

### Built-in Sample 3: Environmental Science
- **Paper:** *Anthropogenic Ocean Acidification and Marine Calcification Cascades*
- **Original Jargon:** *Aragonite saturation states, hermatypic scleractinian corals, pelagic pteropods, mesocosm experiments, trophic cascades.*
- **Simplified Explanation:** "Carbon dioxide pollution is making oceans more acidic. Researchers tested marine animals in future water conditions and discovered a 34% drop in coral growth and shell dissolving, warning that entire ocean food chains could collapse if emissions are not reduced."
- **Key Terms Identified:** *Ocean acidification, Aragonite saturation, Calcification rates, Mesocosm experiments, Trophic cascades.*

---

## 11. Testing Suite & Test Cases

The project includes an automated test suite executed with `pytest`:

```bash
python -m pytest tests/test_samples.py -v
```

### Test Case Coverage

| Test Case | Description | Verification Criteria | Status |
| :---: | :--- | :--- | :---: |
| **Case 1** | Short AI research abstract | Validates prompt construction, length checks, and response parsing. | **PASSED** |
| **Case 2** | Complex ML research abstract (ResNet) | Verifies extraction of 5–10 terms and beginner simplification. | **PASSED** |
| **Case 3** | Healthcare abstract (CRISPR-Cas9) | Verifies oncology terminology parsing and takeaway distillation. | **PASSED** |
| **Case 4** | Environmental science abstract | Verifies ecological and geochemical term extraction. | **PASSED** |
| **Case 5** | Empty, whitespace, & short input | Confirms `InvalidInputError` with appropriate user-facing alerts. | **PASSED** |
| **Case 6** | Missing API key handling | Confirms `MissingApiKeyError` triggers informative setup guides. | **PASSED** |
| **Case 7** | Markdown code fence cleaning | Verifies JSON extractor cleans ` ```json ` blocks gracefully. | **PASSED** |
| **Case 8** | Export formatting (TXT and PDF) | Validates plain-text formatting and valid `%PDF` byte stream. | **PASSED** |

---

## 12. Academic Viva & Evaluation Guide

This guide is designed for the 10-mark final-year engineering mini project evaluation:

### Key Questions & Model Answers

1. **What is Problem Statement PS7?**  
   *Answer:* PS7 addresses the difficulty first-year students and non-experts encounter when reading technical research abstracts due to complex syntax and academic jargon. Our solution automates simplification, jargon extraction, and takeaway summarization.

2. **Why use Google Gemini Flash models instead of larger models?**  
   *Answer:* `gemini-2.5-flash` and `gemini-1.5-flash` deliver high reasoning capabilities, sub-second latency, and support structured JSON schemas natively at low compute overhead, making them ideal for interactive academic applications.

3. **How does the application prevent hallucinations?**  
   *Answer:* Through prompt engineering:
   - Clear system instructions forbidding unsubstantiated claims.
   - Low temperature setting (`0.2`) to favor deterministic, grounded responses.
   - Pydantic schema validation to ensure the response adheres strictly to the required fields.

4. **Why is the official `google-genai` SDK used?**  
   *Answer:* `google-genai` is Google's modern, unified SDK supporting Gemini 2.x, typed configuration (`GenerateContentConfig`), and native structured output with Pydantic classes.

5. **How is the PDF report generated without external server dependencies?**  
   *Answer:* Using `fpdf2`, a lightweight, pure-Python library that constructs vector PDF tables and typography in memory with safe Latin-1 transliteration.

---

## 13. Future Enhancements

- **Direct PDF/ArXiv Paper Upload:** Upload research papers directly via URL or file upload and extract abstracts with `pypdf`.
- **Multilingual Translation:** Simplify abstracts directly into Indian regional languages (Hindi, Tamil, Telugu, Marathi).
- **Interactive Flashcards:** Convert extracted difficult terms into digital flashcards for revision.
- **Audio Synthesis:** Text-to-speech integration to listen to simplified abstracts on mobile devices.

---

## License & Academic Disclaimer

This project is created solely for academic evaluation under BTech Computer Science & Engineering. All sample abstracts are derived from published open-access scientific literature.
