import streamlit as st
from resume_parser import parse_resume
from job_matcher import match_jobs
from company_info import get_company_info

st.title("💼 Job Search AI Assistant")

# -------- WEEK 1-2 (OLD FEATURE) --------
st.header("🔍 Job Search")

role = st.text_input("Enter Job Role")
location = st.text_input("Enter Location")

if st.button("Search Jobs"):
    st.write(f"Showing jobs for {role} in {location}")

# -------- WEEK 3-4 (NEW FEATURES) --------
st.header("📄 Resume Analysis")

resume_text = st.text_area("Paste your resume here")

if st.button("Analyze Resume"):
    skills = parse_resume(resume_text)
    st.write("### Skills Found:", skills)

    jobs = match_jobs(skills)
    st.write("### Matching Jobs:", jobs)

# -------- COMPANY INFO --------
st.header("🏢 Company Info")

company = st.text_input("Enter company name")

if company:
    info = get_company_info(company)
    st.write("### Company Details:", info)