import json
from backend.app import engine
from backend.app.services import load_session, save_session
from pathlib import Path


current_dir = Path(__file__).parent.parent
json_path = current_dir / "tests" / "fixtures" / "mock_tracks.json"


with open(json_path, 'r') as f:
    raw_data = json.load(f)
    f.close()

song_pool = [
    engine.dt.Song (
        id = item['id'],
        title = item['name'],
        artist = item['artists'][0]['name']
    )
    for item in raw_data['tracks']
]
    
try:

    if Path("session_state.json").exists():
        session = load_session("session_state.json")
        print(f"Resuming Session: {session.id}")
    else: 
        session = engine.create_session(user_id="user_dev123", songs=song_pool)
        print(f"✅ Engine started! Session ID: {session.id}")
        engine.advance_round(session)

    while session.is_active:
        if session.current_matchup_index >= len(session.matchups):
            engine.advance_round(session)
            if not session.is_active: break

        m = session.matchups[session.current_matchup_index]
        winner_obj, _ = engine.get_matchup_result((m.song_a, m.song_b))

        #Submit choice and Save
        engine.submit_choice(session, winner_id=winner_obj.id)
        save_session(session=session)

    print("🏆 Tournament Complete!")
    engine.get_ranking(session)

except ValueError as e:
    print(f"❌ {e}")
