import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import requests
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# -------------------- Config --------------------
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
SESSION_TIMEOUT_MINUTES = 30

# In-memory session storage
sessions: Dict[str, Dict[str, Any]] = {}

# -------------------- App init --------------------
app = FastAPI(title="HotelProfessionals Chatbot")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Voor productie: voeg je frontend URL toe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt
SYSTEM_PROMPT = """🎯 Jij bent een behulpzame Nederlandse assistent voor HotelProfessionals.nl.

🧠 Doel:
Help bezoekers uitsluitend met vacatures in de horeca en hotelsector op HotelProfessionals.nl...
"""

# -------------------- Helper --------------------
def cleanup_old_sessions():
    now = datetime.now()
    expired = [sid for sid, s in sessions.items() if now - s["last_activity"] > timedelta(minutes=SESSION_TIMEOUT_MINUTES)]
    for sid in expired:
        del sessions[sid]
        print(f"Cleaned up session: {sid}")

def get_or_create_session(session_id: Optional[str] = None):
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "messages": [],
            "last_activity": datetime.now(),
            "created_at": datetime.now()
        }
        print(f"Created session: {session_id}")
    sessions[session_id]["last_activity"] = datetime.now()
    return session_id, sessions[session_id]

# -------------------- Endpoints --------------------
@app.post("/new_session")
def create_new_session():
    session_id, _ = get_or_create_session()
    return {"session_id": session_id}

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "success", "message": "Session ended"}
    return {"status": "not_found", "message": "Session not found"}

@app.api_route("/ask", methods=["GET", "POST"])
def ask(
    question: Optional[str] = Query(None),
    session_id: Optional[str] = Query(None),
    body: Optional[Dict[str, Any]] = Body(None)
):
    # Get question from body if POST
    if body and "question" in body:
        question = body["question"]

    if not question:
        raise HTTPException(status_code=400, detail="No question provided.")

    if not PERPLEXITY_API_KEY:
        raise HTTPException(status_code=500, detail="PERPLEXITY_API_KEY not set.")

    session_id, session_data = get_or_create_session(session_id)
    conversation = session_data["messages"]

    # Build payload
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation)
    messages.append({"role": "user", "content": question})

    payload = {
        "model": "sonar",
        "messages": messages,
        "search_domain_filter": ["hotelprofessionals.nl"],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    # Call Perplexity API
    try:
        response = requests.post(
            PERPLEXITY_API_URL,
            json=payload,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {PERPLEXITY_API_KEY}"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        # Safe parsing
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "Geen antwoord ontvangen van API.")
    except requests.RequestException as e:
        print("Perplexity API error:", e, getattr(e.response, 'text', ''))
        raise HTTPException(status_code=502, detail=f"Perplexity API request failed: {str(e)}")
    except Exception as e:
        print("Unexpected error:", e)
        raise HTTPException(status_code=502, detail=f"Unexpected error: {str(e)}")

    # Store conversation
    conversation.append({"role": "user", "content": question})
    conversation.append({"role": "assistant", "content": answer})
    if len(conversation) > 10:
        session_data["messages"] = conversation[-10:]

    return {"answer": answer, "session_id": session_id}

@app.get("/stats")
def stats():
    return {
        "active_sessions": len(sessions),
        "sessions": [
            {"session_id": sid[:8]+"...", "messages": len(s["messages"])}
            for sid, s in sessions.items()
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000, ))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
