from backend.app import models as dt
from pathlib import Path


def save_session(session: dt.Session, filepath: str = "session_state.json"):
    with open(filepath, "w") as f:
        f.write(session.model_dump_json(indent=4))
    print(f"💾 Session saved to {filepath}")

def load_session(filepath: str = "session_state.json") -> dt.Session:
    if not Path(filepath).exists():
        raise FileNotFoundError(f"No session file found at {filepath}")
        
    with open(filepath, "r") as f:
        data = f.read()
        session = dt.Session.model_validate_json(data)
        print(f"✅ Session loaded from {filepath}")
        return session