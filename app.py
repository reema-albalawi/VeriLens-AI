import os
import time
import streamlit as st
from google import genai
from PIL import Image

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="VeriLens AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# GEMINI CLIENT
# -----------------------------
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# -----------------------------
# CUSTOM DESIGN
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #090b14 0%, #11162a 55%, #171126 100%);
        color: #ffffff;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .block-container {
        max-width: 1050px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    .hero {
        text-align: center;
        padding: 35px 15px 25px 15px;
    }

    .brand {
        font-size: 3.6rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #9b8cff, #55d6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .tagline {
        font-size: 1.45rem;
        color: #d7d9e5;
        margin-bottom: 12px;
    }

    .description {
        color: #9fa5ba;
        font-size: 1rem;
        max-width: 700px;
        margin: auto;
        line-height: 1.7;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #a9aec2;
        margin-bottom: 20px;
    }

    .status-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 22px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .feature-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 18px;
        min-height: 135px;
    }

    .feature-card h4 {
        margin-bottom: 8px;
    }

    .feature-card p {
        color: #aeb3c7;
        font-size: 0.93rem;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.2rem;
        font-weight: 700;
        font-size: 1rem;
    }

    .disclaimer {
        text-align: center;
        color: #777f96;
        font-size: 0.82rem;
        margin-top: 35px;
    }

    h1, h2, h3, h4, p, label {
        color: inherit;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="brand">VeriLens AI</div>
        <div class="tagline">See beyond what looks real.</div>
        <div class="description">
            An AI-powered reality checker that evaluates suspicious digital
            content and explains the signals you should consider before
            trusting or sharing it.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# FEATURE CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🔎 Analyze</h4>
            <p>Submit text, claims, or images for AI-assisted credibility analysis.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🧠 Understand</h4>
            <p>See warning signs, credibility signals, missing context, and limitations.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>✓ Verify</h4>
            <p>Receive practical next steps before trusting or sharing digital content.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="section-title">Analyze Content</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Paste suspicious text, upload an image, or use both.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# USER INPUT
# -----------------------------
content = st.text_area(
    "Text or claim",
    height=160,
    placeholder="Paste a suspicious claim, message, headline, or online content..."
)

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

image = None

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded content", width=500)

# -----------------------------
# ANALYSIS
# -----------------------------
if st.button("Analyze with VeriLens", type="primary"):

    if not content and not uploaded_image:
        st.warning("Please paste text or upload an image first.")

    else:
        prompt = f"""
You are VeriLens AI, an AI-assisted digital content credibility analyst.

Analyze ONLY the information available in the submitted text and/or image.

IMPORTANT RULES:
- Do not claim that you can definitively prove whether content is real or fake.
- Do not claim certainty when evidence is unavailable.
- Clearly distinguish observations from assumptions.
- If external facts cannot be independently verified from the submitted content, say so.
- The credibility score is an advisory heuristic, NOT a statistical probability.
- If the content appears harmless or fictional, explain that clearly.
- If an image is provided, examine visible context and possible manipulation or misleading presentation.
- Be concise, useful, and explain your reasoning.

Return the assessment using EXACTLY these headings:

# VERILENS ASSESSMENT

## Credibility Score
Give a score from 0 to 100.
100 means stronger credibility signals.
0 means severe credibility concerns.
State that this is an advisory score.

## Status
Choose exactly ONE:
LOW CONCERN
NEEDS VERIFICATION
HIGH RISK

## Key Signals
List the most important observations.

## Claim Credibility
Evaluate the claims that can actually be assessed.
If there is no factual claim, say so.

## Source & Context
Discuss source transparency, context, attribution, and anything relevant that is missing.

## Potential Red Flags
Identify misleading wording, inconsistencies, emotional manipulation,
visual concerns, missing context, or other warning signs.
If none are evident, say so.

## What Supports It
List elements that increase credibility.
If none can be established, say so.

## What Is Missing
Explain what additional evidence or context would be needed.

## Recommended Verification Steps
Give specific steps the user should take before trusting or sharing the content.

TEXT SUBMITTED BY USER:
{content if content else "No text was submitted."}
"""

        inputs = [prompt]

        if uploaded_image:
            inputs.append(image)

        response = None

        with st.spinner("VeriLens is examining the content..."):
            try:
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=inputs
                        )
                        break

                    except Exception as api_error:
                        if "503" in str(api_error) and attempt < 2:
                            time.sleep(3)
                        else:
                            raise api_error

                if response:
                    st.divider()
                    st.markdown(response.text)

                    st.info(
                        "VeriLens provides an AI-assisted credibility assessment. "
                        "Its score is advisory and should not be treated as definitive proof."
                    )

            except Exception as e:
                st.error(
                    "VeriLens could not complete the analysis. "
                    "Please check the API connection and try again."
                )
                st.code(str(e))

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    """
    <div class="disclaimer">
        VeriLens AI • AI-assisted credibility analysis • Human verification still matters
    </div>
    """,
    unsafe_allow_html=True
)