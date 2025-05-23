import streamlit as st
import PyPDF2
from utils.parser import extract_text_from_file
from utils.gpt_helpers import generate_cover_letter
import requests


# --- Backend Communication Function ---
def call_backend_to_generate_cover_letter(resume_text, job_description):
    try:
        response = requests.post(
            "http://localhost:8000/generate-cover-letter",  # Change this to your Render URL after deployment
            json={"resume_text": resume_text, "job_description": job_description}
        )
        response.raise_for_status()
        return response.json()["cover_letter"]
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to contact backend: {e}")
    

def extract_text_from_file(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text    


# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🎯",
    layout="centered",
)

# --- Title & Description ---
st.title("🎯 AI Job Application Assistant")
st.markdown(
    "Upload your **resume** and paste a **job description**, and get a tailored, professional cover letter in seconds."
)

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# --- Job Description Input ---
job_description = st.text_area("📝 Paste the job description here", height=200)

# --- Action Button ---
if uploaded_file and job_description:
    if st.button("✨ Generate Cover Letter"):
        with st.spinner("Reading your resume and crafting the cover letter..."):
            try:
                resume_text = extract_text_from_file(uploaded_file)
                cover_letter = generate_cover_letter(resume_text, job_description)
                st.success("✅ Cover letter generated successfully!")

                # --- Output ---
                st.subheader("📬 Your Tailored Cover Letter")
                st.text_area("Cover Letter", value=cover_letter, height=300)

                # --- Download Button ---
                st.download_button("📥 Download Cover Letter", cover_letter, file_name="cover_letter.txt")

            except Exception as e:
                st.error(f"An error occurred: {e}")

elif not uploaded_file or not job_description:
    st.info("📌 Please upload your resume and paste a job description to begin.")
