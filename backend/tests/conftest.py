import pytest
from app import Song, Session
from pathlib import Path
import json

@pytest.fixture
def mock_session():
    songs = [
        Song(id="1", title="Low Rated", artist="A", rating=800),
        Song(id="2", title="High Rated", artist="B", rating=1500),
        Song(id="3", title="Mid Rated", artist="C", rating=1200)
    ]
    return Session(user_id="dev_user", songs=songs)

@pytest.fixture
def song_pool():
    # Find the directory where THIS file is located
    current_dir = Path(__file__).parent
    json_path = current_dir / "fixtures" / "mock_tracks.json"

    with open(json_path) as f:
        data = json.load(f)

    return [
        Song(id=item['id'], title=item['name'], artist=item['artists'][0]['name'])
        for item in data['tracks']
    ]
