import pytest 
from app import Session

def test_session_persistence_lifecycle(mock_session):
    # Simulate saving the game to a database
    saved_data = mock_session.model_dump_json()

    # Simulate the server restarting
    reloaded_session = Session.model_validate_json(saved_data)

    assert reloaded_session.id == mock_session.id
    assert reloaded_session.current_matchup_index == mock_session.current_matchup_index
    assert reloaded_session.songs[0].rating == mock_session.songs[0].rating

    assert isinstance(reloaded_session, Session)