from fastapi import FastAPI
from .routers import router

app = FastAPI(title="E-commerce CRM")
app.include_router(router)

@app.get("/")
def root():
    return {"ok": True, "service": "E-commerce CRM", "docs": "/docs"}