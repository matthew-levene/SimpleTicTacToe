# Tic-Tac-Toe Game
#
# Tic-Tac-Toe is a board game that consists of nine squares.

# In each round, the player will pick a square to place their marker
# In each alternate round, the computer will pick a free square
#
# The player may choose if they wish to use Xs or Os
#
# The game will end if:
#  > The player or the computer gets three horizontal or vertical squares in a row
#  > The board is filled and the result is a draw

from board import Board

if __name__ == '__main__':
    board = Board()
