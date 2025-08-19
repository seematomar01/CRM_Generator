from fastapi import FastAPI
from .routers import router

app = FastAPI(title="Healthcare CRM")
app.include_router(router)

@app.get("/")
def root():
    return {"ok": True, "service": "Healthcare CRM", "docs": "/docs"}