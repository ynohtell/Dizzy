from app import get_ranking, end_session, create_session, advance_round
import pytest


def test_create_session_success(song_pool):
    """Verify session creation with valid data"""
    user_id = "test_dev"
    session = create_session(user_id=user_id, songs=song_pool)

    assert session.user_id == user_id
    assert len(session.songs) == len(song_pool)
    assert session.is_active == True 


@pytest.mark.parametrize("invalid_user, expected_msg", [
    (" ", "Driver Error"),      # Empty String
    (None, "Driver Error"),     # None Type
    (" ", "Driver Error"),      # Just whitespace
])

def test_create_session_fails_no_user(invalid_user, expected_msg, song_pool):
    """Verify error when user_id is missing"""
    with pytest.raises(ValueError, match=expected_msg):
        create_session(user_id=invalid_user, songs=song_pool)
    # Useful for handling non-valid entry


@pytest.mark.parametrize("invalid_songs, expected_msg", [
    ([], "at least 2 songs"),       # Empty list
    ([1], "at least 2 songs"),      # Only one song
    (None, "at least 2 songs"),     # None Type

])

def test_create_session_fails_min_songs(invalid_songs, expected_msg, song_pool):
    """Verify error when less than 2 songs are provided"""
    tiny_pool = [song_pool[0]]

    with pytest.raises(ValueError, match=expected_msg):
        create_session(user_id="dev", songs=invalid_songs)


def test_create_session_happy_path(song_pool):
    """Verify that valid data from our JSON actually creates a session."""
    session = create_session(user_id="pro_dev", songs=song_pool)
    
    assert session.is_active is True
    assert len(session.songs) == len(song_pool)
    assert isinstance(session.id, str) # Verify UUID generation


def test_get_ranking_order(mock_session, capsys):
    """
    QA Goal: Verify that the ranking logic correctly sorts 
    songs by ELO rating in descending order.
    """
    
    ranked_list = get_ranking(mock_session)
    print(f"DEBUG: Song count is {len(mock_session.songs)}")
    assert len(ranked_list) > 0, "Error, The list is empty!"
    assert ranked_list[0].rating >= ranked_list[-1].rating, "Error: Not sorted correctly!"
    captured = capsys.readouterr()


    # print(captured.out)
    assert "1. High Rated" in captured.out
    assert "2. Mid Rated" in captured.out
    assert "3. Low Rated" in captured.out


def test_end_session(mock_session):
    mock_session.is_active = True # Making sure it was true first
    results = end_session(mock_session)
    assert mock_session.is_active is False, "The session should be inactive after ending."