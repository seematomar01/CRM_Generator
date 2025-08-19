# Education CRM (Generated)

A minimal FastAPI + SQLModel + SQLite backend for **education**.

## Run (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000/docs
```

## Run (Docker)
```bash
docker build -t education-backend .
docker run -p 8000:8000 -v $(pwd)/data:/data education-backend
```

## Notes
- DB: SQLite at `/data/app.db`.
- Entities:

  - Student (table: students)

  - Course (table: courses)

  - Admission (table: admissions)

- Extra domain endpoint(s):

  - enroll_student: Enroll a student into a course (create Admission).
