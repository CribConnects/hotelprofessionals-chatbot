from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# 🔑 Jouw API sleutel hier invullen
PPLX_API_KEY = "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"

app = FastAPI()

# CORS zodat HTML met deze backend kan praten
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Probeer perplexity te importeren, anders mock
try:
    from perplexity import Perplexity
    client = Perplexity(api_key=PPLX_API_KEY)
except ImportError:
    client = None

@app.get("/ask")
def ask(question: str = Query(..., description="De vraag van de gebruiker")):
    if client is None:
        return {"answer": "Perplexity module niet beschikbaar, tijdelijk uitgeschakeld."}

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

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn, os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
