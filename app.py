import streamlit as st
from chatbot import chat

st.title("💼 Job Search AI Assistant")
st.success("Showing best available jobs for you 🚀")
role = st.text_input("Enter Job Role", "developer")
location = st.text_input("Enter Location")

if st.button("Search Jobs"):
    results = chat(role, location)

    for job in results:
        st.write("👉", job)