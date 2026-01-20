import os
import gradio as gr
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer

from resume_generator import generate_resume
from cover_letter_generator import generate_cover_letter
from portfolio_generator import generate_portfolio

# ---------------- LOAD API KEY ---------------- #

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)

# IMPORTANT: Use fully qualified model name
MODEL = "models/gemini-1.5-flash-latest"

# ---------------- ATS SCORING ---------------- #

def ats_score(resume_text, job_description):
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([resume_text, job_description])
        score = (vectors[0] @ vectors[1].T).toarray()[0][0]
        return f"{round(score * 100, 2)}%"
    except Exception as e:
        return f"ATS Error: {e}"

# ---------------- MAIN APP ---------------- #

def run_app(student_data, job_description):
    resume = generate_resume(student_data, client, MODEL)
    cover_letter = generate_cover_letter(student_data, job_description, client, MODEL)
    portfolio = generate_portfolio(student_data)
    ats = ats_score(resume, job_description)

    return resume, cover_letter, ats, portfolio

# ---------------- UI ---------------- #

interface = gr.Interface(
    fn=run_app,
    inputs=[
        gr.Textbox(lines=12, label="Student Details"),
        gr.Textbox(lines=12, label="Job Description")
    ],
    outputs=[
        gr.Textbox(lines=20, label="Generated ATS-Friendly Resume"),
        gr.Textbox(lines=15, label="Generated Cover Letter"),
        gr.Textbox(label="ATS Match Score"),
        gr.HTML(label="Portfolio Preview")
    ],
    title="AI Resume & Portfolio Builder (Google Gemini)",
    description="Generates resumes, cover letters, portfolios, and ATS scores using Google Gemini."
)

interface.launch()
