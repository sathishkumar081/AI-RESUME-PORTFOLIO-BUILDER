import openai
from fpdf import FPDF
from jinja2 import Template

def generate_resume_text(student_data):
    prompt = f"""
    Create an ATS-friendly professional resume using the following data.
    Emphasize skills, projects, internships, and achievements.

    Student Data:
    {student_data}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def create_resume_pdf(resume_text, output_file="resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    for line in resume_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output(output_file)
