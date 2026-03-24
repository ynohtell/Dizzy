import json
from pathlib import Path
from .services import load_session, save_session
from .engine import create_session, advance_round
from .models import Song, Session




def manage_session(user_id: str):
    try:
        restored_session = get_active_session(user_id=user_id)
        if restored_session:
            print("Session restored!")
            return restored_session
        else: 
            song_pool = fetch_user_data(user_id)
            session = create_session(user_id=user_id, songs=song_pool)
            file_path = f"stored_sessions/{user_id}/{session.id}.json"
            advance_round(session)
            session = save_session(session=session, filepath=file_path)
            print("Session created!")
            return session
    except ValueError as e:
        print(f"❌ {e}")


def fetch_user_data(user_id: str):
    # User_id fetching to do
    current_dir = Path(__file__).parent.parent
    json_path = current_dir / "tests" / "fixtures" / "mock_tracks.json"

    
    with open(json_path, 'r') as f:
        raw_data = json.load(f)
        f.close()

    song_pool = [
        Song (
            id = item['id'],
            title = item['name'],
            artist = item['artists'][0]['name']
        )
        for item in raw_data['tracks']
    ]

    return song_pool


def get_current_matchup(session: Session):
    m = session.matchups[session.current_matchup_index]
    return m

def get_matchup_status(session: Session) -> Session:
    file_path = f"stored_sessions/{session.user_id}/{session.id}.json"
    if session.current_matchup_index >= len(session.matchups):
        session = advance_round(session)
        print(f"Round advanced to {session.current_round} and SAVED.")

    save_session(session=session, filepath=file_path)
    return session


def get_active_session(user_id: str, session_id: str = None) -> Session | None :
    user_dir = Path(f'stored_sessions/{user_id}')

    if user_dir.exists():
        if session_id:
            file = Path(f'stored_sessions/{user_id}/{session_id}.json')
            current_session = load_session(filepath=file)
            if current_session and current_session.is_active:
                return current_session
            else:
                return None
        else:
            for file in user_dir.glob('*.json'):
                session = load_session(filepath=file)
                if session.is_active:
                    return session
    else:
        return None


def get_inactive_session(user_id: str, session_id: str = None) -> Session | None :
    user_dir = Path(f'stored_sessions/{user_id}')

    if user_dir.exists():
        if session_id:
            file = Path(f'stored_sessions/{user_id}/{session_id}.json')
            current_session = load_session(filepath=file)
            if current_session and not current_session.is_active:
                return current_session
            else:
                return None
        else:
            for file in user_dir.glob('*.json'):
                session = load_session(filepath=file)
                if session.is_active:
                    return session
    else:
        return None
    
