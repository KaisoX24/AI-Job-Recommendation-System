from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv
import PyPDF2

# Loadubg environment variables
load_dotenv()
client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Function to get job recommendations based on resume text
def job_recommendation(resume_text):
    try:
        system_prompt=("""You are an expert AI Job Recommendation Assistant.
            Always structure your output in **three main sections**:

            1. Job Recommendations
            - Profile Snapshot: Summarize candidate’s education, technical stack, experience, projects, certifications, and soft skills in a neat table.
            - Job Openings That Match Best: Create a table with columns:
                [# | Role | Why It Fits | Key Skills Required | How Resume Matches]

            2. Highlighted Required Skills & Qualifications
            - Make a table: [Skill | Typical Employer Requirement | Candidate’s Evidence from Resume]

            3. Tailored Job-Search Tips
            - Provide 3–4 specific tips, written in bullet points.
            - Add a "Next Steps" sub-section with clear, actionable advice (resume updates, networking, applications).

            Formatting rules
            - Use markdown tables.
            - Keep explanations concise, but specific (always reference keywords from resume).
            - Prioritize clarity and readability.""")
        
        response = client.chat.completions.create(
            model='openai/gpt-oss-20b',
            messages=[
                {
                    "role": "system",
                    "content":system_prompt},
                {
                "role": "user",
                "content": (
                    f"Here is my resume for job recommendations:\n\n {resume_text}"
                )}],
                temperature=0.7)
        return response.choices[0].message.content
    
    except Exception as e:
        return f'Something went wrong \n {e}'

# Web ui
st.set_page_config(page_title='AI Job Recommendation System',layout='wide')
st.title('AI JOB RECOMMENDATION SYSTEM')
st.write('Upload your resume and get job recommendations!')
st.write('---')
uploaded_file=st.sidebar.file_uploader('Upload Your Resume',type=['pdf'])

if uploaded_file:
    with st.spinner('Processing...'):
        uploaded_file=PyPDF2.PdfReader(uploaded_file)
        text=''
        for page in uploaded_file.pages:
            text+=page.extract_text()+'\n'

        recommendations=job_recommendation(text)
        st.subheader("Job Recommendations")
        st.markdown(recommendations)

        with st.expander("View Extracted Resume Text"):
            st.write(text)



