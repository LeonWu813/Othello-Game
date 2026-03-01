from player import Player


class Black_Player(Player):
    def __init__(self):
        self.hold_stones = set()
        self.valid_moves = {}
        self.represent = "Black"
