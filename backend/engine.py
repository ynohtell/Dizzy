K = 32

def create_session(user_id, songs):
    ...

def generate_round_1_pairs(songs):
    ...


def generate_round_2_pairs(songs):
    ...


def generate_round_3_pairs(songs):
    ...


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
