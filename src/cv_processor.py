import PyPDF2
import docx
import re
import os
from src.preprocess import clean_text

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return clean_text(text)

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return clean_text(text)

def analyze_cv(text: str) -> dict:
    """Analyze CV text and provide insights"""
    analysis = {
        "length": len(text.split()),
        "keywords": [],
        "recommendations": []
    }

    # Expanded keyword list
    keywords = [
        "experience", "skills", "education", "projects", "certifications", "languages",
        "خبرة", "مهارات", "تعليم", "مشاريع", "شهادات", "لغات",
        "leadership", "communication", "teamwork", "problem solving", "analytical",
        "microsoft office", "excel", "word", "powerpoint", "python", "java", "javascript",
        "data analysis", "project management", "customer service", "sales", "marketing",
        "research", "development", "engineering", "design", "writing", "editing"
    ]
    for kw in keywords:
        if kw.lower() in text.lower():
            analysis["keywords"].append(kw)

    # Recommendations
    if analysis["length"] < 200:
        analysis["recommendations"].append("Add more details about your experiences and skills to reach optimal length.")
    elif analysis["length"] > 800:
        analysis["recommendations"].append("Consider condensing your CV to focus on the most relevant information.")
    if len(analysis["keywords"]) < 10:
        analysis["recommendations"].append("Incorporate more industry-specific keywords.")
    if not ("education" in text.lower() or "تعليم" in text):
        analysis["recommendations"].append("Include an education section.")
    if not ("experience" in text.lower() or "خبرة" in text):
        analysis["recommendations"].append("Include a work experience section.")
    if not ("skills" in text.lower() or "مهارات" in text):
        analysis["recommendations"].append("Include a skills section.")

    return analysis

def process_cv_file(file_path: str) -> dict:
    """Process uploaded CV file and return analysis"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type. Please upload PDF or DOCX."}

    analysis = analyze_cv(text)
    analysis["extracted_text"] = text[:500]  # First 500 chars for context
    return analysis
