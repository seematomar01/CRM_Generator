# Real Estate CRM (Generated)

A minimal FastAPI + SQLModel + SQLite backend for **real_estate**.

## Run (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000/docs
```

## Run (Docker)
```bash
docker build -t real_estate-backend .
docker run -p 8000:8000 -v $(pwd)/data:/data real_estate-backend
```

## Notes
- DB: SQLite at `/data/app.db`.
- Entities:

  - Property (table: properties)

  - Agent (table: agents)

  - Lead (table: leads)

- Extra domain endpoint(s):

  - assign_lead: Assign a lead to an agent.
