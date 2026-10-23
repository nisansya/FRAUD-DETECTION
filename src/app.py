import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
# from pathlib import Path
from config import MODEL_PATH, SCALER_PATH, THRESHOLD_PATH
from layout import load_css

load_css()


# =====================================================
# 3. LOAD TRAINED MODEL AND SCALER
# =====================================================

@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():
        return None, None

    model = joblib.load(MODEL_PATH)

    scaler = None

    if SCALER_PATH.exists():
        scaler = joblib.load(SCALER_PATH)

    if THRESHOLD_PATH.exists():
        threshold= joblib.load(THRESHOLD_PATH)

    return model, scaler, threshold


try:
    model, scaler, threshold = load_model()

except Exception as error:
    st.error(f"Unable to load model: {error}")
    st.stop()


# =====================================================
# 4. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🛡️ FraudGuard")

    st.caption("AI-Powered Transaction Security")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Fraud Detection",
            "Transaction Analysis",
            "About Project"
        ]
    )

    st.divider()

    if model is not None:
        st.success("Model Loaded")
    else:
        st.error("Model Not Found")

    st.caption("Machine Learning Project")


# =====================================================
# 5. REUSABLE FUNCTIONS
# =====================================================

def page_header(title, subtitle):

    st.markdown(
        f'<div class="main-title">{title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="subtitle">{subtitle}</div>',
        unsafe_allow_html=True
    )


def metric_card(label, value, caption):
    st.html(
        f"""
        <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-caption">{caption}</div>
        </div>
        """
    )

def predict_transactions(df):

    if model is None:
        raise RuntimeError(
            "Trained model was not found."
        )

    # Exclude the target column if the uploaded CSV
    # contains ground-truth labels.
    X = df.drop(
        columns=["Class"],
        errors="ignore"
    ).copy()

    # Preserve the training feature order when available.
    if hasattr(model, "feature_names_in_"):

        expected_features = list(
            model.feature_names_in_
        )

        missing = [
            col for col in expected_features
            if col not in X.columns
        ]

        extra = [
            col for col in X.columns
            if col not in expected_features
        ]

        if missing or extra:
            raise ValueError(
                f"Feature mismatch. Missing: {missing}; "
                f"unexpected: {extra}"
            )

        X = X[expected_features]

    elif scaler is not None and hasattr(
        scaler, "feature_names_in_"
    ):

        expected_features = list(
            scaler.feature_names_in_
        )

        missing = [
            col for col in expected_features
            if col not in X.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required features: {missing}"
            )

        X = X[expected_features]

    # Validate numeric values.
    X = X.apply(
        pd.to_numeric,
        errors="raise"
    )

    if not np.isfinite(
        X.to_numpy(dtype=float)
    ).all():

        raise ValueError(
            "Input contains missing or infinite values."
        )

    # Apply the same scaler used during training.
    if scaler is not None:
        X_processed = scaler.transform(X)
    else:
        X_processed = X

    y_prob= model.predict_proba(X_processed)[:, 1]
    predictions = (y_prob > threshold).astype(int)

    results = df.copy()

    results["Prediction"] = np.where(
        predictions == 1,
        "Fraud",
        "Normal"
    )

    results["Fraud Probability (%)"] = (
        y_prob * 100
    ).round(2)

    return results


# =====================================================
# 6. DASHBOARD PAGE
# =====================================================

