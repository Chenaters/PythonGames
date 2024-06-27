from tkinter import *

class Piece:
    # what piece, alive or dead, black or whit
    def __init__(self, pos, color, board):
        """pos is position list
        color is int 0 for white 1 for black"""
        self.board = board
        self.color = color
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def getcolor(self):
        return self.color

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(self, pos, color, board)

    def possible_moves(self,board):
        outputs = []


        if self.color == 0: # white
            x = self.x
            y = self.y
            if y == 2: # 2 moves first
                if not board.is_piece((x+2, y)):
                    outputs.append((x+2, y))
            if not board.is_piece((x+1, y)):
                outputs.append((x+1, y))
            if board.is_piece((x+1, y+1)):
                outputs.append((x+1, y+1))
            elif:


        else:

    def move_piece(self, pos):



class Rook(Piece):

class Knight(Piece):

class Bishop(Piece):

class Queen(Piece):

class King(Piece):


class Tile:
    #piece on tile
    def __init__(self, piece):
        """Piece is a piece class
        color is 0 for white 1 for black"""
        self.piece = piece


class Board:
    # consists of tiles, where pieces go, whos turn
    def __init__(self):
        self.board = [[Rook((1,8),1, Board), Knight(1), Bishop(1), Queen(1), King(1), Bishop(1), Knight(1), Rook(1)],
                      [Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0)],
                      [Rook(0), Knight(0), Bishop(0), Queen(0), King(0), Bishop(0), Knight(0), Rook(0)]]
        self.turn = 0


    def setup(self):
        """Sets the board"""

    def is_piece(self, pos):
        """Is there a piece at the position,
        return boolean"""

        # (
        x = pos[0] #(1,8)
        y = pos[1]
        if self.board[x - 1][-y] is None:
            return False
        else:
            return True




class Player:
    # consists of whos move
    def __init__(self, color):
        self.color = color


class Game:
    # convert board to view, get players turns, input moves












