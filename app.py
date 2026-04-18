import streamlit as st
import sqlite3
from PyPDF2 import PdfReader
import pandas as pd

# -----------------------------
# DATABASE
# -----------------------------
def connect_db():
    return sqlite3.connect("jobs.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        salary TEXT,
        link TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

# -----------------------------
# UI CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Assistant", layout="wide")

st.title("💼 AI Career Assistant - India Job Market")

st.markdown("""
### 🚀 Smart Career Platform
✔ Job Search Dashboard  
✔ Resume Analyzer  
✔ Company Insights  
✔ Job Tracker System  
✔ Export Feature  
""")

# -----------------------------
# VALIDATION
# -----------------------------
def validate_input(text):
    return text is not None and text.strip() != ""

# -----------------------------
# SAMPLE JOBS
# -----------------------------
jobs_data = [
    {"title": "Software Engineer", "company": "TCS", "location": "Bangalore", "salary": 4, "skills": ["python", "sql"], "wfh": True, "notice": 30},
    {"title": "Data Analyst", "company": "Infosys", "location": "Mumbai", "salary": 5, "skills": ["python", "excel"], "wfh": False, "notice": 60},
    {"title": "Web Developer", "company": "Wipro", "location": "Delhi", "salary": 3, "skills": ["html", "css"], "wfh": True, "notice": 30},
    {"title": "AI Engineer", "company": "Google", "location": "Bangalore", "salary": 10, "skills": ["python", "ml"], "wfh": True, "notice": 90},
]

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

location = st.sidebar.selectbox("Location", ["All", "Bangalore", "Mumbai", "Delhi"])
salary = st.sidebar.selectbox("Salary", ["All", "0-3", "3-6", "6+"])
wfh = st.sidebar.checkbox("Work From Home")
notice = st.sidebar.selectbox("Notice Period", ["All", "30", "60", "90"])

# -----------------------------
# SKILLS INPUT
# -----------------------------
st.subheader("📄 Enter Your Skills")

skills_input = st.text_input("Enter skills (comma separated)")

if not validate_input(skills_input):
    st.warning("Enter skills for better recommendations")

user_skills = [s.strip().lower() for s in skills_input.split(",")] if skills_input else []

# -----------------------------
# JOB FILTER FUNCTION
# -----------------------------
def filter_jobs(jobs):
    result = []

    for job in jobs:

        if location != "All" and job["location"] != location:
            continue

        if salary == "0-3" and job["salary"] > 3:
            continue
        elif salary == "3-6" and (job["salary"] < 3 or job["salary"] > 6):
            continue
        elif salary == "6+" and job["salary"] < 6:
            continue

        if wfh and not job["wfh"]:
            continue

        if notice != "All" and job["notice"] != int(notice):
            continue

        match = sum(1 for s in user_skills if s in job["skills"])
        job["match"] = match

        result.append(job)

    return sorted(result, key=lambda x: x["match"], reverse=True)

jobs = filter_jobs(jobs_data)

# -----------------------------
# DASHBOARD UI
# -----------------------------
st.subheader("📋 Job Dashboard")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Available Jobs")

with col2:
    st.write("### Resume Insights")

# -----------------------------
# JOB DISPLAY
# -----------------------------
for i, job in enumerate(jobs):
    st.markdown(f"### 💼 {job['title']}")
    st.write(f"🏢 {job['company']} | 📍 {job['location']} | 💰 {job['salary']} LPA")
    st.write(f"🧠 Match Score: {job.get('match', 0)}")

    if st.button("💾 Save Job", key=i):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO jobs (title, company, location, salary, link)
        VALUES (?, ?, ?, ?, ?)
        """, (job['title'], job['company'], job['location'], str(job['salary']), ""))
        conn.commit()
        conn.close()
        st.success("Job Saved!")

    st.markdown("---")

# -----------------------------
# EXPORT FEATURE
# -----------------------------
if jobs:
    df = pd.DataFrame(jobs)
    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Jobs CSV",
        csv,
        "jobs.csv",
        "text/csv"
    )

# -----------------------------
# RESUME ANALYSIS
# -----------------------------
st.subheader("📄 Resume Analysis")

file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

if file is None:
    st.warning("Please upload a resume file")

if file:
    text = ""

    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        else:
            text = file.read().decode("utf-8")
    except:
        st.error("Invalid file")

    text = text.lower()

    keywords = ["python", "sql", "ml", "excel", "java", "html", "css", "javascript"]

    found = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]

    st.write("✅ Found:", found)
    st.write("❌ Missing:", missing)

    score = int((len(found) / len(keywords)) * 100)
    score = min(max(score, 0), 100)

    st.metric("Resume Score", f"{score}/100")

# -----------------------------
# COMPANY INSIGHTS
# -----------------------------
st.subheader("🏢 Company Insights")

company = st.text_input("Enter Company Name")

if company:
    st.info(f"Insights for {company}")
    st.write("✔ Average Salary: 6–12 LPA")
    st.write("✔ Work Culture: Hybrid")
    st.write("✔ Rating: 4.2/5")
    st.write("✔ Hiring Status: Active")

# -----------------------------
# SAVED JOBS (TRACKING CARDS)
# -----------------------------
st.subheader("⭐ Saved Jobs")

conn = connect_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM jobs")
saved_jobs = cursor.fetchall()
conn.close()

for job in saved_jobs:
    with st.container():
        st.markdown(f"### 💼 {job[1]}")
        st.write(f"🏢 {job[2]} | 📍 {job[3]} | 💰 {job[4]} LPA")
        st.markdown("---")