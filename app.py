import streamlit as st
from agent import JobSearchAgent
from tools import format_job_listings
import PyPDF2

st.set_page_config(page_title="Job Search AI", layout="wide")
st.title("💼 Comprehensive Job Search AI Assistant")

agent = JobSearchAgent()

# -----------------------------
# CHAT SECTION
# -----------------------------
st.header("💬 Chat with AI")
user_question = st.text_input("Ask AI about career, resume, or jobs")
if user_question:
    with st.spinner("AI is thinking..."):
        answer = agent.chat_with_agent(user_question)
    st.success(answer)

# -----------------------------
# JOB SEARCH SECTION
# -----------------------------
st.header("🔍 Search Jobs")
keyword = st.text_input("Job Title / Keyword", key="keyword")
location = st.text_input("Location (Optional)", key="location")
experience = st.text_input("Experience Filter (Optional, e.g., 1-3 yrs)", key="experience")
skills = st.text_input("Your Skills (comma separated)", key="skills")
resume_file = st.file_uploader("Upload your resume (PDF) for matching", type=["pdf"])

if st.button("Search & Match Jobs"):
    with st.spinner("Fetching jobs..."):
        jobs = agent.search_jobs(keyword, location, experience)
        st.subheader("📋 All Jobs Found")
        st.text(format_job_listings(jobs))

        # -----------------------------
        # RESUME ANALYSIS (WEEK 5)
        # -----------------------------
        if resume_file:
            st.subheader("📄 Resume Analysis")

            # Extract text
            pdf_reader = PyPDF2.PdfReader(resume_file)
            resume_text = ""
            for page in pdf_reader.pages:
                if page.extract_text():
                    resume_text += page.extract_text()

            resume_text = resume_text.lower()

            st.write("Preview:", resume_text[:300])

            # ATS KEYWORDS
            keywords = ["python", "sql", "ml", "excel", "java", "c++", "html", "css", "javascript"]

            found = [k for k in keywords if k in resume_text]
            missing = [k for k in keywords if k not in resume_text]

            st.write("✅ Skills Found:", found)
            st.write("❌ Missing Skills:", missing)

            # -----------------------------
            # SKILL GAP + LEARNING (WEEK 6)
            # -----------------------------
            st.subheader("📚 Learning Recommendations")
            for skill in missing:
                st.write(f"👉 Learn {skill} to improve your resume")

            # -----------------------------
            # ATS SCORE (OUT OF 100)
            # -----------------------------
            score = min(100, int((len(found) / len(keywords)) * 100))
            st.write(f"🎯 Resume Score: {score}/100")

            if score < 40:
                st.error("❌ Poor resume")
            elif score < 70:
                st.warning("⚠ Average resume")
            else:
                st.success("✅ Strong resume")

        # -----------------------------
        # SKILL MATCHING
        # -----------------------------
        if skills:
            skill_list = [s.strip() for s in skills.split(",")]
            matched_jobs = agent.match_jobs(jobs, skill_list)
            st.subheader("🎯 Jobs Matching Your Skills")
            st.text(format_job_listings(matched_jobs))

# -----------------------------
# COMPANY INFO SECTION
# -----------------------------
st.header("🏢 Company Lookup")
company_name = st.text_input("Enter Company Name for Info")
if company_name and st.button("Lookup Company Info"):
    info = agent.company_info(company_name)
    st.info(info)

# -----------------------------
# LINKEDIN FEATURE (WEEK 6)
# -----------------------------
st.header("🔗 LinkedIn Profile")

linkedin_url = st.text_input("Paste your LinkedIn profile link")

st.write("💡 Enter your LinkedIn profile to get suggestions")

if linkedin_url:
    if "linkedin.com" in linkedin_url:
        st.success("✅ Valid LinkedIn profile!")
        st.markdown(f"[🔗 Open Profile]({linkedin_url})")

        st.subheader("📈 Profile Improvement Tips")
        st.write("✔ Add professional profile photo")
        st.write("✔ Write strong headline")
        st.write("✔ Add skills & projects")
        st.write("✔ Keep profile updated")
    else:
        st.warning("⚠ Please enter a valid LinkedIn link")