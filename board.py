from stone import Stone


class Board:
    def __init__(self, board_length, stone_count, cell_length):
        self.BOARDER_STROKE = 2
        self.BOARDER_LENGTH = board_length
        self.stone_count = stone_count
        self.cell_length = cell_length
        self.board_stones = [
            [Stone(j, i, cell_length) for j in range(self.stone_count)]
            for i in range(self.stone_count)
        ]
        self.RESULT_WINDOW_WIDTH = cell_length * 3.5
        self.RESULT_WINDOW_HEIGHT = cell_length * 3
        self.RESULT_WINDOW_RADIUS = 20
        self.NAME_INPUT_RADIUS = 8
        self.PLAY_AGAIN_BUTTON_WIDTH = cell_length * 3
        self.PLAY_AGAIN_BUTTON_HEIGHT = cell_length
        self.RESULT_TEXT_SIZE = 32

    def display(self):
        """Display the board
        None -> None"""
        background(232, 196, 160)
        stroke(51)
        strokeWeight(self.BOARDER_STROKE)
        for i in range(self.stone_count + 1):
            line(
                i * self.cell_length,
                0,
                i * self.cell_length,
                self.BOARDER_LENGTH,
            )
            line(
                0,
                i * self.cell_length,
                self.BOARDER_LENGTH,
                i * self.cell_length,
            )

    def update_board_stone(self):
        """display all the stones in the board base on the position and status
        NONE -> NONE"""
        for i in self.board_stones:
            for j in i:
                j.display()

    def show_result(self, result, name):
        """Show the result of the winner
        Result -> NONE"""
        strokeWeight(0)
        fill(204)
        rect(
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_WIDTH) / 2,
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_HEIGHT) / 2,
            self.RESULT_WINDOW_WIDTH,
            self.RESULT_WINDOW_HEIGHT,
            self.RESULT_WINDOW_RADIUS,
            self.RESULT_WINDOW_RADIUS,
            self.RESULT_WINDOW_RADIUS,
            self.RESULT_WINDOW_RADIUS,
        )
        textSize(self.RESULT_TEXT_SIZE)
        fill(0)
        textAlign(CENTER, TOP)
        text(
            result.result,
            self.BOARDER_LENGTH / 2,
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_HEIGHT) / 2
            + self.RESULT_TEXT_SIZE * 0.5,
        )
        text(
            result.scores,
            self.BOARDER_LENGTH / 2,
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_HEIGHT) / 2
            + self.RESULT_TEXT_SIZE * 1.5,
        )
        fill(204)
        strokeWeight(3)
        rect(
            (self.BOARDER_LENGTH - self.PLAY_AGAIN_BUTTON_WIDTH) / 2,
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_HEIGHT) / 2
            + self.RESULT_TEXT_SIZE * 2.5,
            self.PLAY_AGAIN_BUTTON_WIDTH,
            self.PLAY_AGAIN_BUTTON_HEIGHT,
            self.NAME_INPUT_RADIUS,
            self.NAME_INPUT_RADIUS,
            self.NAME_INPUT_RADIUS,
            self.NAME_INPUT_RADIUS,
        )
        fill(0)
        textSize(22)
        text(
            name,
            self.BOARDER_LENGTH / 2,
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_HEIGHT) / 2
            + self.RESULT_TEXT_SIZE * 3,
        )
        textSize(16)
        text(
            'Type your name and press "Enter" to restart!',
            self.BOARDER_LENGTH / 2,
            (self.BOARDER_LENGTH - self.RESULT_WINDOW_HEIGHT) / 2
            + self.RESULT_TEXT_SIZE * 4.2,
        )
