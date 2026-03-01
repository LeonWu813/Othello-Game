from player import Player


class White_Player(Player):
    def __init__(self):
        self.hold_stones = set()
        self.valid_moves = {}
        self.represent = "White"
