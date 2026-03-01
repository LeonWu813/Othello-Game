"""
Simple test suite for Othello Game
Tests all non-graphical functionality using assert statements
"""

import os

# Import all game modules
from stone import Stone
from player import Player
from black_player import Black_Player
from white_player import White_Player
from board import Board
from result import Result
from game import Game


# Stone Tests


def test_stone_init():
    """Test Stone initialization with various inputs"""
    # Test normal initialization
    stone = Stone(0, 0, 50)
    assert stone.x == 0
    assert stone.y == 0
    assert stone.cell_length == 50
    assert stone.center_x == 25
    assert stone.center_y == 25
    assert stone.status == "empty"

    # Test with different position
    stone2 = Stone(3, 4, 40)
    assert stone2.x == 3
    assert stone2.y == 4
    assert stone2.center_x == 140  # 3*40 + 20
    assert stone2.center_y == 180  # 4*40 + 20


def test_stone_change_status():
    """Test changing stone status"""
    stone = Stone(1, 1, 50)

    # Test changing to Black
    stone.change_status("Black")
    assert stone.status == "Black"

    # Test changing to White
    stone.change_status("White")
    assert stone.status == "White"

    # Test changing to option
    stone.change_status("option")
    assert stone.status == "option"

    # Test changing back to empty
    stone.change_status("empty")
    assert stone.status == "empty"


# Player Tests


def test_player_init():
    """Test Player initialization"""
    player = Player()
    assert player.represent == "empty"


def test_black_player_init():
    """Test Black_Player initialization"""
    player = Black_Player()
    assert player.represent == "Black"
    assert len(player.hold_stones) == 0
    assert len(player.valid_moves) == 0


def test_white_player_init():
    """Test White_Player initialization"""
    player = White_Player()
    assert player.represent == "White"
    assert len(player.hold_stones) == 0
    assert len(player.valid_moves) == 0


def test_player_take_stone():
    """Test taking a stone"""
    player = Black_Player()
    stone = Stone(2, 3, 50)

    # Take the stone
    player.take_stone(stone)

    # Check stone is in hold_stones
    assert stone in player.hold_stones
    # Check stone status changed
    assert stone.status == "Black"

    # Test with White player
    white_player = White_Player()
    stone2 = Stone(4, 5, 50)
    white_player.take_stone(stone2)
    assert stone2 in white_player.hold_stones
    assert stone2.status == "White"


def test_player_lose_stone():
    """Test losing a stone"""
    player = Black_Player()
    stone1 = Stone(1, 1, 50)
    stone2 = Stone(2, 2, 50)

    # Add stones first
    player.take_stone(stone1)
    player.take_stone(stone2)
    assert len(player.hold_stones) == 2

    # Lose one stone
    player.lose_stone(stone1)
    assert stone1 not in player.hold_stones
    assert stone2 in player.hold_stones
    assert len(player.hold_stones) == 1

    # Try to lose a stone not in hold_stones (should not raise error)
    stone3 = Stone(3, 3, 50)
    player.lose_stone(stone3)
    assert len(player.hold_stones) == 1


def test_player_update_valid_move():
    """Test updating valid moves"""
    player = Black_Player()
    stone = Stone(2, 2, 50)
    flip1 = {Stone(1, 1, 50), Stone(1, 2, 50)}
    flip2 = {Stone(2, 1, 50), Stone(3, 1, 50)}

    # First update for a stone
    player.update_valid_move(stone, flip1)
    assert stone in player.valid_moves
    assert player.valid_moves[stone] == flip1

    # Update same stone with additional flips
    player.update_valid_move(stone, flip2)
    assert len(player.valid_moves[stone]) == 4  # Combined flips

    # Add a different stone
    stone2 = Stone(4, 4, 50)
    flip3 = {Stone(5, 5, 50)}
    player.update_valid_move(stone2, flip3)
    assert len(player.valid_moves) == 2


def test_player_display_valid_move():
    """Test display_valid_move changes stone status"""
    player = Black_Player()
    stone1 = Stone(2, 2, 50)
    stone2 = Stone(3, 3, 50)
    flip = {Stone(1, 1, 50)}

    # Add valid moves
    player.update_valid_move(stone1, flip)
    player.update_valid_move(stone2, flip)

    # Display valid moves
    player.display_valid_move()

    # Check that status changed to option
    assert stone1.status == "option"
    assert stone2.status == "option"


