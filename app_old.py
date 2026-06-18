import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
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
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer
    return buffer

st.title("🏥 AI Medical Report Simplifier")

st.markdown("""
### 📄 Upload your medical report and get:

✅ Easy-to-understand explanations  
✅ Abnormal values highlighted  
✅ Diet recommendations  
✅ Lifestyle suggestions  
✅ Questions to ask your doctor
""")

uploaded_file = st.file_uploader(
    "Upload your medical report PDF",
    type=["pdf"]
)

if uploaded_file:
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    st.success("✅ PDF uploaded successfully!")

    with st.expander("📄 View Extracted Text (Optional)"):
        st.text_area("Report Content", text, height=300)
        if st.button("Simplify Report"):
            prompt = f"""
            
        You are an AI Medical Report Simplifier.

        Explain this medical report in very simple English.

        Report:
        {text}

        Give the answer in this exact format:

        1. Summary
        Explain the overall report in simple words.

        2. Abnormal Values
        List only abnormal or important values.

        3. What It Means
        Explain what those abnormal values may indicate.

        4. Precautions
        Give simple health precautions.

        5. Diet Suggestions
        Give food suggestions.

        6. Lifestyle Suggestions
        Give daily life suggestions.

        7. Questions to Ask Doctor
        Give 5 questions the patient should ask the doctor.

        Important Rules:

        Use Markdown headings.

        Format your answer exactly like this:

        ## Summary

        ## Abnormal Values

        ## What It Means

        ## Precautions

        ## Diet Suggestions

        ## Lifestyle Suggestions

        ## Questions to Ask Your Doctor
        ## Health Score (VERY IMPORTANT)

        At the end of your response, you MUST include:

        Overall Health Score: __ / 100

        Risk Level:
        🟢 Healthy
        🟡 Needs Attention
        🔴 Critical

        Choose ONLY ONE risk level based on the medical report.
        Use bullet points wherever possible.

        At the end, write:

            ⚠️ This explanation is for educational purposes only. Please consult a qualified doctor.
            """

                response = model.generate_content(prompt)

                st.subheader("AI Explanation")
            st.write(response.text)
            st.success("✅ Report simplified successfully!")
            st.markdown("---")

            pdf_file = create_pdf(response.text)

            st.download_button(
                label="📥 Download Simplified Report as PDF",
                data=pdf_file,
                file_name="simplified_medical_report.pdf",
                mime="application/pdf",
            )
    
