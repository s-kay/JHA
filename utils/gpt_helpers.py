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
