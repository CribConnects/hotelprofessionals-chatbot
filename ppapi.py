import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

PPLX_API_KEY = os.getenv("PPLX_API_KEY")

app = FastAPI()

# CORS zodat HTML met deze backend kan praten
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = None
if PPLX_API_KEY:
    try:
        # De officiele client gebruiken zodra deze geinstalleerd is
        from perplexity import Perplexity

        client = Perplexity(api_key=PPLX_API_KEY)
    except ImportError:
        # Dependency ontbreekt, laat de endpoint hierop reageren
        client = None


@app.get("/ask")
def ask(question: str = Query(..., description="De vraag van de gebruiker")):
    if not PPLX_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="PPLX_API_KEY environment variable ontbreekt.",
        )

    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Perplexity client niet beschikbaar; controleer dependencies.",
        )

    try:
        completion = client.chat.completions.create(
            model="sonar",
            messages=[
                {"role": "system", "content": "Je bent een Nederlandse vacature-assistent."},
                {"role": "user", "content": question},
            ],
            search_domain_filter=["https://www.hotelprofessionals.nl/"],
        )
        answer = completion.choices[0].message.content
        return {"answer": answer}

    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
