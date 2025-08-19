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
