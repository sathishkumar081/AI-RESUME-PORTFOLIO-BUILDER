from google import genai

def generate_resume(student_data: str, client, model: str) -> str:
    if not student_data.strip():
        return "Error: Student data is empty."

    prompt = f"""
You are a professional resume writer.

Create an ATS-friendly resume.
Use clear headings and bullet points.
Avoid tables, icons, emojis, or graphics.

Student Information:
{student_data}
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Resume Generation Error: {e}"
