# 🚀 Deployment Guide: GitHub naar Railway

Deze gids helpt je stap-voor-stap om je HotelProfessionals chatbot te deployen van je lokale machine naar GitHub en vervolgens naar Railway.

## 📋 Voordat je begint

Zorg dat je hebt:
- [x] Git geïnstalleerd op je computer
- [x] Een GitHub account
- [x] Een Railway account (maak er één op [railway.app](https://railway.app))
- [x] Je Perplexity API key bij de hand

## Stap 1: Lokaal Testen ✅

Voordat we deployen, test eerst of alles lokaal werkt.

### 1.1 Maak een .env bestand

```bash
# Kopieer het voorbeeld bestand
cp .env.example .env

# Open .env en voeg je API key toe
# PERPLEXITY_API_KEY=pplx-jouw-key-hier
```

### 1.2 Installeer dependencies

```bash
# Maak een virtual environment
python -m venv venv

# Activeer het
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installeer packages
pip install -r requirements.txt
```

### 1.3 Start de server

```bash
python main.py
```

Je zou moeten zien:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 1.4 Test de applicatie

Open een nieuwe terminal en run het test script:

```bash
python test_setup.py
```

Als alle tests slagen, ben je klaar voor deployment! 🎉

## Stap 2: Push naar GitHub 📤

### 2.1 Maak een nieuwe GitHub repository

1. Ga naar [github.com](https://github.com)
2. Klik op het "+" icoon rechtsboven
3. Selecteer "New repository"
4. Vul in:
   - Repository name: `hotelprofessionals-chatbot` (of een andere naam)
   - Description: "AI chatbot voor HotelProfessionals.nl vacatures"
   - Public of Private: Jouw keuze
   - **NIET** "Initialize with README" aanvinken (we hebben al bestanden)
5. Klik "Create repository"

### 2.2 Initialiseer Git lokaal

In je project folder:

```bash
# Initialiseer git (als nog niet gedaan)
git init

# Voeg alle bestanden toe
git add .

# Check wat er toegevoegd wordt (optioneel)
git status

# Maak je eerste commit
git commit -m "Initial commit: HotelProfessionals chatbot"

# Stel de main branch in
git branch -M main
```

### 2.3 Link naar GitHub en push

Vervang `YOUR-USERNAME` en `YOUR-REPO-NAME` met je eigen gegevens:

```bash
# Voeg GitHub remote toe
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Push naar GitHub
git push -u origin main
```

Als het goed is gegaan, zie je je code nu op GitHub! 🎊

### 2.4 Verifieer op GitHub

1. Ga naar je repository op GitHub
2. Check of alle bestanden er zijn:
   - ✅ main.py
   - ✅ requirements.txt
   - ✅ Procfile
   - ✅ runtime.txt
   - ✅ README.md
   - ✅ index.html
   - ❌ .env (deze zou NIET zichtbaar moeten zijn!)

**BELANGRIJK**: Als je `.env` bestand zichtbaar is op GitHub:
```bash
# Verwijder het van Git
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

## Stap 3: Deploy naar Railway 🚂

### 3.1 Maak een Railway account

1. Ga naar [railway.app](https://railway.app)
2. Klik "Sign in" rechtsboven
3. Kies "Login with GitHub"
4. Autoriseer Railway

### 3.2 Maak een nieuw project

1. Op het Railway dashboard, klik "New Project"
2. Selecteer "Deploy from GitHub repo"
3. Als dit je eerste keer is, klik "Configure GitHub App"
   - Geef Railway toegang tot je repositories
   - Selecteer je `hotelprofessionals-chatbot` repository
4. Klik op je repository in de lijst

### 3.3 Configureer Environment Variables

Railway begint automatisch met bouwen, maar we moeten eerst de API key toevoegen:

1. In je Railway project, klik op je service
2. Ga naar het "Variables" tabblad
3. Klik "+ New Variable"
4. Voeg toe:
   ```
   Variable name: PERPLEXITY_API_KEY
   Value: pplx-jouw-echte-key-hier
   ```
5. Klik "Add" of druk Enter

### 3.4 Wacht op deployment

Railway zal nu:
1. ✅ Je code detecteren
2. ✅ Python dependencies installeren
3. ✅ De server starten
4. ✅ Een publieke URL genereren

Dit duurt 2-3 minuten. Je ziet de progress in het "Deployments" tabblad.

### 3.5 Verkrijg je publieke URL

1. In je Railway project, klik op je service
2. Ga naar het "Settings" tabblad
3. Scroll naar "Networking"
4. Klik "Generate Domain"
5. Je krijgt een URL zoals: `https://hotelprofessionals-chatbot-production-xxxx.up.railway.app`

**Kopieer deze URL!** Je hebt hem zo nodig.

### 3.6 Test je deployment

Open een browser en ga naar:
```
https://JOUW-RAILWAY-URL.railway.app/
```

Je zou moeten zien:
```json
{"status":"ok","service":"HotelProfessionals Chatbot"}
```

Test ook de API:
```
https://JOUW-RAILWAY-URL.railway.app/ask?question=Welke%20vacatures%20zijn%20er
```

Als dit werkt, is je backend live! 🎉

## Stap 4: Connect Frontend naar Backend 🔗

Nu moeten we de frontend updaten om met je Railway backend te praten.

### 4.1 Update index.html

Open `index.html` en vind deze regel (ongeveer regel 121):

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

Verander het naar je Railway URL:

```javascript
const API_BASE_URL = 'https://jouw-app-naam.up.railway.app';
```

**Belangrijk**: Geen trailing slash!

### 4.2 Commit en push de wijziging

```bash
git add index.html
git commit -m "Update API URL for production"
git push origin main
```

### 4.3 Test de frontend

Open `index.html` in je browser. De chatbot zou nu moeten werken met je live backend!

Test met een vraag zoals:
- "Welke vacatures zijn er beschikbaar?"
- "Ik zoek een baan als kok"
- "Zijn er vacatures in Amsterdam?"

## Stap 5: Host de Frontend (Optioneel) 🌐

Je hebt verschillende opties om de frontend te hosten:

### Optie A: GitHub Pages (Gratis, Simpel)

1. Ga naar je GitHub repository
2. Klik "Settings"
3. Scroll naar "Pages" in de linker sidebar
4. Under "Source", selecteer "main" branch
5. Klik "Save"
6. Je frontend is nu live op: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

### Optie B: Netlify (Gratis, Meer features)

1. Ga naar [netlify.com](https://netlify.com)
2. Sign in met GitHub
3. Klik "Add new site" → "Import an existing project"
4. Selecteer je GitHub repository
5. Deploy settings:
   - Build command: (laat leeg)
   - Publish directory: `.` (de root)
6. Klik "Deploy"

### Optie C: Vercel (Gratis, Zeer snel)

1. Ga naar [vercel.com](https://vercel.com)
2. Sign in met GitHub
3. Click "Add New" → "Project"
4. Selecteer je repository
5. Klik "Deploy"

### Optie D: Op Railway (Alles bij elkaar)

1. In je Railway project, klik "+ New"
2. Selecteer "Empty Service"
3. In de service settings:
   - Klik "Settings" → "Source"
   - Selecteer je GitHub repository
   - Root directory: `.`
   - Start command: `python -m http.server 8080`
4. Genereer een domain voor deze service

## 🎊 Klaar!

Je chatbot is nu volledig live! Hier is wat je hebt:

- ✅ Backend op Railway met Perplexity AI integratie
- ✅ In-memory session management
- ✅ Automatische cleanup
- ✅ Frontend (lokaal of gehost)
- ✅ Full conversational AI over HotelProfessionals.nl

## 📊 Monitoring en Onderhoud

### Railway Logs Bekijken

1. Ga naar je Railway project
2. Klik op je service
3. Ga naar het "Deployments" tabblad
4. Klik op de laatste deployment
5. Bekijk de logs in real-time

### Stats Endpoint

Monitoren hoeveel sessies er actief zijn:
```
https://JOUW-URL.railway.app/stats
```

### Als iets niet werkt

**Backend problemen:**
- Check Railway logs voor errors
- Verifieer dat PERPLEXITY_API_KEY is ingesteld
- Test de health endpoint: `/`

**Frontend problemen:**
- Check browser console (F12) voor errors
- Verifieer dat API_BASE_URL correct is
- Check of CORS errors zijn (zou niet moeten met onze config)

**API key problemen:**
- Verifieer je Perplexity API key
- Check of je credits hebt in je Perplexity account
- Test de API key met curl:
  ```bash
  curl -X POST https://api.perplexity.ai/chat/completions \
    -H "Authorization: Bearer YOUR_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model": "sonar", "messages": [{"role": "user", "content": "test"}]}'
  ```

## 🔄 Updates Deployen

Wanneer je wijzigingen maakt:

```bash
# Maak je wijzigingen in de code
# ...

# Commit de wijzigingen
git add .
git commit -m "Beschrijving van je wijzigingen"

# Push naar GitHub
git push origin main
```

Railway zal automatisch de nieuwe versie deployen! 🚀

## 🆘 Hulp Nodig?

- Railway docs: [docs.railway.app](https://docs.railway.app)
- Perplexity API docs: [docs.perplexity.ai](https://docs.perplexity.ai)
- GitHub docs: [docs.github.com](https://docs.github.com)

---

**Succes met je deployment! 🎉**
