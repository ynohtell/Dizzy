import uuid
import json
import data_structure as dt
from typing import List
import random

K = 32

def create_session(user_id: str , songs: List[dt.Song] = None) -> dt.Session:
    song_list = songs if songs else []
    if song_list:
        paired = generate_round_1_pairs(song_list)
        paired = matchups(paired)

    return dt.Session(user_id=user_id, songs=song_list)

def generate_round_1_pairs(songs):
    # 1. Shuffle
    shuffled = random.sample(songs, len(songs))
    
    # 2. Use zip for all the perfect pairs
    # This automatically ignores the last song if the length is odd
    matchups = list(zip(shuffled[0::2], shuffled[1::2]))
    
    # 3. Handle the remainder
    if len(shuffled) % 2 != 0:
        last_song = shuffled[-1]
        # Pick anyone from the already paired songs as the opponent
        random_opponent = random.choice(shuffled[:-1])
        matchups.append((last_song, random_opponent))
        
    return matchups

def generate_round_2_pairs(songs):
    ...


def generate_round_3_pairs(songs):
    ...

def matchups(pairs):
    print('CURRENT ROUND')
    for pair in pairs:
        
        print(f'Song [1]: {pair[0].title}')
        print(f'Song [2]: {pair[1].title}')
        choice = get_user_choice(2)

        if choice == 1:
            winner, loser = pair[0], pair[1]
            print(winner.title)
            print(winner.elo_score)
        else:
            winner, loser = pair[1], pair[0]
    

# FOR MULTIPLE CHOICE
def get_user_choice(num_options):
    while True:
        try:
            # 1. Try to get and convert the input
            choice = int(input(f"Pick a song (1-{num_options}): "))
            
            # 2. Check if the number is actually in range
            if 1 <= choice <= num_options:
                return choice
            else:
                print(f"❌ Please enter a number between 1 and {num_options}.")
        except ValueError:
            # 3. This runs if int() fails (e.g., user typed "abc")
            print("⚠️ That's not a number! Try again.")
    

def update_elo(winner, loser):
    expected_winner = 1 / (1 + 10^((loser.rating - winner.rating) / 400))
    expected_loser = 1 - expected_winner

    winner.rating = winner.rating + K * (1 - expected_winner)
    loser.rating = loser.rating + K * (0 - expected_loser)

    return winner, loser


def submit_choice(session, matchup_id, winner_id):
    ...


def advance_round(session):
    ...


def get_ranking(session):
    ...


def end_session(session):
    ...


if __name__ == "__main__":
    with open('mock_tracks.json', 'r') as f:
        raw_data = json.load(f)
        f.close()

    song_pool = [
        dt.Song (
            id = item['id'],
            title = item['name'],
            artist = item['artists'][0]['name']
        )
        for item in raw_data['tracks']
    ]
        

    test = create_session(user_id=12312312, songs=song_pool)
