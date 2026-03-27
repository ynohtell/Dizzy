from app import get_ranking, end_session, create_session, advance_round, submit_choice
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


def test_submit_choice():
    ...


def test_advance_round_completes_at_round_4(song_pool):
    # Arrange: Setup a session sitting at the end of Round 3
    session = create_session(user_id="dev", songs=song_pool)
    session.current_round = 3 
    
    # Act: Advance to Round 4
    advance_round(session)
    
    # Assert: Verify the "Tournament Complete" state
    assert session.current_round == 4
    assert session.is_active is False 
    assert session.current_matchup_index == 0


def test_advance_round_generates_matchups(song_pool):
    # Arrange: Starts at Round 0
    session = create_session(user_id="dev", songs=song_pool)
    
    # Act: Move to Round 1
    advance_round(session)
    
    # Assert: Verify Round 1 state
    assert session.current_round == 1
    assert len(session.matchups) > 0  # Verify logic actually ran
    assert session.is_active is True


def test_get_ranking_order(mock_session):
    """
    QA Goal: Verify that the ranking logic correctly sorts 
    songs by ELO rating in descending order.
    """
    
    ranked_list = get_ranking(mock_session)
    
    # 1. Verify we have the expected number of items
    assert len(ranked_list) == 3, f"Expected 3 songs, but got {len(ranked_list)}"
    
    # 2. Verify the exact order by checking the names/titles of the objects.
    # (Note: Change '.title' to whatever attribute your song object uses, like '.name')
    assert ranked_list[0].title == "High Rated", f"Expected 'High Rated', got {ranked_list[0].title}"
    assert ranked_list[1].title == "Mid Rated", f"Expected 'Mid Rated', got {ranked_list[1].title}"
    assert ranked_list[2].title == "Low Rated", f"Expected 'Low Rated', got {ranked_list[2].title}"

    # 3. Verify the mathematical sorting logic directly
    # Checking [0] against [-1] only checks the ends. It's better to ensure 
    # the whole list is strictly descending.
    assert ranked_list[0].rating >= ranked_list[1].rating, "Item 0 should be >= Item 1"
    assert ranked_list[1].rating >= ranked_list[2].rating, "Item 1 should be >= Item 2"


def test_end_session(mock_session):
    mock_session.is_active = True # Making sure it was true first
    results = end_session(mock_session)
    assert mock_session.is_active is False, "The session should be inactive after ending."