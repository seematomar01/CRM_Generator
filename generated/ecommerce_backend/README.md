# E-commerce CRM (Generated)

A minimal FastAPI + SQLModel + SQLite backend for **ecommerce**.

## Run (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000/docs
```

## Run (Docker)
```bash
docker build -t ecommerce-backend .
docker run -p 8000:8000 -v $(pwd)/data:/data ecommerce-backend
```

## Notes
- DB: SQLite at `/data/app.db`.
- Entities:

  - Customer (table: customers)

  - Product (table: products)

  - Order (table: orders)

- Extra domain endpoint(s):

  - compute_order_total: Compute and set order total = quantity * product.price.
