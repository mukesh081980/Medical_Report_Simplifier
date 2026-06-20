import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# API KEY SETUP
# -----------------------------
load_dotenv()

api_key = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY", None)
except Exception:
    api_key = None

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Add it in Streamlit Secrets or .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# PDF GENERATOR
# -----------------------------
def create_pdf(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Medical Report Simplifier", styles["Title"]))
    story.append(Spacer(1, 12))

    for line in report_text.split("\n"):
        line = line.replace("##", "")
        line = line.replace("**", "")
        line = line.replace("*", "•")
        line = escape(line)

        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🏥 Medical Report Simplifier")

st.sidebar.markdown("""
### About Project
This project uses Generative AI to simplify complex medical reports into easy English.

### How to Use
1. Fill patient details
2. Upload a medical report PDF
3. Click Simplify Report
4. Download the summary

### Developed By
Mukesh
""")


# -----------------------------
# MAIN UI
# -----------------------------
st.title("🏥 AI Medical Report Simplifier")

st.info(
    "⚠️ Disclaimer: This AI-generated explanation is for educational purposes only. "
    "Always consult a qualified doctor before making any medical decisions."
)

st.markdown("""
### 📄 Upload your medical report and get:

✅ Easy-to-understand explanations  
✅ Abnormal values highlighted  
✅ Diet recommendations  
✅ Lifestyle suggestions  
✅ Questions to ask your doctor  
✅ Health score  
✅ Emergency warning  
✅ Medicine explanation  
✅ Chat with report  
""")

# -----------------------------
# PATIENT DETAILS
# -----------------------------
st.markdown("### 👤 Patient Details")

patient_name = st.text_input("Patient Name")
patient_age = st.number_input("Age", min_value=1, max_value=120, step=1, value=30)
patient_gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
report_date = st.date_input("Report Date")
hospital_name = st.text_input("Hospital / Lab Name")

# -----------------------------
# BMI
# -----------------------------
st.markdown("### ⚖️ BMI Calculator")

height_cm = st.number_input("Height (cm)", min_value=50, max_value=250, step=1, value=170)
weight_kg = st.number_input("Weight (kg)", min_value=10, max_value=300, step=1, value=70)

bmi = weight_kg / ((height_cm / 100) ** 2)

st.info(f"Your BMI is: {bmi:.2f}")

if bmi < 18.5:
    st.warning("BMI Category: Underweight")
elif bmi < 25:
    st.success("BMI Category: Normal")
elif bmi < 30:
    st.warning("BMI Category: Overweight")
else:
    st.error("BMI Category: Obese")

# -----------------------------
# EXTRA PATIENT INFO
# -----------------------------
st.markdown("### 🩺 Additional Patient Information")

blood_group = st.selectbox(
    "Blood Group",
    ["Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
)

emergency_contact = st.text_input(
    "Emergency Contact Number",
    placeholder="Enter emergency contact number"
)

allergies = st.text_area(
    "Known Allergies",
    placeholder="Example: Penicillin, Peanuts, Dust allergy..."
)

medical_history = st.text_area(
    "Previous Medical Conditions",
    placeholder="Example: Diabetes, Hypertension, Asthma..."
)

current_medications = st.text_area(
    "Current Medications",
    placeholder="Example: Paracetamol, Metformin, Jalra-M..."
)

past_surgeries = st.text_area(
    "Past Surgeries",
    placeholder="Example: Appendix surgery in 2021"
)

family_history = st.text_area(
    "Family Medical History",
    placeholder="Example: Father has diabetes, Mother has hypertension..."
)

# -----------------------------
# LIFESTYLE
# -----------------------------
st.markdown("### 🏃 Lifestyle Information")

smoking = st.selectbox("Do you smoke?", ["No", "Occasionally", "Regularly"])
alcohol = st.selectbox("Do you consume alcohol?", ["No", "Occasionally", "Regularly"])
exercise = st.selectbox(
    "Exercise Frequency",
    ["Daily", "3-5 times/week", "1-2 times/week", "Rarely", "Never"]
)
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Mixed"])
sleep_hours = st.slider("Average Sleep (hours/day)", 1, 12, 7)
water_intake = st.slider("Average Water Intake (Litres/day)", 1, 10, 3)
stress_level = st.slider("Stress Level", 1, 10, 5)

# -----------------------------
# VITALS
# -----------------------------
st.markdown("### ❤️ Vital Signs")

blood_pressure = st.text_input("Blood Pressure", placeholder="Example: 120/80 mmHg")
heart_rate = st.number_input("Heart Rate (BPM)", min_value=30, max_value=200, value=72)
body_temperature = st.number_input(
    "Body Temperature (°C)",
    min_value=30.0,
    max_value=45.0,
    value=36.5,
    step=0.1
)
oxygen_level = st.slider("Oxygen Saturation (SpO₂ %)", 70, 100, 98)

# -----------------------------
# HEALTH GOAL
# -----------------------------
st.markdown("### 🎯 Health Goals")

health_goal = st.selectbox(
    "Primary Health Goal",
    [
        "General Health Checkup",
        "Weight Loss",
        "Weight Gain",
        "Control Diabetes",
        "Control Blood Pressure",
        "Improve Heart Health",
        "Improve Fitness",
        "Other",
    ],
)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload your medical report PDF", type=["pdf"])

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    st.success("✅ PDF uploaded successfully!")

    with st.expander("📄 View Extracted Text (Optional)"):
        st.text_area("Report Content", text, height=300)

    if st.button("Simplify Report"):
        if not patient_name or patient_gender == "Select" or not hospital_name:
            st.warning("Please fill Patient Name, Gender, and Hospital/Lab Name before simplifying.")
            st.stop()

        # Limit PDF text to avoid Gemini timeout
        text = text[:12000]

        prompt = f"""
You are an AI Medical Report Simplifier.

Patient Information:
Name: {patient_name}
Age: {patient_age}
Gender: {patient_gender}
Report Date: {report_date}
Hospital/Lab: {hospital_name}
Blood Group: {blood_group}
BMI: {bmi:.2f}
Allergies: {allergies}
Medical History: {medical_history}
Current Medications: {current_medications}
Past Surgeries: {past_surgeries}
Family Medical History: {family_history}
Emergency Contact: {emergency_contact}
Health Goal: {health_goal}

Lifestyle:
Smoking: {smoking}
Alcohol: {alcohol}
Exercise: {exercise}
Diet: {diet}
Sleep Hours: {sleep_hours}
Water Intake: {water_intake} litres/day
Stress Level: {stress_level}/10

Vital Signs:
Blood Pressure: {blood_pressure}
Heart Rate: {heart_rate}
Body Temperature: {body_temperature}
Oxygen Level: {oxygen_level}%

Medical Report Text:
{text}

Give the answer in this exact format:

## Simple Summary
Explain the report in very simple English.

## Abnormal Values
List abnormal or important values.

## What It Means
Explain possible meaning.

## Health Risk Assessment
Mention risk level: Healthy / Needs Attention / Critical.

## Diet Suggestions
Give personalized diet suggestions.

## Lifestyle Suggestions
Give suggestions based on smoking, alcohol, exercise, sleep, water intake, stress.

## Questions to Ask Doctor
Give 5 questions.

## Health Score
Give overall health score out of 100 in this exact format:
Health Score: 65/100

At the end write:
⚠️ This explanation is for educational purposes only.
"""

        try:
            with st.spinner("⏳ Analyzing your medical report..."):
                response = model.generate_content(prompt)
                report_text = response.text

        except Exception as e:
            st.error(f"Gemini Error: {e}")
            st.stop()

        st.subheader("AI Explanation")
        st.write(report_text)

        # -----------------------------
        # HEALTH SCORE
        # -----------------------------
        match = re.search(r"Health Score:\s*(\d+)", report_text, re.IGNORECASE)

        if match:
            health_score = int(match.group(1))
            health_score = max(0, min(100, health_score))

            st.subheader("📊 Health Score")
            st.write(f"Health Score: {health_score}/100")
            st.progress(health_score / 100)

            if health_score >= 80:
                st.success("🟢 Excellent Health")
            elif health_score >= 60:
                st.warning("🟡 Moderate Health")
            else:
                st.error("🔴 Poor Health")
        else:
            st.warning("Health score was not found in the AI response.")

        # -----------------------------
        # EMERGENCY WARNING
        # -----------------------------
        emergency_words = [
            "critical",
            "emergency",
            "urgent",
            "heart attack",
            "stroke",
            "cancer",
            "icu",
            "severe",
            "immediate",
            "danger",
            "high risk",
        ]

        report_lower = report_text.lower()

        if any(word in report_lower for word in emergency_words):
            st.error(
                "🚨 Emergency Warning: This report may contain serious findings. "
                "Please consult a doctor immediately."
            )
        else:
            st.success("✅ No emergency warning detected.")

        # -----------------------------
        # MEDICINE EXPLANATION
        # -----------------------------
        if current_medications.strip():
            st.subheader("💊 Medicine Explanation")

            medicine_prompt = f"""
Explain these medicines in simple English:

Medicines: {current_medications}

For each medicine, explain:
1. Purpose
2. Common side effects
3. Precautions

Keep it short and simple.
"""

            try:
                with st.spinner("💊 Explaining medicines..."):
                    medicine_response = model.generate_content(medicine_prompt)
                st.write(medicine_response.text)

            except Exception as e:
                st.warning(f"Medicine explanation could not be generated: {e}")

        # -----------------------------
        # DOWNLOADS
        # -----------------------------
        st.success("✅ Report simplified successfully!")

        st.download_button(
            label="📥 Download AI Report",
            data=report_text,
            file_name="Medical_Report_Summary.txt",
            mime="text/plain",
        )

        st.markdown("---")

        pdf_file = create_pdf(report_text)

        st.download_button(
            label="📥 Download Simplified Report as PDF",
            data=pdf_file,
            file_name="simplified_medical_report.pdf",
            mime="application/pdf",
        )

        st.session_state["latest_report_text"] = report_text


# -----------------------------
# CHAT WITH REPORT
# -----------------------------
if "latest_report_text" in st.session_state:
    st.markdown("---")
    st.subheader("💬 Chat with Your Medical Report")

    user_question = st.text_input("Ask a question about your report")

    if user_question:
        chat_prompt = f"""
You are a medical report assistant.

Answer the user's question using only this report explanation:

Report Explanation:
{st.session_state["latest_report_text"][:8000]}

User Question:
{user_question}

Give a simple and safe answer.
Add: Please consult a doctor for medical decisions.
"""

        try:
            with st.spinner("💬 Answering your question..."):
                chat_response = model.generate_content(chat_prompt)

            st.write(chat_response.text)

        except Exception as e:
            st.error(f"Chat Error: {e}")