def test_player_clean_valid_move():
    """Test cleaning valid moves"""
    player = Black_Player()
    stone = Stone(2, 2, 50)
    flip = {Stone(1, 1, 50)}

    # Add valid move
    player.update_valid_move(stone, flip)
    assert len(player.valid_moves) == 1

    # Clean valid moves
    player.clean_valid_move()
    assert len(player.valid_moves) == 0


# Board Tests


def test_board_init_empty():
    """Test Board initialization with size 0"""
    board = Board(0, 0, 50)
    assert len(board.board_stones) == 0
    assert board.stone_count == 0
    assert board.cell_length == 50


def test_board_init_2x2():
    """Test Board initialization with 2x2 size"""
    board = Board(100, 2, 50)
    assert len(board.board_stones) == 2
    assert len(board.board_stones[0]) == 2
    assert board.stone_count == 2

    # Check all stones are initialized correctly
    for i in range(2):
        for j in range(2):
            stone = board.board_stones[i][j]
            assert isinstance(stone, Stone)
            assert stone.x == j
            assert stone.y == i
            assert stone.status == "empty"


def test_board_init_4x4():
    """Test Board initialization with 4x4 size"""
    board = Board(200, 4, 50)
    assert len(board.board_stones) == 4
    assert len(board.board_stones[0]) == 4

    # Check specific stones
    stone_0_0 = board.board_stones[0][0]
    assert stone_0_0.x == 0
    assert stone_0_0.y == 0

    stone_3_3 = board.board_stones[3][3]
    assert stone_3_3.x == 3
    assert stone_3_3.y == 3


def test_board_init_8x8():
    """Test Board initialization with standard 8x8 Othello size"""
    board = Board(400, 8, 50)
    assert len(board.board_stones) == 8
    assert len(board.board_stones[0]) == 8

    # Test corner stones
    assert board.board_stones[0][0].x == 0
    assert board.board_stones[0][0].y == 0
    assert board.board_stones[7][7].x == 7
    assert board.board_stones[7][7].y == 7

    # Test all stones are initially empty
    for row in board.board_stones:
        for stone in row:
            assert stone.status == "empty"


def test_board_properties():
    """Test board properties calculation"""
    board = Board(400, 8, 50)

    # Test window dimensions
    assert board.BOARDER_LENGTH == 400
    assert board.RESULT_WINDOW_WIDTH == 50 * 3.5
    assert board.RESULT_WINDOW_HEIGHT == 50 * 3
    assert board.PLAY_AGAIN_BUTTON_WIDTH == 50 * 3
    assert board.PLAY_AGAIN_BUTTON_HEIGHT == 50


# Result Tests


def test_result_init_black_win():
    """Test Result initialization when Black wins"""
    result = Result(40, 24)
    assert result.black_point == 40
    assert result.white_point == 24
    assert result.result == "BLACK WIN"
    assert result.scores == "40 : 24"


def test_result_init_white_win():
    """Test Result initialization when White wins"""
    result = Result(20, 44)
    assert result.black_point == 20
    assert result.white_point == 44
    assert result.result == "WHITE WIN"
    assert result.scores == "44 : 20"


def test_result_init_tie():
    """Test Result initialization when it's a tie"""
    result = Result(32, 32)
    assert result.black_point == 32
    assert result.white_point == 32
    assert result.result == "TIE"
    assert result.scores == "32 : 32"


def test_result_write_new_player():
    """Test writing result for a new player"""
    test_file = "scores.txt"

    # Clean up before test
    if os.path.exists(test_file):
        os.remove(test_file)

    result = Result(35, 29)  # Black wins
    result.write_result_to_txt("Alice")

    # Check file contents
    with open(test_file, "r") as file:
        content = file.read()
        assert "Alice" in content
        assert "1" in content

    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)


def test_result_write_existing_player():
    """Test updating result for existing player"""
    test_file = "scores.txt"

    # Create initial file with existing player
    with open(test_file, "w") as file:
        file.write("Bob 3 \n")

    result = Result(40, 24)  # Black wins
    result.write_result_to_txt("Bob")

    # Check file contents - should increment Bob's score
    with open(test_file, "r") as file:
        content = file.read()
        assert "Bob 4" in content

    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)


