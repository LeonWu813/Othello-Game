class Stone:
    def __init__(self, x, y, cell_length):
        self.cell_length = cell_length
        self.x = x
        self.y = y
        self.center_x = x * cell_length + cell_length // 2
        self.center_y = y * cell_length + cell_length // 2
        self.status = "empty"
        self.stone_SIZE = 35
        self.stone_OPTION_SIZE = 10
        self.DOT_WEIGHT = 1

    def display(self):
        """Display the stone base on the position and the status
        NONE -> NONE"""
        stroke(0)
        strokeWeight(self.DOT_WEIGHT)

        if self.status == "empty":
            return
        elif self.status == "option":
            fill(102)
            strokeWeight(0)
            ellipse(
                self.center_x,
                self.center_y,
                self.stone_OPTION_SIZE,
                self.stone_OPTION_SIZE,
            )
        elif self.status == "White":
            fill(225)
            ellipse(
                self.center_x,
                self.center_y,
                self.stone_SIZE,
                self.stone_SIZE,
            )
        elif self.status == "Black":
            fill(0)
            ellipse(
                self.center_x,
                self.center_y,
                self.stone_SIZE,
                self.stone_SIZE,
            )

    def change_status(self, status):
        """Change the status of the stone
        String -> None"""
        self.status = status
