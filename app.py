import streamlit as st
import os
from dotenv import load_dotenv
from resume_generator import generate_resume_text, create_resume_pdf
from cover_letter_generator import generate_cover_letter
from portfolio_generator import generate_portfolio

load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Resume & Portfolio Builder", layout="wide")

st.title("AI Resume & Portfolio Builder")

with st.form("student_form"):
    name = st.text_input("Full Name")
    summary = st.text_area("Professional Summary")
    skills = st.text_area("Skills (comma-separated)")
    projects = st.text_area("Projects (Title: Description)")
    job_role = st.text_input("Target Job Role")
    company = st.text_input("Target Company")

    submitted = st.form_submit_button("Generate")

if submitted:
    student_data = {
        "name": name,
        "summary": summary,
        "skills": skills.split(","),
        "projects": [
            {"title": p.split(":")[0], "description": p.split(":")[1], "tech": "Various"}
            for p in projects.split("\n") if ":" in p
        ]
    }

    st.subheader("📄 Resume")
    resume_text = generate_resume_text(student_data)
    st.text(resume_text)
    create_resume_pdf(resume_text)
    st.download_button("Download Resume PDF", open("resume.pdf", "rb"), "resume.pdf")

    st.subheader("✉️ Cover Letter")
    cover_letter = generate_cover_letter(student_data, job_role, company)
    st.text(cover_letter)

    st.subheader("🌐 Portfolio")
    portfolio_html = generate_portfolio(student_data)
    st.components.v1.html(portfolio_html, height=600)
