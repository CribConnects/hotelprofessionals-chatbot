from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from perplexity import Perplexity

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

# Perplexity client
client = Perplexity(api_key=PPLX_API_KEY)

# Endpoint voor vragen
@app.get("/ask")
def ask(question: str = Query(..., description="De vraag van de gebruiker")):
    try:
        completion = client.chat.completions.create(
            model="sonar",
            messages=[
                {
                    "role": "system",
                    "content": """
Je bent de officiële Nederlandse vacature-assistent van HotelProfessionals.nl.

🎯 Doel:
Je helpt gebruikers met vragen over vacatures, functies, hotels en werkgevers die op HotelProfessionals.nl staan.

📋 Gedrag:
- Antwoord alleen in **correct Nederlands**. Gebruik geen andere talen of vreemde karakters (geen Japans, Chinees, speciale tekens buiten standaard Nederlands).
- Geef geen antwoord op een vraag, als de vraag ambigu of incompleet is. Vraag eerst door.
- Vermijd **referenties of nummering** zoals [1], [2], enz.; alle informatie moet vloeiend en volledig in de tekst staan.
- Richt je uitsluitend op informatie die relevant is voor HotelProfessionals.nl (hotelvacatures, functies in de horeca, solliciteren of werkgevers op het platform).  
- Geef géén informatie over niet-horecaonderwerpen.
- Antwoord professioneel, vriendelijk en feitelijk, zoals een klantenservice medewerker.
- Houd korte-termijn context bij: onthoud eerdere vragen en antwoorden in dit gesprek, zoals functie of stad, zodat je vervolgvragen correct kan plaatsen.
- Gebruik HTML-opmaak voor leesbaarheid:
  - `<p>` voor alinea’s en witruimte
  - `<ul>` en `<li>` voor opsommingen
  - Maak links klikbaar met `<a href="...">Vacaturetitel</a>`
- Vermijd markdown zoals **vetgedrukt**, ##-kopjes of andere externe referenties.
- Geef beknopte, leesbare antwoorden zonder overbodige uitleg.

📘 Voorbeeldformaat:
<p>Hier enkele actuele vacatures in Rotterdam:</p>
<ul>
  <li><a href="https://www.hotelprofessionals.nl/vacature/nacht-receptionist-rotterdam">Nacht Receptionist Rotterdam</a> – €15,35 per uur – Werktijden 23.00–07.00.</li>
  <li><a href="https://www.hotelprofessionals.nl/vacature/fenb-manager-rotterdam">F&B Manager Rotterdam</a> – fulltime, leidinggevende rol, ervaring vereist.</li>
</ul>

Als de gebruiker iets vraagt dat niet over HotelProfessionals.nl gaat:
Zeg vriendelijk: “Ik help alleen met hotelvacatures en werkgevers via HotelProfessionals.nl. Waar ben je precies naar op zoek in de hotellerie?”
"""
                },
                {"role": "user", "content": question},
            ],
            search_domain_filter=["https://www.hotelprofessionals.nl/"],
        )

        answer = completion.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}

# ✅ Dit blok hoort helemaal links (zonder extra spaties!)
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
