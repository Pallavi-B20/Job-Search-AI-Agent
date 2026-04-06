import streamlit as st
import sqlite3
import PyPDF2

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
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="AI Job Agent", layout="wide")
st.title("💼 AI Job Search & Resume Assistant")

# -----------------------------
# JOB DATA
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
salary = st.sidebar.selectbox("Salary (LPA)", ["All", "0-3", "3-6", "6+"])
wfh = st.sidebar.checkbox("Work From Home")
notice = st.sidebar.selectbox("Notice Period", ["All", "30", "60", "90"])

# -----------------------------
# SKILLS INPUT
# -----------------------------
st.subheader("📄 Enter Your Skills")

skills_input = st.text_input("Enter skills (Python, SQL, etc):")

if skills_input.strip():
    user_skills = [s.strip().lower() for s in skills_input.split(",")]
else:
    user_skills = []

# -----------------------------
# FILTER FUNCTION
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

        # Match logic
        if not user_skills:
            match = 0
        else:
            match = sum(1 for s in user_skills if s in job["skills"])

        job["match"] = match
        result.append(job)

    return sorted(result, key=lambda x: x["match"], reverse=True)

jobs = filter_jobs(jobs_data)

# -----------------------------
# JOB TITLE DISPLAY
# -----------------------------
if user_skills:
    st.subheader("🎯 Recommended Jobs")
else:
    st.subheader("📋 All Jobs")
    st.info("Showing all jobs. Enter skills to get better matches.")

# -----------------------------
# DISPLAY JOBS
# -----------------------------
if jobs:
    for i, job in enumerate(jobs):
        st.write(f"### {job['title']}")
        st.write(f"🏢 {job['company']}")
        st.write(f"📍 {job['location']}")
        st.write(f"💰 {job['salary']} LPA")

        if job["match"] > 0:
            st.success(f"🧠 Match Score: {job['match']}")
        else:
            st.write(f"🧠 Match Score: {job['match']}")

        st.write("🏆 Benefits: Health insurance, Flexible work")

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
else:
    st.warning("No jobs found")

# -----------------------------
# RESUME ANALYSIS
# -----------------------------
st.subheader("📄 Resume Analysis")

file = st.file_uploader("Upload Resume (txt or pdf)", type=["txt", "pdf"])

if file:
    text = ""

    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
    else:
        text = file.read().decode("utf-8")

    text = text.lower()

    st.write("Resume Preview:", text[:200])

    keywords = ["python", "sql", "ml", "excel", "java", "c++", "html", "css", "javascript"]

    found = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]

    st.write("✅ Skills Found:", found)
    st.write("❌ Missing Skills:", missing)

    score = len(found) * 25
    st.write(f"🎯 Resume Score: {score}/100")

    if score < 50:
        st.warning("⚠ Improve your skills to get better jobs")
    else:
        st.success("✅ Good resume!")

# -----------------------------
# SAVED JOBS
# -----------------------------
st.subheader("⭐ Saved Jobs")

conn = connect_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM jobs")
saved_jobs = cursor.fetchall()
conn.close()

if saved_jobs:
    for job in saved_jobs:
        st.write(f"### {job[1]}")
        st.write(f"🏢 {job[2]} | 📍 {job[3]} | 💰 {job[4]}")
        st.markdown("---")
else:
    st.info("No saved jobs yet")