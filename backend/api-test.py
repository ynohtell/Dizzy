import requests as req

BASE_URL = 'http://127.0.0.1:8000/'
USER_ID = 'test_dev1'

resp = req.post(f"{BASE_URL}/sessions/create?user_id={USER_ID}")

if resp.status_code != 200:
    exit()
session = resp.json()
s_id = session['id']
print(f'Session ID: {s_id}')

for i in range(30):
    # 1. Get Matchup
    match_resp = req.get(f"{BASE_URL}/sessions/{USER_ID}/{s_id}/matchup")
    print(match_resp.text)
    match = match_resp.json()
   
    song_a = match['song_a']['id']
    
    # 2. Vote
    vote = req.post(f"{BASE_URL}/sessions/{USER_ID}/{s_id}/choose?winner_id={song_a}")
    
    if vote.status_code == 200:
        track = vote.json()
        print(f"Voted! Round: {track['current_round']}, Index: {track['current_matchup_index']}")
        
        # If the backend set is_active to False, stop the loop
        if not track.get('is_active', True):
            print("🏁 Tournament finished. Fetching final rankings...")
            ranking = req.get(f"{BASE_URL}/sessions/{USER_ID}/{s_id}/ranking").json()
            for index, song  in enumerate(ranking):
                print(f'{index} Title: {song['title']} - {song['artist']} Rating: {song['rating']}')
            break


