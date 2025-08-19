from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os, shutil, json, pathlib, subprocess
# from .groq_client import chat


import os, requests

GROQ_API_URL = os.environ.get("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

def chat(prompt: str, system: str = "You are a helpful assistant.") -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        # Groq is optional; raise a gentle message for clarity
        return "Groq key not set. Set GROQ_API_KEY to enable LLM features."
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    r = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]


app = FastAPI(title="CRM Codegen (Groq-only)")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "domains"
TEMPLATES_DIR = ROOT / "templates"
OUTPUTS_DIR = ROOT.parent / "outputs"

class GenReq(BaseModel):
    domain: str
    out: str | None = None  # optional custom output path

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
def ui():
    return '''<!doctype html>
    <html><head><meta charset="utf-8"><title>CRM Codegen</title>
    <style>body{font-family:Inter,system-ui,Arial;padding:2rem;max-width:900px;margin:auto}</style>
    </head>
    <body>
    <h1>CRM Codegen (Groq-only)</h1>
    <p>Generate a domain-specific CRM (FastAPI + SQLModel + SQLite).</p>
    <form id="f">
    <label>Choose domain: </label>
    <select name="domain">
        <option>healthcare</option>
        <option>real_estate</option>
        <option>ecommerce</option>
        <option>education</option>
        <option>freelancers</option>
    </select>
    <input type="text" name="out" placeholder="Optional custom output folder (absolute or relative)"/>
    <button type="submit">Generate</button>
    </form>
    <pre id="out"></pre>
    <script>
    const f = document.getElementById('f');
    f.onsubmit = async (e)=>{
        e.preventDefault();
        const fd = new FormData(f);
        const body = {domain: fd.get('domain'), out: fd.get('out') || null};
        const r = await fetch('/generate', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
        const j = await r.json();
        document.getElementById('out').textContent = JSON.stringify(j, null, 2);
    };
    </script>
    </body></html>'''

@app.post("/generate")
def generate(req: GenReq):
    domain = req.domain.strip().lower()
    domain_json = DOMAINS_DIR / f"{domain}.json"
    if not domain_json.exists():
        raise HTTPException(status_code=400, detail=f"Unsupported domain: {domain}")
    out_dir = pathlib.Path(req.out) if req.out else OUTPUTS_DIR / f"{domain}_backend"
    out_dir = out_dir.resolve()
    # call CLI (so CLI & app share logic)
    import sys

    result = subprocess.run(
        [sys.executable, str(ROOT / "cli.py"), "--domain", domain, "--out", str(out_dir)],
        capture_output=True, text=True
)
    ok = result.returncode == 0
    return JSONResponse({"ok": ok, "stdout": result.stdout, "stderr": result.stderr, "out_dir": str(out_dir)})

class LLMReq(BaseModel):
    prompt: str

@app.post("/llm/explain")
def llm(req: LLMReq):
    text = chat(req.prompt)
    return {"text": text}
