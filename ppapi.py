import os
from typing import Any, Dict

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

PPLX_API_KEY = os.getenv("PPLX_API_KEY")
PPLX_API_URL = "https://api.perplexity.ai/chat/completions"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/ask")
def ask(question: str = Query(..., description="De vraag van de gebruiker")) -> Dict[str, Any]:
    if not PPLX_API_KEY:
        raise HTTPException(status_code=500, detail="PPLX_API_KEY environment variable ontbreekt.")

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Je bent een Nederlandse vacature-assistent."},
            {"role": "user", "content": question},
        ],
        "search_domain_filter": ["https://www.hotelprofessionals.nl/"],
    }

    try:
        response = requests.post(
            PPLX_API_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {PPLX_API_KEY}",
            },
            timeout=30,
        )
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Perplexity request mislukte: {exc}") from exc

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Perplexity API gaf status {response.status_code}: {response.text}")

    data = response.json()
    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="Onverwacht antwoord van Perplexity.") from exc

    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
