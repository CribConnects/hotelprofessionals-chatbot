# ⚡ Quick Start Guide

Kom binnen 5 minuten aan de slag!

## 1️⃣ Setup (2 minuten)

```bash
# Clone/download het project
cd hotelprofessionals-chatbot

# Maak virtual environment
python -m venv venv

# Activeer (Windows)
venv\Scripts\activate
# Of (macOS/Linux)
source venv/bin/activate

# Installeer
pip install -r requirements.txt
```

## 2️⃣ Configureer (1 minuut)

Maak een `.env` bestand:

```bash
PERPLEXITY_API_KEY=pplx-jouw-key-hier
```

## 3️⃣ Run (1 minuut)

```bash
# Start backend
python main.py
```

Open `index.html` in je browser. Klaar! 🎉

## 🚀 Deploy naar Railway (2 minuten)

```bash
# Push naar GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/JOUW-USERNAME/JOUW-REPO.git
git push -u origin main

# Op Railway:
# 1. New Project → Deploy from GitHub
# 2. Selecteer je repo
# 3. Voeg PERPLEXITY_API_KEY toe in Variables
# 4. Klaar!
```

Update `index.html` regel 121 met je Railway URL:
```javascript
const API_BASE_URL = 'https://jouw-app.up.railway.app';
```

## 🧪 Test

```bash
python test_setup.py
```

## 📚 Meer Info

- Uitgebreide setup: zie `README.md`
- Deployment details: zie `DEPLOYMENT_GUIDE.md`

---

**Hulp nodig?** Check de logs of de andere documentatie!
