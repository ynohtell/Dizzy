from backend.engine import get_ranking, end_session
import base_mock

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