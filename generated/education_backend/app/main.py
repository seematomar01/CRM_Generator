from fastapi import FastAPI
from .routers import router

app = FastAPI(title="Education CRM")
app.include_router(router)

@app.get("/")
def root():
    return {"ok": True, "service": "Education CRM", "docs": "/docs"}