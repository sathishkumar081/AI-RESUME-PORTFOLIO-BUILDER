from google import genai

def generate_cover_letter(student_data: str, job_description: str, client, model: str) -> str:
    if not student_data.strip() or not job_description.strip():
        return "Error: Missing student data or job description."

    prompt = f"""
Write a professional and personalized cover letter.

Candidate Details:
{student_data}

Job Description:
{job_description}

Guidelines:
- Formal tone
- 3–4 paragraphs
- Highlight skills matching the job
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Cover Letter Generation Error: {e}"
