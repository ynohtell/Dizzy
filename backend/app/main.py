import json
import engine
from pathlib import Path

current_dir = Path(__file__).parent.parent
json_path = current_dir / "tests" / "fixtures" / "mock_tracks.json"
print(json_path)

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
    session = engine.create_session(user_id="user_dev123", songs=song_pool)
    print(f"✅ Engine started! Session ID: {session.id}")
    while session.is_active:
        if session.current_round == 0:
            engine.advance_round(session)

        if session.current_matchup_index < len(session.matchups):

            m = session.matchups[session.current_matchup_index]

            winner_obj, loser_obj = engine.get_matchup_result((m.song_a, m.song_b))

            engine.submit_choice(session, winner_id=winner_obj.id)
        else:
            engine.advance_round(session)

except ValueError as e:
    print(f"❌ {e}")
