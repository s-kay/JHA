import openai
import requests

BACKEND_URL = "http://localhost:8000/generate-cover-letter"

def generate_cover_letter(resume_text, job_description):
    try:
        response = requests.post(BACKEND_URL, json={
            "resume": resume_text,
            "job_description": job_description
        })
        response.raise_for_status()
        return response.json().get("cover_letter", "No content returned.")
    except requests.exceptions.RequestException as e:
        return f"Error contacting backend: {str(e)}"


def tailor_resume(resume_text: str, job_description: str):
    prompt = f"""
    You are an expert resume optimizer. Given the resume and job description below,
    rewrite the resume to highlight relevant experiences, skills, and achievements
    that align with the job.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Tailor it professionally and preserve formatting as much as possible.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content
