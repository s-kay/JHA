import openai
import streamlit as st

# Load your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_cover_letter(resume_text, job_description, tone="Professional"):
    prompt = f"""
    You are a job application assistant. Given the resume and job description below,
    write a short, {tone.lower()} cover letter that highlights the candidate's most relevant skills.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
