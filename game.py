from board import Board
from black_player import Black_Player
from white_player import White_Player
from result import Result


class Game:
    """Game of the Othello"""

    def __init__(self, board_length, stone_count, cell_length, players):
        self.DIRECTIONS = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]
        if players == 1:
            self.is_single_player = True
        else:
            self.is_single_player = False
        self.DELAY = 2
        self.SETUP = 2
        self.black_player = Black_Player()
        self.white_player = White_Player()
        self.possible_move = set()
        self.current_player, self.next_player = self.black_player, self.white_player
        self.board = Board(board_length, stone_count, cell_length)
        self.board_stones = self.board.board_stones
        self.stone_count = stone_count
        self.end_game = False
        self.result = None
        self.start_game()

    def start_game(self):
        """Display the initial black & white stones and update the posiible move
        None -> None"""
        middle = self.stone_count // 2 - 1
        for i in range(self.SETUP):
            self.player_take_stone(middle + i, middle + i, self.black_player)
            self.player_take_stone(middle + 1 - i, middle + i, self.white_player)

        for i in range(self.SETUP + 1):
            self.possible_move.add(self.board_stones[middle - 1][middle + i])
            self.possible_move.add(self.board_stones[middle + i][middle + 2])
            self.possible_move.add(self.board_stones[middle + 2][middle + 1 - i])
            self.possible_move.add(self.board_stones[middle - 1 + i][middle - 1])

        self.check_valid_move()
        self.current_player.display_valid_move()

    def update(self):
        """Dispay the updated version of the game
        None -> None"""
        self.board.display()
        self.board.update_board_stone()

    def player_take_stone(self, y, x, isCurrentPlayer=False, isComMove=False):
        """Check if the player put the stone of the valid move and take it with the opponent stones between
        INT, INT, CLASS Player -> NONE"""

        stone = self.board_stones[y][x]
        if isCurrentPlayer:
            player = isCurrentPlayer
            player.take_stone(stone)
            return False

        if stone.status == "option" or isComMove:
            player = self.current_player
            if stone not in player.valid_moves:
                return False
            flip = player.valid_moves[stone]
            for i in flip:
                self.current_player.take_stone(i)
                self.next_player.lose_stone(i)
            player.take_stone(stone)
            self.update_posibble_move(stone)
            self.change_turn()
            return True
        return False

    def change_turn(self):
        """Change player turn and update the valid move of the next player
        None -> None
        """
        self.current_player, self.next_player = self.next_player, self.current_player
        self.check_valid_move()
        if self.is_computer_turn:
            return
        self.current_player.display_valid_move()

    @property
    def is_computer_turn(self):
        """To check if it is computer's turn
        NONE -> Bool"""
        if self.is_single_player and self.current_player == self.white_player:
            return True
        else:
            return False

    def com_take_stone(self):
        """To check if it is computer's turn
        NONE -> Bool"""
        choices = self.current_player.valid_moves
        max = 0
        find_optimal = []
        for key in choices:
            if len(choices[key]) > max:
                find_optimal.insert(0, key)
                max = len(choices[key])
        picked_stone = find_optimal[0]
        self.player_take_stone(picked_stone.y, picked_stone.x, False, True)

    def check_valid_move(self):
        """Check the current player valid moves from the possible moves
        NONE -> NONE"""
        self.current_player.clean_valid_move()
        for i in self.possible_move:
            flip = set()
            y = i.y
            x = i.x
            for addy, addx in self.DIRECTIONS:
                newy = y + addy
                newx = x + addx
                if self.check_out_of_range(newy, newx):
                    continue

                if self.board_stones[newy][newx].status == self.next_player.represent:
                    flip.update(self.check_path(newy, newx, addy, addx))

            if flip:
                self.current_player.update_valid_move(i, flip)
        self.check_end_game()

    def check_path(self, y, x, addy, addx):
        """Helper functions for check_valid_move() for checking one of the direciton of the stone
        INT, INT, INT, INT -> SET"""
        path = set()
        while True:
            if self.check_out_of_range(y, x):
                return set()
            elif self.board_stones[y][x].status == "empty":
                return set()
            elif self.board_stones[y][x].status == self.current_player.represent:
                return path
            else:
                path.add(self.board_stones[y][x])
                y += addy
                x += addx

    def check_out_of_range(self, y, x):
        """
        Helper function to check if the given position is out of range of the board
        INT, INT -> BOOL
        """
        if y < 0 or y > self.stone_count - 1 or x < 0 or x > self.stone_count - 1:
            return True
        else:
            return False

    def update_posibble_move(self, stone):
        """
        Helper function to update the possible_move from the empty cells that have at least one stone in one of eight direction
        CLASS Stone -> None"""
        y = stone.y
        x = stone.x
        self.possible_move.remove(stone)
        for addy, addx in self.DIRECTIONS:
            newy = y + addy
            newx = x + addx
            if self.check_out_of_range(newy, newx):
                continue

            if self.board_stones[newy][newx].status == "empty":
                self.possible_move.add(self.board_stones[newy][newx])

        for i in self.possible_move:
            i.status = "empty"

    def check_end_game(self):
        """count the rest of the space in the board, end game if it's empty space left
        NONE -> NONE"""
        if len(self.current_player.valid_moves) == 0:
            for i in self.board_stones:
                for j in i:
                    if j.status == "empty":
                        j.status = self.next_player.represent

            current_player_point = len(self.current_player.hold_stones)
            next_player_point = (
                self.stone_count * self.stone_count - current_player_point
            )

            print(
                self.current_player.represent,
                current_player_point,
                self.next_player.represent,
                next_player_point,
            )

            if self.current_player == self.black_player:
                result = Result(current_player_point, next_player_point)
            else:
                result = Result(next_player_point, current_player_point)

            self.end_game = True
            self.result = result

    def show_game_result(self, name=""):
        self.board.show_result(self.result, name)

    def record_result(self, name=""):
        if self.result.result == "BLACK WIN":
            self.result.write_result_to_txt(name)