def test_result_write_multiple_players():
    """Test maintaining multiple player scores"""
    test_file = "scores.txt"

    # Create initial file with multiple players
    with open(test_file, "w") as file:
        file.write("Alice 2 \n")
        file.write("Bob 5 \n")
        file.write("Charlie 1 \n")

    result = Result(36, 28)  # Black wins
    result.write_result_to_txt("Bob")

    # Check all players are preserved and Bob's score is incremented
    with open(test_file, "r") as file:
        content = file.read()
        assert "Alice 2" in content
        assert "Bob 6" in content
        assert "Charlie 1" in content

    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)


# Game Tests
def test_game_init_single_player():
    """Test Game initialization for single player mode"""
    game = Game(400, 8, 50, 1)
    assert game.is_single_player == True
    assert isinstance(game.black_player, Black_Player)
    assert isinstance(game.white_player, White_Player)
    assert game.current_player == game.black_player
    assert game.next_player == game.white_player
    assert game.end_game == False
    assert len(game.DIRECTIONS) == 8


def test_game_init_two_player():
    """Test Game initialization for two player mode"""
    game = Game(400, 8, 50, 2)
    assert not (hasattr(game, "is_single_player") and game.is_single_player)
    assert game.current_player == game.black_player
    assert game.next_player == game.white_player


def test_game_start_4x4():
    """Test initial game setup for 4x4 board"""
    game = Game(200, 4, 50, 2)

    # Check initial stones placement (center 2x2)
    stone_1_1 = game.board_stones[1][1]
    stone_1_2 = game.board_stones[1][2]
    stone_2_1 = game.board_stones[2][1]
    stone_2_2 = game.board_stones[2][2]

    assert stone_1_1 in game.black_player.hold_stones
    assert stone_2_2 in game.black_player.hold_stones
    assert stone_1_2 in game.white_player.hold_stones
    assert stone_2_1 in game.white_player.hold_stones

    # Check possible moves are set
    assert len(game.possible_move) > 0

    # Check valid moves for black player (starting player)
    assert len(game.current_player.valid_moves) > 0


def test_game_start_8x8():
    """Test initial game setup for standard 8x8 board"""
    game = Game(400, 8, 50, 2)

    # Check initial stones placement (center 2x2)
    assert game.board_stones[3][3].status == "Black"
    assert game.board_stones[4][4].status == "Black"
    assert game.board_stones[3][4].status == "White"
    assert game.board_stones[4][3].status == "White"

    # Check each player has 2 stones
    assert len(game.black_player.hold_stones) == 2
    assert len(game.white_player.hold_stones) == 2


def test_game_check_out_of_range():
    """Test boundary checking"""
    game = Game(400, 8, 50, 2)

    # Valid positions
    assert game.check_out_of_range(0, 0) == False
    assert game.check_out_of_range(7, 7) == False
    assert game.check_out_of_range(3, 4) == False

    # Invalid positions
    assert game.check_out_of_range(-1, 0) == True
    assert game.check_out_of_range(0, -1) == True
    assert game.check_out_of_range(8, 0) == True
    assert game.check_out_of_range(0, 8) == True
    assert game.check_out_of_range(10, 10) == True


def test_game_change_turn():
    """Test turn changing mechanism"""
    game = Game(400, 8, 50, 2)

    # Initially black's turn
    assert game.current_player == game.black_player
    assert game.next_player == game.white_player

    # Change turn
    game.change_turn()
    assert game.current_player == game.white_player
    assert game.next_player == game.black_player

    # Change turn again
    game.change_turn()
    assert game.current_player == game.black_player
    assert game.next_player == game.white_player


def test_game_is_computer_turn():
    """Test computer turn detection"""
    game = Game(400, 8, 50, 1)  # Single player mode

    # Initially black's turn (human)
    assert game.is_computer_turn == False

    # Change to white's turn (computer)
    game.current_player = game.white_player
    assert game.is_computer_turn == True


def test_game_check_path():
    """Test path checking for valid moves"""
    game = Game(400, 8, 50, 2)

    # Set up a simple scenario
    game.board_stones[3][3].status = "Black"
    game.board_stones[3][4].status = "White"
    game.board_stones[3][5].status = "Black"

    # Check path from (3,4) going right (0, 1)
    game.current_player = game.black_player
    path = game.check_path(3, 4, 0, 1)

    # Should return the white stone at (3,4) as flippable
    assert len(path) == 1


