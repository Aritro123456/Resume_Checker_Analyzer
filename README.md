# Smart ATS Resume crewAI multi-agent system
An AI-powered resume tailoring system that automatically optimizes your resume for specific job postings using a crew of specialized AI agents. Built with CrewAI, this tool analyzes job requirements, your profile, and existing resume to produce ATS-optimized application materials and interview preparation guides.

## Features

- **Intelligent Job Analysis**: Extracts key requirements and qualifications from job postings
- **Profile Enhancement**: Builds comprehensive profiles using GitHub and personal information
- **Smart Resume Tailoring**: Optimizes your resume to match job requirements while maintaining authenticity
- **Interview Prep**: Generates relevant interview questions and talking points
- **Multiple Interfaces**: Choose between CLI and web-based UI
- **History Tracking**: Save and manage your tailored resumes (optional)

## Quick Start

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-agentic-ats-resume.git
cd smart-agentic-ats-resume

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Required API keys in `.env`:
- `OPENAI_API_KEY`: For GPT-4 Turbo integration
- `SERPER_API_KEY`: For web search capabilities

### Usage

#### Web Interface
```bash
streamlit run streamlit_app.py
```
Then upload your resume and paste the job description in the web interface.

#### Command Line
```bash
python3 bin/crew_run.py
```
Edit inputs in `bin/crew_run.py` for batch processing.

## Architecture

The system uses four specialized AI agents:
1. **Tech Job Researcher**: Analyzes job postings
2. **Personal Profiler**: Builds comprehensive candidate profiles
3. **Resume Strategist**: Optimizes resume content
4. **Interview Preparer**: Generates interview materials

### Key Components

- `utils/agents.py`: AI agent definitions and configuration
- `utils/tasks.py`: Workflow task definitions
- `utils/crew.py`: Agent orchestration
- `bin/crew_run.py`: CLI entry point
- `streamlit_app.py`: Web interface
- `db/`: Database integration (optional)

## Output

The system generates:
1. Tailored resume (MD/PDF format)
2. Interview preparation materials
3. Stored results in database (optional)

## Development

### Adding New Agents

1. Define new agent in `utils/agents.py`
2. Create corresponding task in `utils/tasks.py`
3. Update crew configuration in `utils/crew.py`

### Extending Functionality

- Modify agent tools in `utils/agents.py`
- Add new task types in `utils/tasks.py`
- Enhance UI in `streamlit_app.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is designed to optimize resumes while maintaining truthfulness. It will not generate false information or credentials.
