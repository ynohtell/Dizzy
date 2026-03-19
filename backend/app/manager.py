import json
from pathlib import Path
from .services import load_session, save_session
from .engine import create_session, advance_round
from .models import Song, Session




def manage_session(user_id: str):
    try:
        user_dir = Path(f'stored_sessions/{user_id}')
        

        if user_dir.exists():
            for file in user_dir.glob('*.json'):
                session = load_session(filepath=file)
                if session.is_active:
                    print("Session restored!")
                    return session
        else: 
            song_pool = fetch_user_data(user_id)
            session = create_session(user_id=user_id, songs=song_pool)
            user_dir.mkdir()
            if user_dir.exists():
                file_path = f"stored_sessions/{user_id}/{session.id}.json"
                session = save_session(session=session, filepath=file_path)
                print("Session created!")
                advance_round(session)
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


# while session.is_active:
#     if session.current_matchup_index >= len(session.matchups):
#         engine.advance_round(session)
#         print(f'Current Round: {session.current_round}')
#         if not session.is_active: break

#     m = session.matchups[session.current_matchup_index]
#     winner_obj, _ = engine.get_matchup_result((m.song_a, m.song_b))

#     #Submit choice and Save
#     engine.submit_choice(session, winner_id=winner_obj.id)
#     save_session(session=session)

# print("🏆 Tournament Complete!")
# engine.get_ranking(session)