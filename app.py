import streamlit as st
from utils.gpt_helpers import generate_cover_letter
import PyPDF2

# --- Functions ---
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- UI ---
st.title("AI Job Application Assistant")
st.markdown("Upload your resume and a job description to get a tailored cover letter.")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")
job_description = st.text_area("Paste the job description")

if uploaded_file and job_description:
    with st.spinner("Generating your cover letter..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        cover_letter = generate_cover_letter(resume_text, job_description)
        st.subheader("Your Tailored Cover Letter")
        st.text_area("Cover Letter", value=cover_letter, height=300)
        st.download_button("Download Cover Letter", cover_letter, file_name="cover_letter.txt")
