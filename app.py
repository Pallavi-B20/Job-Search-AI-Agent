import streamlit as st
from utils.resume_parser import parse_resume
from utils.matcher import match_jobs
from utils.company_info import get_company_info
# Title
st.title("💼 Job Search AI Assistant")
st.write("Showing best available jobs for you 🚀")

# -------------------------------
# 🔍 WEEK 1–2: JOB SEARCH
# -------------------------------
st.header("🔍 Job Search")

role = st.text_input("Enter Job Role")
location = st.text_input("Enter Location")

if st.button("Search Jobs"):
    if role and location:
        st.success(f"Showing jobs for '{role}' in '{location}'")
    else:
        st.warning("Please enter both role and location")

# -------------------------------
# 📄 WEEK 3–4: RESUME ANALYSIS
# -------------------------------
st.header("📄 Resume Analysis")

resume_text = st.text_area("Paste your resume here")

if st.button("Analyze Resume"):
    if resume_text:
        skills = parse_resume(resume_text)
        st.write("### ✅ Skills Found:", skills)

        jobs = match_jobs(skills)
        st.write("### 💼 Matching Jobs:", jobs)
    else:
        st.warning("Please enter resume text")

# -------------------------------
# 🏢 COMPANY INFO
# -------------------------------
st.header("🏢 Company Info")

company = st.text_input("Enter company name")

if st.button("Get Company Info"):
    if company:
        info = get_company_info(company)
        st.write("### 📊 Company Details:", info)
    else:
        st.warning("Please enter company name")