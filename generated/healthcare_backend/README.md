# Healthcare CRM (Generated)

A minimal FastAPI + SQLModel + SQLite backend for **healthcare**.

## Run (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000/docs
```

## Run (Docker)
```bash
docker build -t healthcare-backend .
docker run -p 8000:8000 -v $(pwd)/data:/data healthcare-backend
```

## Notes
- DB: SQLite at `/data/app.db`.
- Entities:

  - Patient (table: patients)

  - Doctor (table: doctors)

  - Appointment (table: appointments)

- Extra domain endpoint(s):

  - schedule_appointment: Create an appointment if patient & doctor exist.
