# HotelProfessionals Chatbot 🤖

Een intelligente Nederlandse chatbot die bezoekers helpt met vacatures op HotelProfessionals.nl. Gebouwd met FastAPI en Perplexity AI's Sonar model met RAG-functionaliteit.

## 🌟 Features

- **Domain-specifieke zoekopdrachten**: Gebruikt Perplexity's `search_domain_filter` om alleen informatie van HotelProfessionals.nl op te halen
- **Conversatie geheugen**: Houdt context bij binnen een sessie voor natuurlijke gesprekken
- **Automatische cleanup**: Verwijdert inactieve sessies na 30 minuten (geen database groei)
- **Off-topic bescherming**: Stuurt gesprekken vriendelijk terug naar vacature-gerelateerde onderwerpen
- **Responsive UI**: Moderne chat interface met dark mode
- **Spraakherkenning**: Ondersteunt spraak-naar-tekst (in ondersteunde browsers)
- **Railway-ready**: Voorbereid voor eenvoudige deployment

## 🏗️ Architectuur

```
┌─────────────┐      HTTP      ┌─────────────┐     API Call    ┌──────────────┐
│   Frontend  │────────────────▶│   FastAPI   │────────────────▶│  Perplexity  │
│   (HTML/JS) │                 │   Backend   │                 │     Sonar    │
└─────────────┘◀────────────────└─────────────┘◀────────────────└──────────────┘
                    JSON                             JSON
                    
Backend Features:
- Session management (UUID-based)
- In-memory conversation history
- Automatic session cleanup
- CORS enabled voor frontend
```

## 📋 Vereisten

- Python 3.9+
- Perplexity API key (met Sonar toegang)
- Git

## 🚀 Lokale Setup

### 1. Clone de repository

```bash
git clone <your-repo-url>
cd hotelprofessionals-chatbot
```

### 2. Maak een virtuele omgeving

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Installeer dependencies

```bash
pip install -r requirements.txt
```

### 4. Configureer environment variables

Maak een `.env` bestand in de root directory:

```bash
cp .env.example .env
```

Bewerk `.env` en voeg je Perplexity API key toe:

```
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Start de backend

```bash
python main.py
```

Of met uvicorn direct:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

De API is nu beschikbaar op `http://localhost:8000`

### 6. Open de frontend

Open `index.html` in je browser, of serve het met een lokale server:

```bash
# Python 3
python -m http.server 3000

# Of met Node.js
npx serve
```

## 📡 API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "ok",
  "service": "HotelProfessionals Chatbot"
}
```

### `POST /new_session`
Maak een nieuwe chat sessie
```json
Response: {
  "session_id": "uuid-here"
}
```

### `GET /ask`
Stel een vraag aan de chatbot

Parameters:
- `question` (required): De vraag van de gebruiker
- `session_id` (optional): Session ID voor context

```json
Response: {
  "answer": "Het antwoord van de bot",
  "session_id": "uuid-here"
}
```

### `DELETE /session/{session_id}`
Beëindig een sessie
```json
Response: {
  "status": "success",
  "message": "Session ended"
}
```

### `GET /stats`
Krijg statistieken over actieve sessies (monitoring)
```json
Response: {
  "active_sessions": 3,
  "sessions": [...]
}
```

## 🚂 Railway Deployment

### Stap 1: Push naar GitHub

```bash
git init
git add .
git commit -m "Initial commit: HotelProfessionals chatbot"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Stap 2: Maak een Railway project

