import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from contextlib import asynccontextmanager

# Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
SESSION_TIMEOUT_MINUTES = 30

# In-memory storage for conversation sessions
sessions: Dict[str, Dict[str, Any]] = {}


def cleanup_old_sessions():
    """Remove sessions that have been inactive for longer than SESSION_TIMEOUT_MINUTES"""
    now = datetime.now()
    expired_sessions = [
        session_id
        for session_id, session_data in sessions.items()
        if now - session_data["last_activity"] > timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    ]
    for session_id in expired_sessions:
        del sessions[session_id]
        print(f"Cleaned up expired session: {session_id}")


# Initialize FastAPI app
app = FastAPI(title="HotelProfessionals Chatbot")

# CORS middleware - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System prompt to keep the bot focused on hotelprofessionals.nl
SYSTEM_PROMPT = """🎯 Jij bent een behulpzame Nederlandse assistent voor HotelProfessionals.nl.

🧠 Doel:
Help bezoekers uitsluitend met vacatures in de horeca en hotelsector op HotelProfessionals.nl. Geef alleen bruikbare informatie als er voldoende context is (functie, locatie, type dienstverband).

📜 Gedragsregels:
1. Beantwoord alleen vragen over vacatures, functies of het platform HotelProfessionals.nl.
2. Als een vraag over iets anders gaat, zeg vriendelijk: 
   "Ik ben speciaal getraind om te helpen met vacatures op HotelProfessionals.nl. Kan ik je helpen bij het vinden van een geschikte functie in de horeca of hotelsector?"
3. Vraag *altijd eerst door* als de vraag onvolledig is (bijv. geen functie, locatie of type dienstverband). Geef geen voorbeelden of vacatures totdat de gebruiker voldoende informatie heeft gegeven.
4. Geef voorbeelden dikgedrukt, gevolgd met de url van de vacature
5. Als je een lijst met vacatures noemt, zorg voor een lege regel boven en onder de lijst en gebruik altijd werkende links naar specifieke vacatures. Vermijd algemene filter- of zoekpagina’s.
6. Houd antwoorden kort, duidelijk en professioneel.
7. Benoem geen referenties in je antwoorden zoals [1], [3]

💡 Contextgedrag:
- Onthoud eerdere berichten in het gesprek.
- Gebruik alleen informatie die de gebruiker heeft gegeven om gerichte antwoorden te geven.
- Begin geen antwoord met willekeurige voorbeelden of vacatures zonder dat de gebruiker eerst duidelijk aangeeft wat hij/zij zoekt.
"""

@app.get("/")
def read_root() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "ok", "service": "HotelProfessionals Chatbot"}


@app.post("/new_session")
def create_new_session() -> Dict[str, str]:
    """Create a new chat session and return session ID"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "messages": [],
        "last_activity": datetime.now(),
        "created_at": datetime.now()
    }
    print(f"Created new session: {session_id}")
    return {"session_id": session_id}


@app.delete("/session/{session_id}")
def end_session(session_id: str) -> Dict[str, str]:
    """End a chat session and remove it from memory"""
    if session_id in sessions:
        del sessions[session_id]
        print(f"Ended session: {session_id}")
        return {"status": "success", "message": "Session ended"}
    return {"status": "not_found", "message": "Session not found"}


@app.get("/ask")
async def ask(
    question: str = Query(..., description="De vraag van de gebruiker"),
    session_id: Optional[str] = Query(None, description="Session ID voor conversatie context")
) -> Dict[str, Any]:
    """
    Main endpoint to ask questions to the chatbot.
    Maintains conversation history per session.
    """
    
    if not PERPLEXITY_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="PERPLEXITY_API_KEY environment variable is not set."
        )
    
    # Create new session if none provided or if session doesn't exist
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "messages": [],
            "last_activity": datetime.now(),
            "created_at": datetime.now()
        }
        print(f"Created new session: {session_id}")
    
    # Update last activity timestamp
    sessions[session_id]["last_activity"] = datetime.now()
    
    # Get conversation history for this session
    conversation_history = sessions[session_id]["messages"]
    
    # Build messages array for Perplexity API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": question})
    
    # Prepare payload for Perplexity API
    payload = {
        "model": "sonar",
        "messages": messages,
        "search_domain_filter": ["hotelprofessionals.nl"],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            PERPLEXITY_API_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            },
            timeout=30,
        )
        response.raise_for_status()
        
    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Perplexity API timeout - please try again."
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Perplexity API request failed: {str(exc)}"
        )
    
    # Parse response from Perplexity
    try:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        
        # Store user question and bot response in session history
        sessions[session_id]["messages"].append({"role": "user", "content": question})
        sessions[session_id]["messages"].append({"role": "assistant", "content": answer})
        
        # Limit history to last 10 messages (5 exchanges) to prevent token overflow
        if len(sessions[session_id]["messages"]) > 10:
            sessions[session_id]["messages"] = sessions[session_id]["messages"][-10:]
        
        return {
            "answer": answer,
            "session_id": session_id
        }
        
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected response format from Perplexity API: {str(exc)}"
        )


@app.get("/stats")
def get_stats() -> Dict[str, Any]:
    """Get current statistics about active sessions (useful for monitoring)"""
    return {
        "active_sessions": len(sessions),
        "sessions": [
            {
                "session_id": sid[:8] + "...",  # Truncate for privacy
                "message_count": len(data["messages"]),
                "last_activity": data["last_activity"].isoformat(),
                "age_minutes": (datetime.now() - data["created_at"]).seconds // 60
            }
            for sid, data in sessions.items()
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)