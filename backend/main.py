import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

from app import engine, manager
from app.services import load_session, save_session
from app import models as dt
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="Dizzy API")
# Tell FastAPI who is allowed to talk to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your SvelteKit dev server URL
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

@app.post("/sessions/create", response_model=dt.Session)
def create_game(user_id: str):
    try:
        session = manager.manage_session(user_id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catching unexpected errors is good practice for stability
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/sessions/{user_id}/{session_id}/matchup")
def get_current_matchup(user_id: str, session_id: str):
    try:
        session = manager.get_active_session(user_id=user_id, session_id=session_id)
        pair = manager.get_current_matchup(session=session)
        return pair
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sessions/{user_id}/{session_id}/choose")
def submit_vote(user_id: str, session_id: str, winner_id: str):
    try:
        session = manager.get_active_session(user_id, session_id)
        if not session.is_active:
             ValueError('Session completed!')
             
        current_match = manager.get_current_matchup(session=session)
        song_a = current_match.song_a
        song_b = current_match.song_b
        
        if current_match.winner_id:
            raise ValueError('Current match already have winner')
        
        if winner_id != song_a.id and winner_id != song_b.id:
            raise ValueError('Incorrect Winner ID')

        session = engine.submit_choice(session=session, winner_id=winner_id)
        session = manager.get_matchup_status(session=session)
        return session
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/sessions/{user_id}/{session_id}/ranking')
def get_ranking(user_id: str, session_id: str):
    try:
        session = manager.get_inactive_session(user_id=user_id, session_id=session_id)
        if session is None:
            HTTPException(status_code=404, detail="Session not found")
        
        
        if session.is_active:
            raise ValueError('Session in progress.')


        ranking = engine.get_ranking(session)
        return ranking 
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Session not found")