1. Ga naar [Railway.app](https://railway.app)
2. Klik op "New Project"
3. Selecteer "Deploy from GitHub repo"
4. Kies je repository
5. Railway detecteert automatisch de Python app

### Stap 3: Configureer Environment Variables

In Railway dashboard:
1. Ga naar je project
2. Klik op "Variables"
3. Voeg toe:
   - `PERPLEXITY_API_KEY`: Je Perplexity API key

### Stap 4: Deploy

Railway zal automatisch deployen. Je krijgt een URL zoals:
`https://your-app-name.railway.app`

### Stap 5: Update Frontend

In `index.html`, update de `API_BASE_URL`:

```javascript
const API_BASE_URL = 'https://your-app-name.railway.app';
```

Commit en push deze wijziging:

```bash
git add index.html
git commit -m "Update API URL for production"
git push
```

## 🔧 Configuratie

### Session Timeout

Standaard worden inactieve sessies na 30 minuten verwijderd. Pas dit aan in `main.py`:

```python
SESSION_TIMEOUT_MINUTES = 30  # Wijzig naar gewenste waarde
```

### Conversatie Geschiedenis Limiet

Standaard worden de laatste 10 berichten (5 uitwisselingen) bewaard. Pas dit aan in `main.py`:

```python
if len(sessions[session_id]["messages"]) > 10:  # Wijzig 10 naar gewenst aantal
    sessions[session_id]["messages"] = sessions[session_id]["messages"][-10:]
```

### System Prompt

Pas het gedrag van de bot aan door de `SYSTEM_PROMPT` in `main.py` te wijzigen.

### CORS Origins

Voor productie, beperk de toegestane origins in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jouw-frontend-domain.com"],  # Specifieke domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing

Test de API endpoints:

```bash
# Health check
curl http://localhost:8000/

# Maak sessie
curl -X POST http://localhost:8000/new_session

# Stel vraag
curl "http://localhost:8000/ask?question=Welke%20vacatures%20zijn%20er%3F&session_id=YOUR_SESSION_ID"

# Stats
curl http://localhost:8000/stats
```

## 📊 Monitoring

Gebruik het `/stats` endpoint om te monitoren:
- Aantal actieve sessies
- Session leeftijden
- Aantal berichten per sessie

Voor productie monitoring, overweeg tools zoals:
- Railway's ingebouwde monitoring
- Sentry voor error tracking
- Custom logging naar een logging service

## 🛠️ Troubleshooting

### API key problemen

Zorg ervoor dat je `.env` bestand correct is geconfigureerd:
```bash
# Check of environment variable is geladen
python -c "import os; print(os.getenv('PERPLEXITY_API_KEY'))"
```

### CORS errors

Als je CORS errors krijgt, check:
1. `allow_origins` in `main.py`
2. Of je frontend de juiste API URL gebruikt
3. Browser console voor specifieke error messages

### Session cleanup werkt niet

De cleanup task draait elke 5 minuten. Check de logs:
```bash
# Lokaal
python main.py

# Railway
Bekijk logs in Railway dashboard
```

### Perplexity timeout

Als requests timeout:
1. Check je internet connectie
2. Verhoog de timeout in `main.py`:
```python
response = requests.post(..., timeout=60)  # Verhoog van 30 naar 60
```

## 📚 Dependencies

- **FastAPI**: Modern, snel web framework
- **Uvicorn**: ASGI server
- **Requests**: HTTP library voor Perplexity API calls
- **Python-multipart**: Voor form data handling

## 🔐 Security Notes

- **Nooit** commit je `.env` bestand met API keys
- Gebruik Railway's environment variables voor productie
- Overweeg rate limiting voor productie gebruik
- Beperk CORS origins in productie
- Monitor API usage om onverwacht hoog gebruik te detecteren

## 📝 Toekomstige Verbeteringen

Mogelijke features om toe te voegen:
- [ ] Redis voor persistente session storage
- [ ] Rate limiting per IP/session
- [ ] Analytics en logging naar database
- [ ] Admin dashboard voor monitoring
- [ ] Email notificaties voor bepaalde queries
- [ ] Multi-language support
- [ ] A/B testing van verschillende prompts
- [ ] Feedback systeem (thumbs up/down)

## 📄 License

[Voeg je license hier toe]

## 👤 Contact

[Voeg je contact informatie hier toe]

---

**Made with ❤️ for HotelProfessionals.nl**
