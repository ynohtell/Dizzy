import data_structure as dt
from typing import List
import random

K = 32

def create_session(user_id: str , songs: List[dt.Song]) -> dt.Session:
    if not songs or len(songs) < 2:
        raise ValueError("⛽ Engine Error: You need at least 2 songs to start a matchup!")

    if not user_id:
        raise ValueError("👤 Driver Error: No user_id provided.")


    return dt.Session(
        user_id=user_id,
        songs=songs,
        is_active=True,
    )


def matchup_pairing(session, pairs, round_number):
    if pairs is None:
        return []
    
    return [
        dt.Matchup(song_a=p[0], song_b=p[1], round_number=round_number)
        for p in pairs 
    ]

def generate_round_1_pairs(songs):
    # 1. Shuffle
    shuffled = random.sample(songs, len(songs))
    
    # 2. Use zip for all the perfect pairs
    # This automatically ignores the last song if the length is odd
    paired = list(zip(shuffled[0::2], shuffled[1::2]))
    
    # 3. Handle the remainder
    if len(shuffled) % 2 != 0:
        last_song = shuffled[-1]
        # Pick anyone from the already paired songs as the opponent
        random_opponent = random.choice(shuffled[:-1])
        paired.append((last_song, random_opponent))
    
        
    return paired

def generate_round_2_pairs(songs):
    # 1. Sort by rating
    sorted_songs = sorted(songs, key=lambda s: s.rating, reverse=True)
    
    matchups = []
    
    # 2. Extract Wildcard (Rank 1 vs Rank 10)
    # Be careful: Ensure you have at least 10 songs!
    if len(sorted_songs) >= 10:
        rank_1 = sorted_songs.pop(0)  # Remove first
        rank_10 = sorted_songs.pop(8) # Remove what was index 9 (now 8)
        matchups.append((rank_1, rank_10))
    
    # 3. Pair the rest adjacently (1v2, 3v4...)
    # We use the same 'zip' trick you learned today!
    matchups.extend(list(zip(sorted_songs[0::2], sorted_songs[1::2])))
    
    # 4. Handle odd numbers (if any remain)
    if len(sorted_songs) % 2 != 0:
        # Give the last person a random opponent from the already paired group
        # (excluding the wildcard songs)
        matchups.append((sorted_songs[-1], random.choice(sorted_songs[:-1])))
        
    return matchups


def generate_round_3_pairs(songs):
    # 1. Sort by rating (Gasoline)
    sorted_songs = sorted(songs, key=lambda s: s.rating, reverse=True)
    
    matchups = []

    # 2. Extract Wildcard (Rank 2 vs Rank 9)
    # Python indices: Rank 2 is index 1, Rank 9 is index 8
    if len(sorted_songs) >= 9:
        # Note: Pop the higher index first so the lower index doesn't shift!
        rank_9 = sorted_songs.pop(8) 
        rank_2 = sorted_songs.pop(1)
        matchups.append((rank_2, rank_9))

    # 3. Pair remaining adjacently
    matchups.extend(list(zip(sorted_songs[0::2], sorted_songs[1::2])))

    # 4. Final Odd-One-Out check
    if len(sorted_songs) % 2 != 0:
        matchups.append((sorted_songs[-1], random.choice(sorted_songs[:-1])))

    return matchups


def get_matchup_result(pair):
    """Handles exactly one matchup and returns the outcome."""
    print(f"\nSong [1]: {pair[0].title}")
    print(f"Song [2]: {pair[1].title}")

    choice = get_user_choice(2)

    if choice == 1:
        return pair[0], pair[1]
    else:
        return pair[1], pair[0]


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
    expected_winner = 1 / (1 + 10 ** ((loser.rating - winner.rating) / 400))
    expected_loser = 1 - expected_winner

    winner.rating = winner.rating + K * (1 - expected_winner)
    loser.rating = loser.rating + K * (0 - expected_loser)

    return winner, loser


def submit_choice(session, winner_id):
    # 1. Get the current matchup using the 'Bookmark' index
    if session.current_matchup_index >= len(session.matchups):
        print("Round already finished!")
        return

    current_match = session.matchups[session.current_matchup_index]
    
    # 2. Assign the winner inside the Matchup object
    current_match.winner_id = winner_id
    
    # 3. Handle ELO (Logic you've already written)
    # Identify objects based on ID
    if current_match.song_a.id == winner_id:
        winner, loser = current_match.song_a, current_match.song_b
    else:
        winner, loser = current_match.song_b, current_match.song_a
        
    update_elo(winner, loser)

    # 4. CRITICAL: Move the bookmark forward
    session.current_matchup_index += 1
    
    # Check if we need to end the round or the game
    if session.current_matchup_index == len(session.matchups):
        print("All matchups in this round are done!")


def advance_round(session):
    session.current_round += 1
    print(f"Current Round: {session.current_round}")
    session.current_matchup_index = 0

    if session.current_round > 3:
        session.is_active = False
        print("🏆 Tournament Complete!")
        return 
    
    rounds = [generate_round_1_pairs, generate_round_2_pairs, generate_round_3_pairs]
    round_func = rounds[session.current_round - 1]

    raw_pairs = round_func(session.songs)

    session.matchups = matchup_pairing(session, raw_pairs, session.current_round)


# def get_next_available_match(session: Session) -> Optional[Matchup]:
#     for matchup in session.matchups:
#         if matchup.winner_id is None:
#             return matchup
#     return None # All matches in this round are done!


def get_ranking(session):
    ...


def end_session(session):
    #  mark complete, return final ranking
    #  save playlist
    session.is_active = False
    ...