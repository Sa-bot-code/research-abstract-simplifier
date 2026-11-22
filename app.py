"""Research Paper Abstract Simplifier (PS7).

A Streamlit Generative AI application for final-year BTech CSE academic submission.
Transforms complex academic research abstracts into beginner-friendly explanations,
dynamically extracts technical terms with simple meanings, and identifies key takeaways.
"""

from __future__ import annotations

import os
import streamlit as st
from dotenv import load_dotenv

from ai_service import (
    DEFAULT_MODEL,
    InvalidApiKeyError,
    InvalidInputError,
    MissingApiKeyError,
    NetworkConnectivityError,
    RateLimitError,
    SimplificationResult,
    SimplificationServiceError,
    simplify_abstract,
)
from export_service import generate_pdf_report, generate_txt_report
from sample_abstracts import SAMPLE_ABSTRACTS, get_sample_names

# Load environment configuration
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Research Paper Abstract Simplifier | PS7",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern academic styling with Blue, White, and Purple theme
st.markdown(
    """
    <style>
    /* Global Typography and Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1280px;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #7C3AED 100%);
        border-radius: 16px;
        padding: 2.2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.25);
    }
    .main-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
        color: #FFFFFF !important;
    }
    .main-header p {
        font-size: 1.1rem;
        margin-top: 0.6rem;
        margin-bottom: 0.8rem;
        color: #E0E7FF;
        font-weight: 400;
    }
    .academic-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: #FFFFFF;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    /* Card Containers */
    .custom-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .custom-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }

    .original-card {
        border-top: 4px solid #3B82F6;
    }

    .simplified-card {
        border-top: 4px solid #8B5CF6;
        background: #FAFAFF;
    }

    .card-header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #EDF2F7;
        padding-bottom: 0.6rem;
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .stat-pill {
        background: #EEF2FF;
        color: #4338CA;
        font-weight: 600;
        font-size: 0.8rem;
        padding: 0.25rem 0.65rem;
        border-radius: 12px;
        border: 1px solid #C7D2FE;
    }

    /* Takeaways styling */
    .takeaway-item {
        background: #F8FAFC;
        border-left: 4px solid #6366F1;
        padding: 0.85rem 1.1rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.65rem;
        font-size: 0.96rem;
        color: #334155;
        line-height: 1.5;
    }

    /* Difficult terms table styling */
    .term-badge {
        background: #F3E8FF;
        color: #6B21A8;
        font-weight: 700;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.9rem;
    }

    /* Metric counter banner */
    .counter-bar {
        display: flex;
        gap: 1rem;
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: -0.4rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "abstract_input" not in st.session_state:
        st.session_state.abstract_input = ""
    if "result" not in st.session_state:
        st.session_state.result = None
    if "sample_loaded_name" not in st.session_state:
        st.session_state.sample_loaded_name = None


initialize_session_state()

# Sidebar Configuration
with st.sidebar:
    st.image(
        "https://api.iconify.design/lucide:sparkles.svg?color=%234F46E5&width=48",
        width=48,
    )
    st.title("System Settings")

    st.markdown("### 🔑 Gemini API Key")
    env_api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if env_api_key and env_api_key != "your_gemini_api_key_here":
        st.success("API Key detected in `.env` file", icon="✅")
        use_manual_key = st.checkbox("Override with a different key", value=False)
        if use_manual_key:
            user_api_key = st.text_input(
                "Enter Custom Gemini API Key",
                type="password",
                help="Your key remains private and is never logged or saved.",
            )
        else:
            user_api_key = env_api_key
    else:
        st.warning("No API key found in `.env` file.", icon="⚠️")
        user_api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Get your key at https://aistudio.google.com/app/apikey",
        )
        if user_api_key:
            st.info("API Key entered for this session.", icon="🔒")

    st.markdown("---")
    st.markdown("### ⚙️ Model Parameters")
    model_options = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash",
        "gemini-3.7-flash",
    ]
    env_model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    default_index = model_options.index(env_model) if env_model in model_options else 0
    selected_model = st.selectbox("Gemini Model", model_options, index=default_index)

    temperature = st.slider(
        "Temperature (Creativity vs Fidelity)",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Lower values (0.1 - 0.3) provide higher factual accuracy and less hallucination.",
    )

    st.markdown("---")
    st.markdown("### 📌 Academic Information")
    st.markdown(
        """
        - **Project Title:** Research Paper Abstract Simplifier
        - **Problem Statement:** PS7
        - **Academic Level:** BTech CSE Final Year
        - **SDK:** `google-genai` (Official)
        - **Framework:** Streamlit + Python 3.11+
        """
    )

    with st.expander("📖 Viva Preparation & FAQs"):
        st.markdown(
            """
            **Q: How does the AI avoid hallucination?**  
            *A: Strict prompt instructions prevent external facts, low temperature (0.2) constrains sampling, and Pydantic enforces schema output.*

            **Q: Why use Structured JSON Output?**  
            *A: It guarantees programmatic separation of simplified text, difficult terms, and takeaways without parsing errors.*

            **Q: What is the benefit of google-genai SDK?**  
            *A: It is Google's new official SDK supporting Gemini 2.5/2.0 native function calling, typed schemas, and flash models.*
            """
        )

# Main Banner Header
st.markdown(
    """
    <div class="main-header">
        <span class="academic-badge">Academic Submission • Problem Statement PS7</span>
        <h1>Research Paper Abstract Simplifier</h1>
        <p>Understand Complex Research in Simple Words Using Generative AI</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Feature 1: Sample Abstracts Showcase
st.markdown("##### 💡 Load a Sample Research Abstract")
sample_cols = st.columns(3)

for idx, (domain_key, sample_data) in enumerate(SAMPLE_ABSTRACTS.items()):
    with sample_cols[idx]:
        if st.button(
            f"📄 {domain_key}",
            use_container_width=True,
            help=f"Load: '{sample_data['title']}'",
        ):
            st.session_state.abstract_input = sample_data["abstract"]
            st.session_state.sample_loaded_name = domain_key
            st.session_state.result = None
            st.rerun()

if st.session_state.sample_loaded_name:
    sample_info = SAMPLE_ABSTRACTS[st.session_state.sample_loaded_name]
    st.caption(
        f"**Loaded Sample:** *{sample_info['title']}* ({sample_info['domain']})"
    )

# Feature 1: Abstract Input Area
current_text = st.session_state.abstract_input
abstract_text = st.text_area(
    label="Research Paper Abstract Input",
    value=current_text,
    placeholder="Paste your research paper abstract here...",
    height=200,
    help="Paste an authentic academic abstract with technical terms.",
    label_visibility="collapsed",
)

# Keep session state updated with text changes
st.session_state.abstract_input = abstract_text

# Real-time word and character count
word_count = len(abstract_text.split()) if abstract_text.strip() else 0
char_count = len(abstract_text)

st.markdown(
    f"""
    <div class="counter-bar">
        <span>📝 <strong>Words:</strong> {word_count}</span>
        <span>🔤 <strong>Characters:</strong> {char_count}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Action Buttons: Simplify & Clear
btn_col1, btn_col2, btn_spacer = st.columns([2, 1.2, 5])

with btn_col1:
    simplify_clicked = st.button(
        "✨ Simplify Abstract",
        type="primary",
        use_container_width=True,
    )

with btn_col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.abstract_input = ""
        st.session_state.result = None
        st.session_state.sample_loaded_name = None
        st.rerun()

# Feature 2: Simplification Execution Logic
if simplify_clicked:
    if not abstract_text.strip():
        st.error("⚠️ Please enter or load a research paper abstract before simplifying.")
    elif word_count < 10:
        st.warning("⚠️ The abstract provided is too short. Please provide at least 15-20 words for meaningful simplification.")
    else:
        with st.spinner("🧠 Analyzing abstract, extracting technical terms, and simplifying with Gemini AI..."):
            try:
                simplification = simplify_abstract(
                    abstract_text=abstract_text,
                    api_key=user_api_key,
                    model_name=selected_model,
                    temperature=temperature,
                )
                st.session_state.result = simplification
                st.success("✅ Abstract simplified successfully!", icon="🎉")
            except MissingApiKeyError as e:
                st.error(f"🔑 **API Key Required:** {e}")
                st.info("💡 **Quick Fix:** Enter your Gemini API key in the left sidebar or create a `.env` file with `GEMINI_API_KEY=your_key`.")
            except InvalidApiKeyError as e:
                st.error(f"⛔ **Authentication Error:** {e}")
                st.info("💡 Please verify that your Gemini API key is valid at https://aistudio.google.com/app/apikey")
            except NetworkConnectivityError as e:
                st.error(f"🌐 **Connection Error:** {e}")
            except RateLimitError as e:
                st.warning(f"⏳ **Rate Limit:** {e}")
            except InvalidInputError as e:
                st.warning(f"⚠️ {e}")
            except SimplificationServiceError as e:
                st.error(f"❌ **Simplification Error:** {e}")
            except Exception as e:
                st.error(f"❌ **Unexpected Error:** {e}")

# Display Results if Available
result: SimplificationResult = st.session_state.result

if result:
    st.markdown("---")
    
    # Feature 3: Side-by-Side Comparison
    st.markdown("### 📊 Side-by-Side Comparison")
    col_orig, col_simp = st.columns(2)

    orig_words = len(abstract_text.split())
    simp_words = len(result.simplified_abstract.split())

    with col_orig:
        st.markdown(
            f"""
            <div class="custom-card original-card">
                <div class="card-header-flex">
                    <h4 class="card-title" style="color: #1E3A8A;">📄 Original Abstract</h4>
                    <span class="stat-pill">{orig_words} words</span>
                </div>
                <p style="color: #334155; line-height: 1.65; font-size: 0.98rem; text-align: justify;">
                    {abstract_text.strip()}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_simp:
        reduction_pct = max(0, 100 - int((simp_words * 100) / max(1, orig_words)))
        st.markdown(
            f"""
            <div class="custom-card simplified-card">
                <div class="card-header-flex">
                    <h4 class="card-title" style="color: #6D28D9;">✨ Simplified Abstract (Student-Friendly)</h4>
                    <span class="stat-pill" style="background:#EDE9FE; color:#6D28D9; border-color:#DDD6FE;">
                        {simp_words} words ({reduction_pct}% reduction)
                    </span>
                </div>
                <p style="color: #1E1B4B; line-height: 1.7; font-size: 1.02rem; font-weight: 450; text-align: justify;">
                    {result.simplified_abstract.strip()}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature 5: Key Takeaways
    st.markdown("### 🎯 Key Research Takeaways")
    st.markdown("<p style='color:#64748B;'>Core research objectives, methodologies, and findings explained for beginners:</p>", unsafe_allow_html=True)

    takeaway_html = ""
    for idx, takeaway in enumerate(result.key_takeaways, 1):
        takeaway_html += f"""
        <div class="takeaway-item">
            <strong>Key Point {idx}:</strong> {takeaway}
        </div>
        """
    st.markdown(takeaway_html, unsafe_allow_html=True)

    # Feature 4: Difficult Terms and Meanings
    st.markdown("### 📚 Difficult Technical Terms & Meanings")
    st.markdown("<p style='color:#64748B;'>Technical jargon automatically extracted from the abstract with simple explanations:</p>", unsafe_allow_html=True)

    # Format into DataFrame / Table
    terms_data = [
        {"Technical Term": item.term, "Beginner-Friendly Meaning": item.meaning}
        for item in result.difficult_terms
    ]

    st.dataframe(
        terms_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Technical Term": st.column_config.TextColumn(
                "Technical Term",
                width="medium",
                help="Technical term from the original abstract",
            ),
            "Beginner-Friendly Meaning": st.column_config.TextColumn(
                "Beginner-Friendly Meaning",
                width="large",
                help="Simplified everyday explanation",
            ),
        },
    )

    # Feature 6: Download and Copy Section
    st.markdown("---")
    st.markdown("### 📥 Export & Share Results")

    exp_col1, exp_col2, exp_col3 = st.columns(3)

    # Text report generation
    txt_content = generate_txt_report(
        original_abstract=abstract_text,
        result=result,
        model_name=selected_model,
    )

    # PDF report generation
    pdf_bytes = generate_pdf_report(
        original_abstract=abstract_text,
        result=result,
        model_name=selected_model,
    )

    with exp_col1:
        st.download_button(
            label="📄 Download Report as TXT",
            data=txt_content,
            file_name="abstract_simplification_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with exp_col2:
        st.download_button(
            label="📑 Download Report as PDF",
            data=pdf_bytes,
            file_name="abstract_simplification_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with exp_col3:
        # Streamlit copy snippet
        with st.popover("📋 Copy Simplified Text", use_container_width=True):
            st.caption("Copy the simplified text below:")
            st.code(result.simplified_abstract, language="text")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem; padding: 1rem 0;">
        <strong>Research Paper Abstract Simplifier</strong> • Problem Statement PS7 • Final Year BTech CSE Mini Project<br>
        Built with Streamlit & Google Gemini API (<code>google-genai</code>)
    </div>
    """,
    unsafe_allow_html=True,
)
