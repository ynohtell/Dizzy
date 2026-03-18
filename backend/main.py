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
        file_path = f"{user_id}/{session.id}-session_state.json"
        save_session(session=session, filepath=file_path)
        return session
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))


@app.get("/sessions/{session_id}/matchup")
def get_current_matchup(session_id: str):
    try:
        session_id = load_session(f"{session_id}-session_state.json")
        return "Successful"
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))


@app.post("/sessions/{session_id}/choose")
def submit_vote(session_id: str, winner_id: str):
    ...


@app.get('/sessions/{session.id}/ranking')
def get_ranking():
    ...

