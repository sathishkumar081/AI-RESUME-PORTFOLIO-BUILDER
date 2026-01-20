import openai

def generate_cover_letter(student_data, job_role, company):
    prompt = f"""
    Write a professional, personalized cover letter.

    Job Role: {job_role}
    Company: {company}

    Candidate Information:
    {student_data}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
