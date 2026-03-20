import requests as req

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "test_user_1"

resp = req.post(f"{BASE_URL}/sessions/create?user_id={USER_ID}")

if resp.status_code != 200:
    print(f"Error {resp.status_code}: {resp.text}")
    exit()

session = resp.json()

s_id = session['id']
print(f"Created session: {s_id}")

round_match = 1
# 2. Play 3 Rounds
for i in range(3):
    # Get Matchup
    match = req.get(f"{BASE_URL}/sessions/{USER_ID}/{s_id}/matchup").json()
    song_a = match['song_a']['id']
    song_b = match['song_b']['id']
    round_num = match['round_number']
    
    print(f"Round {round_num}: {match['song_a']['title']} vs {match['song_b']['title']}")
    
    # Vote for Song A every time just to test
    vote = req.post(f"{BASE_URL}/sessions/{USER_ID}/{s_id}/choose?winner_id={song_a}")
    print(f"Vote status: {vote.status_code}: {vote.text}")
    track = resp.json()
    print(f"Match index {track['current_matchup_index']}")

# 3. Check Ranking
ranking = req.get(f"{BASE_URL}/sessions/{USER_ID}/{s_id}/ranking")
print("Final Rankings:", ranking.json())