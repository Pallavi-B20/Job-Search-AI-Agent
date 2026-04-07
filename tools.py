# tools.py

import PyPDF2

# -----------------------------
# FORMAT JOB LISTINGS
# -----------------------------
def format_job_listings(jobs):
    if not jobs:
        return "No jobs found."

    output = ""
    for job in jobs:
        output += f"🔹 {job.get('title', 'N/A')}\n"
        output += f"   🏢 Company: {job.get('company', 'N/A')}\n"
        output += f"   📍 Location: {job.get('location', 'N/A')}\n"
        output += "-" * 40 + "\n"

    return output


# -----------------------------
# EXTRACT TEXT FROM PDF RESUME
# -----------------------------
def extract_text_from_pdf(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    
    return text


# -----------------------------
# EXTRACT SKILLS FROM TEXT
# -----------------------------
def extract_skills(text):
    keywords = ["python", "sql", "ml", "excel", "java", "c++", "html", "css", "javascript"]

    text = text.lower()
    found = [skill for skill in keywords if skill in text]
    missing = [skill for skill in keywords if skill not in text]

    return found, missing, keywords


# -----------------------------
# CALCULATE ATS SCORE
# -----------------------------
def calculate_score(found, total_keywords):
    if not total_keywords:
        return 0
    return min(100, int((len(found) / len(total_keywords)) * 100))


# -----------------------------
# LEARNING RECOMMENDATIONS
# -----------------------------
def learning_recommendations(missing_skills):
    recommendations = []
    for skill in missing_skills:
        recommendations.append(f"👉 Learn {skill} to improve your resume")
    return recommendations