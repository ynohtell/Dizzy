import pytest
from backend.data_structure import Song, Session

@pytest.fixture
def mock_session():
    songs = [
        Song(id="1", title="Low Rated", artist="A", rating=800),
        Song(id="2", title="High Rated", artist="B", rating=1500),
        Song(id="3", title="Mid Rated", artist="C", rating=1200)
    ]
    return Session(user_id="dev_user", songs=songs)