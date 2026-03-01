class Player:
    def __init__(self):
        self.represent = "empty"

    def take_stone(self, stone):
        """Take the stone and added to the hold_stone list
        CLASS Stone -> NONE"""
        self.hold_stones.add(stone)
        stone.change_status(self.represent)

    def lose_stone(self, stone):
        """Lose the stone and removed from the hold_stone list
        CLASS Stone -> NONE"""
        if stone in self.hold_stones:
            self.hold_stones.remove(stone)

    def update_valid_move(self, stone, flips):
        """update the dictionary of the valid move. Key = valid move cell, Values = list of the stone would take if player put stone on this position
        CLASS stone, LIST -> NONE"""
        if stone in self.valid_moves:
            self.valid_moves[stone].update(flips)
        else:
            self.valid_moves[stone] = flips

    def display_valid_move(self):
        """display the valid move dictionary
        NONE -> NONE"""
        for i in self.valid_moves:
            i.status = "option"

    def clean_valid_move(self):
        """clean the valid move dictionary
        NONE -> NONE"""
        self.valid_moves.clear()
