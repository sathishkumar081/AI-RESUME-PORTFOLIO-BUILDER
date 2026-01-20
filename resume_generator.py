%%writefile app.py
import os
import gradio as gr
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer

# ---------------- CONFIG ---------------- #

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-1.5-flash"   # WORKING MODEL

# ---------------- CORE FUNCTIONS ---------------- #

def generate_resume(student_data):
    if not student_data.strip():
        return "Error: Student data is empty."

    prompt = f"""
You are a professional resume writer.

Generate an ATS-friendly resume.
Use clear headings and bullet points.
Avoid tables, emojis, and graphics.

Student Data:
{student_data}
"""
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Resume Generation Error: {str(e)}"


def ats_score(resume_text, job_description):
    if not resume_text.strip() or not job_description.strip():
        return "ATS Score Error: Missing input."

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([resume_text, job_description])

        similarity = (vectors[0] @ vectors[1].T).toarray()[0][0]
        return f"{round(similarity * 100, 2)}%"
    except Exception as e:
        return f"ATS Scoring Error: {str(e)}"


def run_app(student_data, job_description):
    resume = generate_resume(student_data)
    score = ats_score(resume, job_description)
    return resume, score

# ---------------- UI ---------------- #

interface = gr.Interface(
    fn=run_app,
    inputs=[
        gr.Textbox(lines=12, label="Student Details"),
        gr.Textbox(lines=12, label="Job Description")
    ],
    outputs=[
        gr.Textbox(lines=20, label="Generated ATS-Friendly Resume"),
        gr.Textbox(label="ATS Match Score")
    ],
    title="AI Resume & Portfolio Builder (Google Gemini)",
    description="ATS-optimized resume generation using Google Gemini"
)

interface.launch(share=Ture)
