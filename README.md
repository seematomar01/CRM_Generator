# CRM Codegen Suite (Groq-only)

This repo contains:
1. **Groq-powered code generator** (FastAPI + CLI) that produces domain-specific CRM backends (FastAPI + SQLModel + SQLite, no external DB needed).
2. **Five ready-to-run sample CRMs** already generated for: Healthcare, Real Estate, E-commerce, Education, and Freelancers.
3. **Docker setups** and **README** instructions for both the generator and each generated CRM.

## Requirements
- Python 3.11+ (if running locally without Docker)
- Docker (optional, recommended)
- A Groq API key (optional: only needed for the generator's LLM features). Set `GROQ_API_KEY` in your environment.

## Quick Start (Generator)
```bash
# 1) Run the generator (Docker)
docker compose up generator

# Open the UI:
# http://localhost:8080 (choose a domain and click Generate)
```

Or run locally without Docker:
```bash
cd generator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY=YOUR_KEY   # optional (only needed for LLM endpoints)
uvicorn app.main:app --host 0.0.0.0 --port 8080
# Open http://localhost:8080
```

CLI usage:
```bash
cd generator
source .venv/bin/activate  # if created
python cli.py generate --domain healthcare --out ../generated/healthcare_backend
```

## Run a Sample CRM (Docker)
Each pre-generated CRM is in `generated/<domain>_backend`.
Example (Healthcare):
```bash
cd generated/healthcare_backend
docker build -t crm-healthcare .
docker run -p 8000:8000 -v $(pwd)/data:/data crm-healthcare
# Open Swagger at http://localhost:8000/docs
```

## What’s Inside
- **Generator** (FastAPI + CLI): Jinja2 templates + domain configs. No external DB needed; SQLite is embedded.
- **Domains** supported:
  - Healthcare: Patients, Doctors, Appointments (+ appointment scheduling endpoint)
  - Real Estate: Properties, Agents, Leads (+ assign lead to agent)
  - E-commerce: Customers, Products, Orders (+ order total computation)
  - Education: Students, Courses, Admissions (+ enroll endpoint)
  - Freelancers: Clients, Projects, Invoices, TimeEntries (+ generate invoice from time)

**Note**: The Groq integration is used for optional helper endpoints (e.g., generating extended docs snippets). All primary codegen is deterministic via templates, so it works even without a GROQ_API_KEY.

## License
MIT
