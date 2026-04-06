# utils/resume_parser.py

def parse_resume(text):
    """
    Simple resume parser: extract skills from resume text
    """
    skills = []

    if "python" in text.lower():
        skills.append("Python")
    if "java" in text.lower():
        skills.append("Java")
    if "sql" in text.lower():
        skills.append("SQL")

    return skills