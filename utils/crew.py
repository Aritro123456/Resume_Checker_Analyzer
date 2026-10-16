#!/usr/bin/env python3
"""
crew.py

Principal‐developer–level, architected implementation of the ATS Resume‐Tailoring workflow.
Defines configuration, tools, agents, tasks, crew assembly, and execution in one file.
"""

import warnings
import os
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, ScrapeWebsiteTool, MDXSearchTool, SerperDevTool


# ─── Configuration & Environment ───────────────────────────────────────────────

warnings.filterwarnings("ignore")

# Load .env from project root (fails silently if not found)
load_dotenv()

# Set up structured logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Tool Factory ─────────────────────────────────────────────────────────────

def create_tools(resume_path: str, mdx_path: str):
    """
    Instantiate and return the set of CrewAI tools.
    """
    return {
        "search": SerperDevTool(api_key=os.environ["SERPER_API_KEY"]),
        "scrape": ScrapeWebsiteTool(),
        "read_resume": FileReadTool(file_path=resume_path),
        "semantic_search": MDXSearchTool(mdx=mdx_path),
    }

# ─── Agent Factory ────────────────────────────────────────────────────────────

def create_agents(tools):
    """
    Build and return the list of Agents driving the workflow.
    """
    researcher = Agent(
        role="Tech Job Researcher",
        goal="Analyze job postings deeply to identify required skills & qualifications.",
        tools=[tools["scrape"], tools["search"]],
        verbose=True,
        backstory=(
            "Extract critical information from job postings to form the foundation "
            "for tailored resume content."
        )
    )

    profiler = Agent(
        role="Personal Profiler for Engineers",
        goal="Compile detailed personal and professional profiles from diverse sources.",
        tools=[tools["scrape"], tools["search"], tools["read_resume"], tools["semantic_search"]],
        verbose=True
    )

    resume_strategist = Agent(
        role="Resume Strategist for Engineers",
        goal="Optimize resumes so they align tightly with job requirements.",
        tools=[tools["scrape"], tools["search"], tools["read_resume"], tools["semantic_search"]],
        verbose=True
    )

    interview_preparer = Agent(
        role="Engineering Interview Preparer",
        goal="Generate focused interview questions & talking points.",
        tools=[tools["scrape"], tools["search"], tools["read_resume"], tools["semantic_search"]],
        verbose=True
    )

    return [researcher, profiler, resume_strategist, interview_preparer]

# ─── Task Factory ─────────────────────────────────────────────────────────────

def create_tasks(agents):
    """
    Create and return Task objects linked to each Agent.
    """
    researcher, profiler, strategist, interviewer = agents

    research_task = Task(
        name="Extract Job Requirements",
        description=(
            "Analyze the job posting URL ({job_posting_url}) to extract key "
            "skills, experiences, and qualifications required."
        ),
        expected_output="Structured list of required skills, qualifications, and experiences.",
        agent=researcher,
        async_execution=True
    )

    profile_task = Task(
        name="Compile Applicant Profile",
        description=(
            "Compile a profile using:\n"
            "  • GitHub:        ({github_url})\n"
            "  • LinkedIn:      ({linkedin_url})\n"
            "  • Google Scholar:({scholar_url})\n"
            "  • Portfolio:     ({portfolio_url})\n"
            "  • Personal write-up: ({personal_writeup})\n"
            "Extract and synthesize information from all sources."
        ),
        expected_output=(
            "Comprehensive profile including skills, projects, publications, and highlights."
        ),
        agent=profiler,
        async_execution=True
    )

    resume_strategy_task = Task(
        name="Tailor Resume",
        description=(
            "Using outputs from previous tasks, tailor the resume to highlight the most relevant "
            "experience and skills. Do not invent information."
        ),
        expected_output="Markdown resume perfectly aligned with the job posting.",
        output_file="tailored_resume.md",
        context=[research_task, profile_task],
        agent=strategist
    )

    interview_task = Task(
        name="Prepare Interview Materials",
        description=(
            "Generate interview questions and talking points based on the tailored resume "
            "and job requirements to prepare the candidate."
        ),
        expected_output="Markdown with key questions and talking points.",
        output_file="interview_materials.md",
        context=[research_task, profile_task, resume_strategy_task],
        agent=interviewer
    )

    return [research_task, profile_task, resume_strategy_task, interview_task]

# ─── Main Workflow ────────────────────────────────────────────────────────────

def main():
    # Instantiate tools, agents, and tasks
    tools  = create_tools(resume_path="../data/Nikhil_Nageshwar_Inturi.pdf", mdx_path="../data/Nikhil_Nageshwar_Inturi.pdf")
    agents = create_agents(tools)
    tasks  = create_tasks(agents)

    # Assemble the Crew
    crew = Crew(agents=agents, tasks=tasks, verbose=True)

    # Define inputs (extendable with any URLs or writeups)
    inputs = {
        "job_posting_url": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4215170359",
        "github_url":      "https://github.com/unikill066",
        "linkedin_url":    "https://www.linkedin.com/in/nikhilinturi/",
        "scholar_url":     "https://scholar.google.com/citations?user=9mU1K0cAAAAJ&hl=en",
        "portfolio_url":   "https://inturinikhilnageshwar.netlify.app/",
        "personal_writeup": (
            "I build AI that helps scientists decode pain. With 7 + years at the intersection of Generative AI, "
            "Machine Learning, and Bioinformatics, I’ve shipped everything from RAG-powered chatbots that surface lab "
            "insights on demand to high-throughput pipelines that segment millions of neurons 95 % effectively and 15 % "
            "more accurately than before. Today: Senior Data Scientist at the Center for Advanced Pain Studies (UT Dallas) "
            "and M.S. candidate in Business Analytics & AI, leading three cross-functional teams (image segmentation, "
            "sequencing analytics, bioinformatics). Recent wins include:\n"
            "• Unified data-to-knowledge chat system that ingests spatial & single-cell omics, publications, and lab notebooks via "
            "custom RAG pipelines—cutting search time from hours to minutes.\n"
            "• Neuron-detection suite (Detectron2 | YOLOv11 | SAM) that improved labeling precision by 15 % and scaled inference 10× on Kubernetes.\n"
            "• Predictive models of rat jaw kinematics, supporting pre-clinical pain-modulation studies.\n"
            "Previously: At Infosys and Aganitha, I automated AAV capsid engineering, built 7-mer clustering models, and optimized enterprise "
            "ML workflows that now analyze > 5 TB of genomic data weekly.\n"
            "Tech stack: Python, PyTorch, FastAI, Hugging Face, Nextflow, Docker/K8s, SQL, R, Tableau. Methodologies: RAG & Agentic AI "
            "architectures, CV segmentation, single-cell & spatial-omics analysis, MLOps, container orchestration.\n"
            "When I’m not coding, I’m a Technical Officer for Code.exe @ UTD—hosting hands-on workshops in Python, SQL, and Docker for 500+ "
            "students each semester.\n"
            "Let’s connect if you’re exploring AI for neuroscience, multi-omic analytics, or just want to geek out over Generative AI’s next leap.\n"
            "GitHub: https://github.com/unikill066"
        )
    }

    logger.info("Starting ATS Resume Tailoring workflow...")
    result = crew.kickoff(inputs=inputs)
    logger.info("Workflow complete. Generated outputs: %s", list(result.keys()))

    return result

if __name__ == "__main__":
    main()
