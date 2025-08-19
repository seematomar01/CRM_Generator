# Freelancers CRM (Generated)

A minimal FastAPI + SQLModel + SQLite backend for **freelancers**.

## Run (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000/docs
```

## Run (Docker)
```bash
docker build -t freelancers-backend .
docker run -p 8000:8000 -v $(pwd)/data:/data freelancers-backend
```

## Notes
- DB: SQLite at `/data/app.db`.
- Entities:

  - Client (table: clients)

  - Project (table: projects)

  - TimeEntry (table: time_entries)

  - Invoice (table: invoices)

- Extra domain endpoint(s):

  - generate_invoice: Create an invoice summing time_entries * project.rate_per_hour.
