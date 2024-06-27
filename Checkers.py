from tkinter import *


class CheckersSquare(Canvas):
    def __init__(self, master, c, r, squareColor):
        Canvas.__init__(self, master, height=50, width=50, highlightthickness=0, bg=squareColor)
        self.grid(row=r, column=c)
        # set the attributes
        self.position = (r, c)
        self.isKing = False
        # bind button click to placing a piece
        self.bind('<Button>', master.get_click)

    def get_position(self):
        '''CheckersSquare.get_position() -> (int, int)
        returns (row, column) of square'''
        return self.position

    def place_piece(self, piece):  # input of color and king status
        """CheckersSquare.place_piece(color)
        Places a circle of color"""
        color = ["white", "black"]
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        if piece != "Empty":
            if piece[1] == 0:  # create piece
                self.create_oval(8, 8, 42, 42, fill=color[piece[0]])
            else:  # create white king
                self.create_oval(4, 4, 21, 21, fill=color[piece[0]])
                self.is_king()
        # TODO make king special looking

    def is_king(self):
        """CheckersSquare.return_king()
        Returns True if piece is a king"""
        return self.isKing

    def king(self):
        """CheckersSquare.king()
        Makes piece a king"""
        self.isKing = True

    def remove_piece(self):
        """CheckersSquare.remove_piece()
        Removes the piece on a square"""
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)


class CheckersBoard:
    def __init__(self):
        """CheckersBoard()
        The info for a checkersBoard"""
        self.board = {}  # dict to store position
        # create opening position
        # first index means whihc player second index is if its kinged
        count = 0
        for row in range(1, 9):
            count += 1
            for column in range(1, 9):
                coords = (row, column)
                if (column in [1, 2, 3]) and ((count % 2) == 0):
                    self.board[coords] = [1, 0]  # player 1 not king
                elif (column in [6, 7, 8]) and ((count % 2) == 0):
                    self.board[coords] = [0, 0]  # player 0 not king
                else:
                    self.board[coords] = "Empty"  # empty
                count += 1
        self.board[2, 5] = [1, 0]

        self.currentPlayer = 0  # player 0 starts

    def get_piece(self, coords):
        '''CheckersBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer

    def forced_moves(self):
        '''CheckersBoard.forced_moves(player)
        Returns a list of forced moves for a player'''

        # TODO make this work for top side and bottom side
        # TODO make sure to check for open spaces when taking
        forced_moves = []

        # go through the coordinates and find the forced moves
        # ((2,5),(3,4)) 1st is coord of piece 2nd is piece its capturing
        for coord in self.board:
            if self.board[coord][0] == self.currentPlayer and self.currentPlayer == 1:  # black to play
                if self.board[coord][1] == 1:  # piece is a king
                    left_top_side = (coord[0] - 1, coord[1] + 1)
                    right_top_side = (coord[0] + 1, coord[1] + 1)
                    left_bottom_side = (coord[0] - 1, coord[1] - 1)
                    right_bottom_side = (coord[0] + 1, coord[1] - 1)
                    coords = [left_top_side, right_top_side, left_bottom_side, right_bottom_side]
                    coords = self.remove_outer(coords)
                    for option in coords:
                        if self.board[option][0] == ((self.currentPlayer + 1) % 2):  # if enemy
                            forced_moves.append((coord, option))
                else:  # piece ins't a king
                    left_side = (coord[0] - 1, coord[1] + 1)
                    right_side = (coord[0] + 1, coord[1] + 1)
                    coords = [left_side, right_side]
                    coords = self.remove_outer(coords)
                    for option in coords:
                        if self.board[option][0] == ((self.currentPlayer + 1) % 2):  # if enemy
                            forced_moves.append((coord, option))
            elif self.board[coord][0] == self.currentPlayer and self.currentPlayer == 0:  # white to play
                if self.board[coord][1] == 1:  # piece is a king
                    left_top_side = (coord[0] - 1, coord[1] + 1)
                    right_top_side = (coord[0] + 1, coord[1] + 1)
                    left_bottom_side = (coord[0] - 1, coord[1] - 1)
                    right_bottom_side = (coord[0] + 1, coord[1] - 1)
                    coords = [left_top_side, right_top_side, left_bottom_side, right_bottom_side]
                    coords = self.remove_outer(coords)
                    for option in coords:
                        if self.board[option][0] == ((self.currentPlayer + 1) % 2):  # if enemy
                            forced_moves.append((coord, option))
                else:  # piece ins't a king
                    left_side = (coord[0] - 1, coord[1] - 1)
                    right_side = (coord[0] + 1, coord[1] - 1)
                    coords = [left_side, right_side]
                    coords = self.remove_outer(coords)
                    for option in coords:
                        if self.board[option][0] == ((self.currentPlayer + 1) % 2):  # if enemy
                            forced_moves.append((coord, option))
            # TODO this doesn't check if a capture will lead outside of teh board or if the capture is even possible

        # check if capturing goes out of the board
        for capture in forced_moves:
            direction_y = capture[1][1]-capture[0][1]
            direction_x = capture[1][0]-capture[0][0]
        return forced_moves

    def get_legal_moves(self):
        '''CheckersBoard.get_legal_moves() -> list
        returns a list of the current player's legal moves'''
        forced_moves = self.forced_moves()
        if len(forced_moves) == 0:
            # TODO calcualte the legal unforced moves
            pass
        else:
            return forced_moves

    def king_piece(self, coord):
        pass

    # TODO make when piece reaches end, it turns into a king, switching the second value in the info on the piece to a 1.

    def remove_outer(self, coords):
        """Takes some coords and removes coords not in the board
        Returns list of coords in board"""
        correct_coords = []
        for coord in coords:
            if coord[0] <= 0 or coord[0] >= 9 or coord[1] <= 0 or coord[1] >= 9:
                continue
            else:
                correct_coords.append(coords)
        return correct_coords


class CheckersFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='grey')
        self.grid()
        self.board = CheckersBoard()
        self.colors = ["white", "black"]
        # set up squares
        self.squares = {}
        count = 0
        for row in range(1, 9):
            count += 1
            for column in range(1, 9):
                rc = (row, column)
                if count % 2 == 0:
                    self.squares[rc] = CheckersSquare(self, row, column, "medium sea green")
                elif (count - 1) % 2 == 0:
                    self.squares[rc] = CheckersSquare(self, row, column, "white")
                count += 1
        # border
        self.columnconfigure(0, minsize=3)
        self.rowconfigure(0, minsize=3)
        self.columnconfigure(9, minsize=3)
        self.rowconfigure(9, minsize=3)

        # turn counter
        turn_display = Canvas(master, height=50, width=50, highlightthickness=0, bg="light blue")
        turn_display.create_oval(8, 8, 42, 42, fill=self.colors[self.board.get_player()])
        turn_display.grid()

        self.updateDisplay()

    def updateDisplay(self):
        # take each spot and add the checkers piece
        for row in range(1, 9):
            for column in range(1, 9):
                rc = (row, column)
                piece = self.board.get_piece(rc)
                self.squares[rc].place_piece(piece)

    def get_click(self, event):
        '''CheckersFrame.get_click(event)
        event handler for mouse click
        gets click data and tries to make the move'''

        # TODO get the position of the click, if on piece, display dots showing legal moves, if on dots move piece to there
        pass

    def pass_move(self):
        '''CheckersFrame.pass_move()
        event handler for Pass button
        passes for the player's turn'''
        pass


def playCheckers():
    root = Tk()
    root.title('Checkers')
    RG = CheckersFrame(root)
    RG.mainloop()


playCheckers()
