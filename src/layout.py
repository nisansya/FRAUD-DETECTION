import streamlit as st

def load_css():
    st.set_page_config(
        page_title="FraudGuard | Credit Card Fraud Detection",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    .stApp {
        background-color: #0B1120;
        color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    [data-testid="stSidebar"] * {
        color: #E5E7EB;
    }

    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: linear-gradient(
            135deg, #172033, #111827
        );
        border: 1px solid #263449;
        border-radius: 14px;
        padding: 20px;
        min-height: 120px;
    }

    .metric-label {
        font-size: 13px;
        color: #94A3B8;
        margin-bottom: 12px;
    }

    .metric-value {
        font-size: 15px;
        font-weight: 700;
        color: #F8FAFC;
    }

    .metric-caption {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 8px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 15px;
        color: #F8FAFC;
    }

    .status {
        display: inline-block;
        background-color: #12352D;
        color: #4ADE80;
        padding: 8px 13px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    .upload-box {
        background-color: #111827;
        border: 1px solid #263449;
        padding: 22px;
        border-radius: 14px;
    }

    .stButton > button {
        background-color: #6366F1;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        padding: 10px;
    }

    .stButton > button:hover {
        background-color: #4F46E5;
        color: white;
        border: none;
    }

    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #263449;
        padding: 15px;
        border-radius: 12px;
    }

    hr {
        border-color: #263449;
    }

    </style>
    """, unsafe_allow_html=True)

