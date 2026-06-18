# AI Medical Report Simplifier

## Project Overview
The AI Medical Report Simplifier is a Generative AI application that helps patients understand complex medical reports. Users can upload a medical report, and the application generates a simple explanation, provides a health score, and allows downloading the explanation as a PDF.

## Problem Statement
Medical reports often contain technical terminology that is difficult for patients to understand. This project converts those reports into simple language using Generative AI.

## Objectives
- Upload medical reports.
- Extract text from PDF files.
- Simplify medical terminology.
- Generate a health score.
- Download the simplified report as a PDF.

## Features
- PDF Upload
- AI-based Report Simplification
- Health Score Generation
- PDF Download
- Easy-to-use Streamlit Interface

## Technologies Used
- Python
- Streamlit
- Google Gemini API
- PyPDF2
- ReportLab
- python-dotenv

## Project Structure
```
Medical_Report_Simplifier/
│
├── app.py
├── README.md
├── requirements.txt
├── .env
├── backend/
└── venv/
```

## Installation
1. Install Python.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Add your Gemini API Key to the `.env` file.
4. Run the project:
   ```
   streamlit run app.py
   ```

## Future Scope
- Multi-language support
- Disease risk prediction
- Voice explanation
- Medical chatbot
- Graphical analysis of reports

## Author
Mukesh