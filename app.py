import streamlit as st
import PyPDF2

st.set_page_config(page_title="Job Search AI", layout="wide")
st.title("💼 Job Search AI Assistant")

# -----------------------------
# JOB DATA
# -----------------------------
jobs = [
    {"title": "Software Engineer", "company": "TCS", "location": "Bangalore"},
    {"title": "Data Analyst", "company": "Infosys", "location": "Mumbai"},
    {"title": "Web Developer", "company": "Wipro", "location": "Delhi"},
]

# -----------------------------
# JOB SEARCH
# -----------------------------
st.header("🔍 Search Jobs")

keyword = st.text_input("Enter job title")

if keyword:
    results = [job for job in jobs if keyword.lower() in job["title"].lower()]

    if results:
        for job in results:
            st.write(f"### {job['title']}")
            st.write(f"🏢 {job['company']}")
            st.write(f"📍 {job['location']}")
            st.markdown("---")
    else:
        st.warning("No jobs found")

# -----------------------------
# RESUME ANALYSIS
# -----------------------------
st.header("📄 Resume Analysis")

file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if file:
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()

    text = text.lower()

    st.write("Preview:", text[:300])

    keywords = ["python", "sql", "ml", "excel", "java", "c++"]

    found = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]

    st.write("✅ Skills Found:", found)
    st.write("❌ Missing Skills:", missing)

    # Score
    score = min(100, int((len(found) / len(keywords)) * 100))
    st.write(f"🎯 Resume Score: {score}/100")

    if score < 40:
        st.error("❌ Poor resume")
    elif score < 70:
        st.warning("⚠ Average resume")
    else:
        st.success("✅ Strong resume")

    # Learning
    st.subheader("📚 Learning Recommendations")
    for skill in missing:
        st.write(f"👉 Learn {skill}")

# -----------------------------
# LINKEDIN FEATURE
# -----------------------------
st.header("🔗 LinkedIn Profile")

linkedin = st.text_input("Enter LinkedIn URL")

if linkedin:
    if "linkedin.com" in linkedin:
        st.success("Valid LinkedIn Profile")
        st.markdown(f"[Open Profile]({linkedin})")

        st.subheader("📈 Tips")
        st.write("✔ Add profile photo")
        st.write("✔ Write strong headline")
        st.write("✔ Add projects")
    else:
        st.warning("Enter valid LinkedIn link")