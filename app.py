
import streamlit as st
import requests
from utils.gpt_helpers import generate_cover_letter, tailor_resume
from utils.parser import extract_text_from_file
from utils.workspace_utils import save_to_workspace
from auth.auth_manager import is_logged_in, logout
import login

if not is_logged_in():
    login.show_login()  # This displays your login page
    st.stop()

st.set_page_config(page_title="AI Job Assistant", layout="wide")

def main():
    if not is_logged_in():
        st.warning("🔒 Please log in to access the app.")
        return

    st.title("🤖 AI Job Assistant")
    st.sidebar.title("🔧 Options")

    # Sign-out button
    if st.sidebar.button("Sign Out"):
        logout()
        st.rerun()

    section = st.sidebar.radio("Choose an action", [
        "Find Jobs", "Tailor Resume", "Generate Cover Letter", "Workspace"
    ])

    if section == "Find Jobs":
        keyword = st.text_input("Job Keyword", key="job_kw")
        location = st.text_input("Location", value="remote")
        experience = st.selectbox("Experience Level", ["Any", "Entry", "Mid", "Senior"])
        remote_only = st.checkbox("Remote only?", value=True)

        if st.button("Search"):
            with st.spinner("Searching for jobs..."):
                try:
                    res = requests.get("https://ai-job-backend.onrender.com/search_jobs", params={
                        "keyword": keyword,
                        "location": location,
                        "experience": experience,
                        "remote_only": remote_only
                    })
                    jobs = res.json().get("results", [])
                    st.session_state["job_list"] = jobs

                    if jobs:
                        st.success(f"✅ Found {len(jobs)} jobs")
                        for i, job in enumerate(jobs):
                            with st.expander(f"{job['title']} at {job['company']}"):
                                st.write(f"📍 {job.get('location', 'Unknown')}")
                                st.write(f"{job.get('description', '')[:300]}...")
                                if st.button(f"Use This Job {i}"):
                                    st.session_state["selected_job"] = job
                                    st.session_state["job_description"] = job["description"]
                    else:
                        st.warning("No jobs found.")

                except Exception as e:
                    st.error(f"Failed to fetch jobs: {e}")

    elif section == "Tailor Resume":
        uploaded_resume = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])
        job_description = st.text_area("Paste Job Description")

        if st.button("Tailor Resume"):
            if uploaded_resume and job_description:
                try:
                    resume_text = extract_text_from_file(uploaded_resume)
                    tailored = tailor_resume(resume_text, job_description)
                    st.text_area("📄 Tailored Resume", value=tailored, height=300)
                    save_to_workspace("tailored_resume.txt", tailored)
                    st.success("Resume tailored successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.info("Please upload your resume and provide job description.")

    elif section == "Generate Cover Letter":
        uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"], key="cl_resume")
        job_description = st.text_area("Paste Job Description", key="cl_job_desc")

        if st.button("Generate Cover Letter"):
            if uploaded_resume and job_description:
                with st.spinner("Crafting your letter..."):
                    try:
                        resume_text = extract_text_from_file(uploaded_resume)
                        cover_letter = generate_cover_letter(resume_text, job_description)
                        st.text_area("📬 Cover Letter", value=cover_letter, height=300)
                        st.download_button("📥 Download", cover_letter, file_name="cover_letter.txt")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.info("Please provide both resume and job description.")

    elif section == "Workspace":
        st.info("🗂️ Your workspace feature is under development.")

if __name__ == "__main__":
    main()
