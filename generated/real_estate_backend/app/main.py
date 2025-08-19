from fastapi import FastAPI
from .routers import router

app = FastAPI(title="Real Estate CRM")
app.include_router(router)

@app.get("/")
def root():
    return {"ok": True, "service": "Real Estate CRM", "docs": "/docs"}