if page == "Dashboard":

    page_header(
        "Credit Card Fraud Detection",
        "Monitor transactions and identify potentially "
        "fraudulent activities using machine learning."
    )

    if model is not None:

        st.markdown(
            '<span class="status">● MODEL READY</span>',
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "Model files are missing. Save your trained "
            "model in the models folder."
        )

    st.markdown(
        '<div class="section-title">System Overview</div>',
        unsafe_allow_html=True
    )

    # Metrics become meaningful after transactions
    # have been analyzed in this Streamlit session.
    results = st.session_state.get(
        "prediction_results"
    )

    if results is not None:

        total = len(results)

        fraud_count = int(
            (results["Prediction"] == "Fraud").sum()
        )

        normal_count = total - fraud_count

        fraud_rate = (
            fraud_count / total * 100
            if total > 0 else 0
        )

    else:

        total = 0
        fraud_count = 0
        normal_count = 0
        fraud_rate = 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Transactions Analyzed",
            f"total:{total}",
            "Current session"
        )

    with c2:
        metric_card(
            "Potential Fraud",
            f"{fraud_count:,}",
            "Flagged by the model"
        )

    with c3:
        metric_card(
            "Normal Transactions",
            f"{normal_count:,}",
            "Classified as normal"
        )

    with c4:
        metric_card(
            "Flagged Rate",
            f"{fraud_rate:.2f}%",
            "Of analyzed transactions"
        )

    st.markdown(
        '<div class="section-title">Fraud Analytics</div>',
        unsafe_allow_html=True
    )

    if results is not None and total > 0:

        left, right = st.columns(2)

        with left:

            counts = (
                results["Prediction"]
                .value_counts()
                .reindex(
                    ["Normal", "Fraud"],
                    fill_value=0
                )
                .rename_axis("Status")
                .reset_index(name="Count")
            )

            fig = px.pie(
                counts,
                names="Status",
                values="Count",
                hole=0.65,
                title="Fraud vs Normal Transactions",
                color="Status",
                color_discrete_map={
                    "Normal": "#6366F1",
                    "Fraud": "#F43F5E"
                }
            )

            fig.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font_color="#E5E7EB"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with right:

            if "Amount" in results.columns:

                fig = px.histogram(
                    results,
                    x="Amount",
                    color="Prediction",
                    nbins=35,
                    title="Transaction Amount Distribution",
                    color_discrete_map={
                        "Normal": "#6366F1",
                        "Fraud": "#F43F5E"
                    }
                )

                fig.update_layout(
                    paper_bgcolor="#111827",
                    plot_bgcolor="#111827",
                    font_color="#E5E7EB"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No Amount column is available for plotting."
                )

        st.markdown("### Latest Predictions")

        st.dataframe(
            results.tail(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Upload a transaction CSV from Fraud Detection "
            "to populate your dashboard."
        )


# =====================================================
# 7. FRAUD DETECTION PAGE
# =====================================================

elif page == "Fraud Detection":

    page_header(
        "Fraud Detection",
        "Upload transaction records and analyze them "
        "with your trained machine learning model."
    )

    st.markdown(
        '<div class="upload-box">'
        '<h4>📁 Upload Transaction Dataset</h4>'
        '<p style="color:#94A3B8;">'
        'Upload a CSV containing the same input features '
        'used during model training.'
        '</p></div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            st.markdown("### Dataset Preview")

            st.write(
                f"Rows: {df.shape[0]:,} | "
                f"Columns: {df.shape[1]:,}"
            )

            st.dataframe(
                df.head(10),
                use_container_width=True
            )

            if st.button(
                "🔍 Analyze Transactions",
                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing transactions..."
                ):

                    results = predict_transactions(df)

                    st.session_state[
                        "prediction_results"
                    ] = results

                st.success(
                    "Transaction analysis completed!"
                )

                fraud_count = int(
                    (
                        results["Prediction"] == "Fraud"
                    ).sum()
                )

                normal_count = (
                    len(results) - fraud_count
                )

                a, b, c = st.columns(3)

                a.metric(
                    "Total Transactions",
                    len(results)
                )

                b.metric(
                    "Potential Fraud",
                    fraud_count
                )

                c.metric(
                    "Normal",
                    normal_count
                )

                st.markdown("### Prediction Results")

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "⬇️ Download Predictions",
                    data=results.to_csv(
                        index=False
                    ).encode("utf-8"),
                    file_name="fraud_predictions.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        except Exception as error:

            st.error(
                f"Unable to process the file: {error}"
            )

# =====================================================
# 8. TRANSACTION ANALYSIS PAGE
# =====================================================

elif page == "Transaction Analysis":

    page_header(
        "Transaction Analysis",
        "Inspect your latest transaction predictions."
    )

    results = st.session_state.get(
        "prediction_results"
    )

    if results is None:

        st.info(
            "First upload a CSV and run fraud detection."
        )

    else:

        st.markdown("### Analysis Summary")

        st.dataframe(
            results.describe(include="all").T,
            use_container_width=True
        )

        if "Fraud Probability (%)" in results.columns:

            fig = px.histogram(
                results,
                x="Fraud Probability (%)",
                nbins=30,
                title="Predicted Fraud Probability Distribution"
            )

            fig.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font_color="#E5E7EB"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if "Amount" in results.columns:

            fig = px.box(
                results,
                x="Prediction",
                y="Amount",
                color="Prediction",
                title="Transaction Amount by Prediction"
            )

            fig.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font_color="#E5E7EB"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =====================================================
# 9. ABOUT PROJECT PAGE
# =====================================================

elif page == "About Project":

    page_header(
        "About FraudGuard",
        "Machine learning for credit card fraud classification."
    )

    st.markdown("""
    ### Project Overview

    This project uses a trained machine learning classifier
    to distinguish potentially fraudulent transactions from
    transactions classified as normal.

    ### Technology Stack

    - Python
    - Pandas and NumPy
    - Scikit-learn
    - Streamlit
    - Plotly
    - Joblib

    ### Machine Learning Workflow

    1. Data collection and exploration
    2. Data preprocessing
    3. Handling class imbalance
    4. Model training
    5. Model evaluation
    6. Model and scaler serialization
    7. Streamlit deployment

    ### Important Metrics

    - Precision
    - Recall
    - F1 score
    - Confusion matrix
    - Precision-Recall AUC

    Accuracy alone is not sufficient for fraud detection
    because fraudulent transactions are usually rare.

    ### Important Note

    The application is a portfolio demonstration.
    A prediction is not a guarantee that a transaction
    is safe or fraudulent.
    """)


# =====================================================
# 10. FOOTER
# =====================================================

st.divider()

st.caption(
    "FraudGuard | Credit Card Fraud Detection | "
    "Machine Learning Portfolio Project"
)