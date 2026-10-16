#!/usr/bin/env python3
"""
bin/crew_run.py

Programmatic entry-point to launch the ATS Resume Tailoring Crew with predefined inputs.
"""
import warnings
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

warnings.filterwarnings('ignore')
load_dotenv()

from utils import get_openai_api_key, get_serper_api_key

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
from utils.crew import job_application_crew

job_application_inputs = {
    'job_posting_url': (
        'https://jobs.lever.co/AIFund/6c82e23e-d954-4dd8-a734-c0c2c5ee00f1'
        '?lever-origin=applied&lever-source%5B%5D=AI+Fund'
    ),
    'github_url': 'https://github.com/joaomdmoura',
    'personal_writeup': (
        """
Noah is an accomplished Software Engineering Leader with 18 years of experience, specializing in
managing remote and in-office teams, and expert in multiple programming languages and frameworks.
He holds an MBA and a strong background in AI and data science. Noah has successfully led major tech
initiatives and startups, proving his ability to drive innovation and growth in the tech industry.
Ideal for leadership roles that require a strategic and innovative approach.
        """
    )
}

result = job_application_crew.kickoff(inputs=job_application_inputs)

print("Workflow executed. Result keys:")
for key in result:
    print(f" - {key}")
