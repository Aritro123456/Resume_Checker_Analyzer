import streamlit as st

# import your DB layer and utils
from db.connection import SessionLocal
from db.queries    import save_resume, delete_resume
from utils.agents  import tailor_resume  # example function

def main():
    st.set_page_config(page_title="Resume Tailor", layout="wide")
    st.title("🤖 ATS-Smart Resume Tailor")

    with st.sidebar:
        st.header("Upload Inputs")
        resume_file = st.file_uploader("Your current résumé", type=["pdf", "docx"])
        job_desc    = st.text_area("Paste the job description here", height=200)
        submit_btn  = st.button("Generate Tailored Résumé")

    if submit_btn:
        if not resume_file or not job_desc.strip():
            st.error("Please upload your résumé and paste a job description.")
            return

        # 1) Read & parse the résumé
        raw_text = resume_file.read()  # bytes
        # TODO: branch on file type and extract text (PyPDF2, python-docx, etc.)

        # 2) Tailor it
        tailored_bytes = tailor_resume(raw_text, job_desc)

        # 3) (Optional) Save to DB
        with SessionLocal() as db:
            record = save_resume(db, user_id=1, content=tailored_bytes)

        # 4) Offer download
        st.success("Here’s your tailored résumé!")
        st.download_button(
            label="📄 Download PDF",
            data=tailored_bytes,
            file_name="tailored_resume.pdf",
            mime="application/pdf"
        )

    # (Optional) List & delete past resumes
    st.markdown("---")
    st.header("Past Tailors")
    with SessionLocal() as db:
        items = delete_resume(db, list_only=True)  # or a query function
    for itm in items:
        cols = st.columns([8,1])
        cols[0].markdown(f"• **{itm.created_at:%Y-%m-%d}** — {itm.filename}")
        if cols[1].button("🗑️", key=itm.id):
            with SessionLocal() as db:
                delete_resume(db, itm.id)
            st.experimental_rerun()

if __name__ == "__main__":
    main()