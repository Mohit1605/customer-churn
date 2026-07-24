import requests
import streamlit as st
import streamlit.components.v1 as components
from api_client import predict_customer


st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


CUSTOMER_OPTIONS = {
    "gender": ["Male", "Female"],
    "yes_no": ["No", "Yes"],
    "contract": ["Month-to-month", "One year", "Two year"],
    "payment_method": [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ],
    "phone_service": ["Yes", "No"],
    "multiple_lines": ["No", "Yes", "No phone service"],
    "internet_service": ["DSL", "Fiber optic", "No"],
    "service_options": ["No", "Yes", "No internet service"],
}


def render_css() -> None:
    st.markdown(
        """
        <style>
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
            header { visibility: hidden; }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(56, 189, 248, 0.22), transparent 28%),
                    radial-gradient(circle at top right, rgba(168, 85, 247, 0.25), transparent 32%),
                    linear-gradient(180deg, #020617 0%, #0f172a 100%);
                color: #e2e8f0;
            }

            .main {
                background: transparent;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }

            .hero-card {
                position: relative;
                background: linear-gradient(135deg, #0f172a, #1d4ed8 55%, #06b6d4);
                border-radius: 24px;
                padding: 32px;
                color: #f8fafc;
                margin-bottom: 24px;
                box-shadow: 0 20px 45px rgba(14, 165, 233, 0.28);
            }

            .hero-status {
                position: absolute;
                top: 18px;
                right: 18px;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px;
                border-radius: 999px;
                background: rgba(15, 23, 42, 0.72);
                border: 1px solid rgba(255, 255, 255, 0.16);
                color: #f8fafc;
                font-size: 13px;
                font-weight: 700;
                backdrop-filter: blur(8px);
            }

            .hero-status-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #22c55e;
                box-shadow: 0 0 12px rgba(34, 197, 94, 0.95);
            }

            .hero-title {
                font-size: 38px;
                font-weight: 800;
                margin-bottom: 10px;
                letter-spacing: -0.03em;
                color: #f8fafc;
            }

            .hero-subtitle {
                font-size: 18px;
                opacity: 0.95;
                line-height: 1.6;
                color: #dbeafe;
            }

            .section-card {
                background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
                color: #e2e8f0;
                padding: 22px;
                border-radius: 20px;
                border: 1px solid rgba(56, 189, 248, 0.25);
                box-shadow: 0 18px 36px rgba(0, 0, 0, 0.32);
                margin-bottom: 22px;
            }

            .section-title {
                font-size: 24px;
                font-weight: 700;
                color: #f8fafc;
                margin-bottom: 12px;
            }

            div.stButton > button:first-child {
                width: 100%;
                height: 56px;
                border: none;
                border-radius: 14px;
                background: linear-gradient(135deg, #38bdf8, #2563eb);
                color: #f8fafc;
                font-size: 18px;
                font-weight: 700;
                box-shadow: 0 12px 28px rgba(56, 189, 248, 0.3);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            div.stButton > button:hover {
                background: linear-gradient(135deg, #0ea5e9, #1d4ed8);
                transform: translateY(-2px);
                box-shadow: 0 16px 34px rgba(14, 165, 233, 0.42);
            }

            div[data-testid="stForm"] {
                background: rgba(15, 23, 42, 0.78);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(56, 189, 248, 0.22);
                border-radius: 22px;
                padding: 16px;
                box-shadow: 0 18px 36px rgba(0, 0, 0, 0.3);
            }

            .stTabs [role="tablist"] {
                background: rgba(15, 23, 42, 0.7);
                border-radius: 14px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    try:
        response = requests.get("http://127.0.0.1:8000/health/", timeout=5)
        response.raise_for_status()
        backend_connected = response.json().get("status") == "Running"
    except Exception:
        backend_connected = False

    status_text = "Connected" if backend_connected else "Disconnected"
    status_color = "#22c55e" if backend_connected else "#ef4444"

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-status">
                <span class="hero-status-dot" style="background: {status_color}; box-shadow: 0 0 12px {status_color};"></span>
                Backend: {status_text}
            </div>
            <div class="hero-title">📊 Customer Churn Prediction</div>
            <div class="hero-subtitle">
                Predict whether a telecom customer is likely to churn using a Machine Learning model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_customer_profile() -> dict:
    with st.container(border=True):
        st.subheader("👤 Customer Profile")
        st.caption("Basic customer demographic information.")

        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", options=CUSTOMER_OPTIONS["gender"], index=1)
            senior_citizen = st.selectbox(
                "Senior Citizen",
                options=CUSTOMER_OPTIONS["yes_no"],
                index=0,
            )
        with col2:
            partner = st.selectbox("Partner", options=CUSTOMER_OPTIONS["yes_no"], index=1)
            dependents = st.selectbox("Dependents", options=CUSTOMER_OPTIONS["yes_no"], index=0)

    return {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
    }


def render_account_information() -> dict:
    with st.container(border=True):
        st.subheader("📄 Account Information")
        st.caption("Customer subscription and billing details.")

        col1, col2 = st.columns(2)
        with col1:
            tenure = st.number_input(
                "Tenure (Months)",
                min_value=0,
                value=12,
                step=1,
                help="Number of months the customer has stayed with the company.",
            )
            contract = st.selectbox(
                "Contract",
                options=CUSTOMER_OPTIONS["contract"],
                index=0,
            )
            paperless_billing = st.selectbox(
                "Paperless Billing",
                options=CUSTOMER_OPTIONS["yes_no"],
                index=0,
            )

        with col2:
            payment_method = st.selectbox(
                "Payment Method",
                options=CUSTOMER_OPTIONS["payment_method"],
                index=0,
            )
            monthly_charges = st.number_input(
                "Monthly Charges ($)",
                min_value=0.0,
                value=70.0,
                step=0.01,
                format="%.2f",
            )
            total_charges = st.number_input(
                "Total Charges ($)",
                min_value=0.0,
                value=840.0,
                step=0.01,
                format="%.2f",
            )

    return {
        "tenure": tenure,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }


def render_services() -> dict:
    with st.container(border=True):
        st.subheader("📡 Services")
        st.caption("Customer phone and internet service subscriptions.")

        phone_col, internet_col = st.columns(2)

        with phone_col:
            st.markdown("### ☎️ Phone Services")
            phone_service = st.selectbox(
                "Phone Service",
                options=CUSTOMER_OPTIONS["phone_service"],
                index=0,
            )
            multiple_lines = st.selectbox(
                "Multiple Lines",
                options=CUSTOMER_OPTIONS["multiple_lines"],
                index=0,
            )

        with internet_col:
            st.markdown("### 🌐 Internet Services")
            internet_service = st.selectbox(
                "Internet Service",
                options=CUSTOMER_OPTIONS["internet_service"],
                index=1,
            )
            online_security = st.selectbox(
                "Online Security",
                options=CUSTOMER_OPTIONS["service_options"],
                index=0,
            )
            online_backup = st.selectbox(
                "Online Backup",
                options=CUSTOMER_OPTIONS["service_options"],
                index=1,
            )
            device_protection = st.selectbox(
                "Device Protection",
                options=CUSTOMER_OPTIONS["service_options"],
                index=0,
            )
            tech_support = st.selectbox(
                "Tech Support",
                options=CUSTOMER_OPTIONS["service_options"],
                index=0,
            )
            streaming_tv = st.selectbox(
                "Streaming TV",
                options=CUSTOMER_OPTIONS["service_options"],
                index=1,
            )
            streaming_movies = st.selectbox(
                "Streaming Movies",
                options=CUSTOMER_OPTIONS["service_options"],
                index=1,
            )

    return {
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
    }


def build_request_payload() -> dict:
    request_data = render_customer_profile()
    request_data.update(render_account_information())
    request_data.update(render_services())
    return request_data


def render_result(prediction_data: dict) -> None:
    prediction = prediction_data["prediction"]
    probability = prediction_data["prediction_probability"] * 100
    confidence = prediction_data["confidence"]

    if prediction == "Churn":
        accent = "#ef4444"
        accent_soft = "rgba(239, 68, 68, 0.12)"
        icon = "🔴"
        status = "At Risk"
        badge = "High Risk"
        recommendation = (
            "Offer a retention discount, personalized plan, or proactive customer support."
        )
    else:
        accent = "#10b981"
        accent_soft = "rgba(16, 185, 129, 0.12)"
        icon = "🟢"
        status = "Stable"
        badge = "Healthy"
        recommendation = (
            "Customer appears loyal. Continue providing excellent service and engagement."
        )

    html = f"""
    <style>
        body {{ font-family: "Source Sans", sans-serif; }}
        .prediction-card {{
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            color: #e2e8f0;
            padding: 28px;
            border-radius: 24px;
            box-shadow: 0 20px 45px rgba(3, 7, 18, 0.55);
            border: 1px solid rgba(56, 189, 248, 0.24);
            margin-top: 30px;
            font-family: "Source Sans", sans-serif;
        }}
        .prediction-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 22px;
        }}
        .prediction-title {{
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            color: #f8fafc;
        }}
        .prediction-badge {{
            background: {accent_soft};
            color: {accent};
            border: 1px solid rgba(255,255,255,0.12);
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }}
        .hero-row {{
            display: grid;
            grid-template-columns: 120px 1fr;
            align-items: center;
            gap: 18px;
            background: linear-gradient(135deg, rgba(37,99,235,0.16), rgba(6,182,212,0.1));
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 22px;
            border: 1px solid rgba(56, 189, 248, 0.16);
        }}
        .prediction-icon {{
            text-align: center;
            font-size: 62px;
            line-height: 1;
        }}
        .prediction-label {{
            font-size: 34px;
            font-weight: 800;
            color: {accent};
            margin-bottom: 3px;
        }}
        .prediction-status {{
            font-size: 16px;
            color: #cbd5e1;
            font-weight: 600;
        }}
        .risk-section {{
            background: rgba(15, 23, 42, 0.86);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 18px;
            border: 1px solid rgba(56, 189, 248, 0.18);
        }}
        .risk-header {{
            margin: 0 0 10px;
            font-size: 15px;
            font-weight: 700;
            color: #f8fafc;
        }}
        .risk-progress {{
            width: 100%;
            height: 16px;
            accent-color: {accent};
            border-radius: 999px;
        }}
        .risk-value {{
            text-align: right;
            font-size: 16px;
            font-weight: 800;
            margin-top: 8px;
            color: {accent};
        }}
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-top: 18px;
        }}
        .stat-card {{
            background: rgba(15, 23, 42, 0.86);
            border-radius: 16px;
            padding: 14px;
            border: 1px solid rgba(56, 189, 248, 0.18);
            text-align: center;
        }}
        .stat-label {{
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: 800;
            color: #f8fafc;
        }}
        .recommendation-box {{
            background: linear-gradient(135deg, rgba(37,99,235,0.16), rgba(6,182,212,0.12));
            border-radius: 16px;
            padding: 16px;
            margin-top: 14px;
            border: 1px solid rgba(56, 189, 248, 0.16);
        }}
        .recommendation-title {{
            margin: 0 0 8px;
            font-size: 15px;
            font-weight: 800;
            color: #f8fafc;
        }}
        .recommendation {{
            font-size: 15px;
            line-height: 1.7;
            color: #dbeafe;
            margin: 0;
        }}
        @media (max-width: 760px) {{
            .hero-row {{ grid-template-columns: 1fr; text-align: center; }}
            .stats-row {{ grid-template-columns: 1fr; }}
            .prediction-header {{ flex-direction: column; align-items: flex-start; }}
        }}
    </style>
    <div class="prediction-card">
        <div class="prediction-header">
            <h2 class="prediction-title">🎯 Prediction Result</h2>
            <div class="prediction-badge">{badge}</div>
        </div>

        <div class="hero-row">
            <div class="prediction-icon">{icon}</div>
            <div>
                <div class="prediction-label">{prediction}</div>
                <div class="prediction-status">{status}</div>
            </div>
        </div>

        <div class="risk-section">
            <div class="risk-header">Risk Score</div>
            <progress class="risk-progress" value="{probability}" max="100"></progress>
            <div class="risk-value">{probability:.2f}%</div>
        </div>

        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">📊 Probability</div>
                <div class="stat-value">{probability:.2f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">🔥 Confidence</div>
                <div class="stat-value" style="color:#38bdf8;">{confidence}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">💼 Status</div>
                <div class="stat-value" style="color:{accent};">{status}</div>
            </div>
        </div>

        <div class="recommendation-box">
            <div class="recommendation-title">💡 Recommendation</div>
            <p class="recommendation">{recommendation}</p>
        </div>
    </div>
    """
    components.html(html, height=720, scrolling=False)


def main() -> None:
    render_css()
    render_header()

    with st.form("customer_churn_form"):
        request_data = build_request_payload()
        st.divider()
        submitted = st.form_submit_button("🚀 Predict Churn", use_container_width=True)

    if submitted:
        try:
            with st.spinner("Predicting customer churn..."):
                result = predict_customer(request_data)
            render_result(result)
        except Exception as exc:
            st.error(str(exc))


if __name__ == "__main__":
    main()