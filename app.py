import streamlit as st
import PyPDF2
from utils.parser import extract_text_from_file
from utils.gpt_helpers import generate_cover_letter
import requests
from utils.workspace_utils import save_to_workspace
from utils.auth_utils import sign_in_with_email_password, sign_up
import requests
from PIL import Image



if "user" not in st.session_state:
    st.title("Login to AI Job Assistant")

    auth_mode = st.radio("Select Action", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Continue"):
        if auth_mode == "Login":
            user = sign_in_with_email_password(email, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid login")
        else:
            if sign_up(email, password):
                st.success("Registered! Please login.")
            else:
                st.error("Registration failed")

    st.stop()

# --- Backend Communication Function ---
def call_backend_to_generate_cover_letter(resume_text, job_description):
    try:
        response = requests.post(
            "https://ai-job-backend.onrender.com/generate-cover-letter",  # Change this to your Render URL after deployment
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

BACKEND_URL = "https://ai-job-backend.onrender.com"  # or deployed backend URL
def get_jobs_from_backend(query, location):
    res = requests.get(f"{BACKEND_URL}/jobs", params={"query": query, "location": location})
    return res.json() if res.status_code == 200 else []

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

st.header("🔍 AI Job Finder")
job_query = st.text_input("Search Jobs (e.g. 'Python Developer')", "AI Engineer")
job_location = st.text_input("Location", "Remote")

if st.button("🔎 Find Jobs"):
    jobs = get_jobs_from_backend(job_query, job_location)
    for i, job in enumerate(jobs):
        st.markdown(f"**{job['title']}** at *{job['company']}*")
        st.write(job["summary"])
        with st.expander("🔗 View / Apply"):
            st.write(f"[Open Job Posting]({job['link']})")

        if st.button(f"Use this job ↓", key=f"job_select_{i}"):
            st.session_state.job_description = job["summary"]
            st.experimental_rerun()


# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# --- Job Description Input ---
job_description = st.text_area("📝 Paste the job description here", height=200, value=st.session_state.get('job_description', ''))

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


# Search Jobs
st.subheader("🔍 Find Jobs")
with st.form(key="job_search"):
    keyword = st.text_input("🔎 Job keyword (e.g., Data Scientist)")
    location = st.text_input("📍 Location (optional)")
    experience = st.selectbox("🧠 Experience Level", ["", "Junior", "Mid", "Senior"])
    remote_only = st.checkbox("Remote only", value=True)
    submit = st.form_submit_button("Search Jobs")

if submit and keyword:
    with st.spinner("Searching..."):
        try:
            response = requests.get(
                "https://ai-job-backend.onrender.com/search_jobs",
    params={
        "keyword": keyword,
        "location": location,
        "experience": experience,
        "remote_only": remote_only
                }
            )
            jobs = response.json().get("results", [])

            if jobs:
                st.success(f"Found {len(jobs)} jobs")
                for i, job in enumerate(jobs):
                    with st.expander(f"{job['title']} at {job['company']}"):
                        st.write(f"📍 {job['location']}")
                        st.write(f"[Apply Here]({job['url']})")
                        if st.button(f"Use This Job {i}"):
                            st.session_state['selected_job'] = job
                            st.session_state['job_description'] = job['description']
            else:
                st.warning("No matching jobs found.")
        except Exception as e:
            st.error(f"Error fetching jobs: {e}")

#..Application Page
for i, job in enumerate(jobs):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{job['title']}** at *{job['company']}*")
        st.caption(job['location'])
        st.write(job['description'][:300] + "...")
with col2:
    if st.button(f"Apply Now {i}"):
        js = f"window.open('{job['url']}')"
        st.components.v1.html(f"<script>{js}</script>", height=0)


#..Tailor Resume
if uploaded_file and job_description:
    st.markdown("### 🛠️ Tailor My Resume to This Job")
    if st.button("🧠 Tailor Resume"):
        with st.spinner("Tailoring your resume..."):
            try:
                resume_text = extract_text_from_file(uploaded_file)
                tailored_resume = cover_letter(resume_text, job_description)
                st.text_area("🎯 Tailored Resume", value=tailored_resume, height=400)
                st.download_button("📥 Download Tailored Resume", tailored_resume, file_name="tailored_resume.txt")
            except Exception as e:
                st.error(f"An error occurred while tailoring: {e}")

#..Save tailored Resume
file_path = save_to_workspace(tailored_resume)
st.success(f"🗂️ Saved to workspace: `{file_path}`")

#.. Apply Assistant
if st.button(f"🪄 Use My Tailored Resume {i}"):
    st.session_state['active_resume'] = tailored_resume
    st.session_state['active_cover_letter'] = cover_letter
    st.markdown("✅ Tailored documents loaded. Ready to apply!")

if 'active_resume' in st.session_state:
    st.subheader("📎 Quick Copy to Apply")
    st.text_area("📄 Resume", st.session_state['active_resume'], height=200)
    st.text_area("📝 Cover Letter", st.session_state['active_cover_letter'], height=200)
    st.caption("👆 Copy these and paste into the application form manually.")

