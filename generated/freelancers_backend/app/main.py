from fastapi import FastAPI
from .routers import router

app = FastAPI(title="Freelancers CRM")
app.include_router(router)

@app.get("/")
def root():
    return {"ok": True, "service": "Freelancers CRM", "docs": "/docs"}