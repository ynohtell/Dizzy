import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

from app import engine, manager
from app.services import load_session, save_session
from app import models as dt



app = FastAPI(title="Dizzy API")

@app.post("/sessions/create", response_model=dt.Session)
def create_game(user_id: str):
    try:
        session = manager.manage_session(user_id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sessions/{user_id}/{session_id}/matchup")
def get_current_matchup(user_id: str, session_id: str):
    try:
        session = manager.locate_session(user_id=user_id, session_id=session_id)
        match = manager.get_current_matchup(session=session)
        return match
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sessions/{user_id}/{session_id}/choose")
def submit_vote(user_id: str, session_id: str, winner_id: str):
    try:
        session = manager.locate_session(user_id, session_id)
        current_match = manager.get_current_matchup(session=session)
        song_a = current_match.song_a
        song_b = current_match.song_b
        
        if current_match.winner_id:
            raise ValueError('Current match already have winner')
        
        if not winner_id == song_a.id and not winner_id == song_b.id:
            raise ValueError('Incorrect Winner ID')

        file_path = f"stored_sessions/{user_id}/{session.id}.json"
        record_match = engine.submit_choice(session=session, winner_id=winner_id)
        save_session(session=record_match, filepath=file_path)
        return record_match
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/sessions/{user_id}/{session_id}/ranking')
def get_ranking(user_id: str, session_id: str):
    try:
        session = manager.locate_session(user_id=user_id, session_id=session_id)
        if not session.is_active:
            ranking = engine.get_ranking(session.id)
            return ranking 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
