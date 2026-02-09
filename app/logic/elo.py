def calculate_elo(winner_elo: int, loser_elo: int) -> tuple[int, int]:

    return winner_elo + 10, loser_elo - 10