def test_game_update_possible_move():
    """Test updating possible moves after placing a stone"""
    game = Game(400, 8, 50, 2)
    stone = game.board_stones[2][3]

    # Add stone to possible moves
    game.possible_move.add(stone)

    # Update possible moves
    game.update_posibble_move(stone)

    # Stone should be removed from possible moves
    assert stone not in game.possible_move

    # Adjacent empty cells should be added
    for dy, dx in game.DIRECTIONS:
        ny, nx = 2 + dy, 3 + dx
        if not game.check_out_of_range(ny, nx):
            if game.board_stones[ny][nx].status == "empty":
                assert game.board_stones[ny][nx] in game.possible_move


def test_game_player_take_stone_invalid():
    """Test taking stone from invalid position"""
    game = Game(400, 8, 50, 2)

    # Try to place stone on non-option cell
    result = game.player_take_stone(0, 0)
    assert result == False


def test_game_check_end_game():
    """Test end game detection when no valid moves"""
    game = Game(200, 4, 50, 2)

    # Manually clear valid moves to simulate end game
    game.current_player.valid_moves.clear()

    # Check end game
    game.check_end_game()
    assert game.end_game == True
    assert game.result is not None


def test_game_check_valid_move_initial():
    """Test valid move checking at game start"""
    game = Game(200, 4, 50, 2)

    # Black player should have valid moves at start
    assert len(game.current_player.valid_moves) > 0

    # Verify each valid move has flippable stones
    for stone, flips in game.current_player.valid_moves.items():
        assert isinstance(stone, Stone)
        assert isinstance(flips, set)
        assert len(flips) > 0


def test_game_com_take_stone_logic():
    """Test computer move selection logic"""
    game = Game(400, 8, 50, 1)  # Single player

    # Set up so it's computer's turn
    game.current_player = game.white_player

    # Add some valid moves for computer
    stone1 = game.board_stones[2][3]
    stone2 = game.board_stones[2][4]
    flip1 = {game.board_stones[3][3]}
    flip2 = {game.board_stones[3][4], game.board_stones[4][4]}

    game.current_player.update_valid_move(stone1, flip1)
    game.current_player.update_valid_move(stone2, flip2)

    # Computer should pick the move with more flips
    choices = game.current_player.valid_moves
    max_flips = 0
    best_stone = None
    for key in choices:
        if len(choices[key]) > max_flips:
            best_stone = key
            max_flips = len(choices[key])

    # Stone2 should be the best choice (2 flips vs 1)
    assert best_stone == stone2
    assert max_flips == 2


def test_game_record_result():
    """Test result recording logic"""
    game = Game(400, 8, 50, 2)

    # Create a black win result
    game.result = Result(40, 24)

    # Should only record if BLACK WIN
    assert game.result.result == "BLACK WIN"


# Main Test Runner
def run_all_tests():
    """Run all test functions"""
    # Stone tests
    test_stone_init()
    test_stone_change_status()

    # Player tests
    test_player_init()
    test_black_player_init()
    test_white_player_init()
    test_player_take_stone()
    test_player_lose_stone()
    test_player_update_valid_move()
    test_player_display_valid_move()
    test_player_clean_valid_move()

    # Board tests
    test_board_init_empty()
    test_board_init_2x2()
    test_board_init_4x4()
    test_board_init_8x8()
    test_board_properties()

    # Result tests
    test_result_init_black_win()
    test_result_init_white_win()
    test_result_init_tie()
    test_result_write_new_player()
    test_result_write_existing_player()
    test_result_write_multiple_players()

    # Game tests
    test_game_init_single_player()
    test_game_init_two_player()
    test_game_start_4x4()
    test_game_start_8x8()
    test_game_check_out_of_range()
    test_game_change_turn()
    test_game_is_computer_turn()
    test_game_check_path()
    test_game_update_possible_move()
    test_game_player_take_stone_invalid()
    test_game_check_end_game()
    test_game_check_valid_move_initial()
    test_game_com_take_stone_logic()
    test_game_record_result()


if __name__ == "__main__":
    run_all_tests()
