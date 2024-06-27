from tkinter import *
from tkinter import messagebox
import random


class MineTile(Label):
    """represents a minesweeper tile"""

    def __init__(self, master, coord, is_mine):
        """MineTile(master, coord, isMine)
        A minetile in minesweeper"""
        # initial values
        Label.__init__(self, master, height=1, width=2, text='', bg='white', font=('Arial', 12), relief=RAISED)
        self.coord = coord
        self.isMine = is_mine
        self.isFlagged = False
        self.isSeen = False
        self.disabled = False

        # different colors to be used for mine numbers
        self.colormap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']

        # set up listeners
        self.bind('<Button-1>', self.reveal)
        self.bind('<Button-3>', self.flag)

    def flag(self, event):
        """MineTile.flag(event)
        Flags or unflags a mine tile"""
        if (not self.isSeen) and (not self.disabled):  # checks if tile can be flagged
            if self.master.flag(not self.isFlagged):  # checks the flag count to see if flags can be placed
                self.isFlagged = not self.isFlagged  # turns flag to new state
                # flag or unflag tile
                if self.isFlagged:
                    self['text'] = '*'
                else:
                    self['text'] = ''

    def reveal(self, event):
        """MineTile.reveal(event)
        Reveals a tile when event happens"""
        if (not self.isFlagged) and (not self.disabled):  # only reveals if tile isn't flagged and isn't disabled
            if self.reveal_tile():  # reveals surrounding if tile has no surrounding mines
                self.master.reveal_surrounding(self.coord)

    def reveal_tile(self):
        """MineTile.reveal_tile()
        reveals the tile"""
        if self.isMine:  # player loses
            self.master.player_loss()
        else:  # display surrounding mines number
            mine_surround = self.master.mine_surrounding(self.coord)
            self['bg'] = 'dim gray'
            self['relief'] = SUNKEN
            self.isSeen = True
            self.disable_tile()
            # displays number if mine_surround is not 0
            if mine_surround != 0:
                self['fg'] = self.colormap[mine_surround]
                self['text'] = str(mine_surround)
                self.master.check_for_win()
                return False  # tile has mines surrounding it
            else:
                self.master.check_for_win()
                return True  # tile doesn't have mines surrounding it

    def mine(self):
        """MineTile.mine()
        returns whether tile is a mine or not"""
        return self.isMine

    def seen(self):
        """MineTile.seen()
        Returns whether tile is revealed or not"""
        return self.isSeen

    def flagged(self):
        """MineTile.flagged()
        Returns if tile is flagged or not"""
        return self.isFlagged

    def turn_mine(self):
        """MineTile.turn_mine()
        Makes a tile a mine"""
        self.isMine = True

    def disable_tile(self):
        """MineTile.disable_tile()
        Make a tile disabled from use"""
        self.disabled = True


class FlagCountLabel(Label):

    def __init__(self, master, total_mine):
        """FLagCountLabel(master, totalMine)
        Makes a label that displays amount of mines."""
        self.totalFlag = total_mine
        Label.__init__(self, master, bg='black', height=1, width=2, text=self.totalFlag, font=('Arial', 12), fg='white')

    def lower_count(self):
        """FlagCounterLabel.lowerCount()
        Lowers count of flags in display.
        """
        if self.can_flag():
            self.totalFlag -= 1
            self['text'] = self.totalFlag

            return True  # returns True to show flag can be placed

    def increase_count(self):
        """FlagCounterLabel.increaseCount()
        Increases amount of flags shown in display"""
        self.totalFlag += 1
        self['text'] = self.totalFlag

    def can_flag(self):
        """FlagCountLabel.canFlag()
        Checks if player can place a flag"""
        if self.totalFlag > 0:
            return True
        else:
            return False


class MineSweeperFrame(Frame):

    def __init__(self, master, width, height, amount):
        """MineSweeperFrame(master, width, height, amount)
        Starts a MineSweeper game"""
        # initial values
        self.width = width
        self.height = height
        self.amount = amount
        Frame.__init__(self, master, bg='black')
        self.grid()
        # create tiles
        self.tiles = {}
        for x in range(self.width):  # TODO board will always have empty space if width less than 5
            for y in range(self.height):
                coord = (x, y)
                self.tiles[coord] = MineTile(self, coord, False)
                self.tiles[coord].grid(row=y, column=x)
        # set mines
        coord_list = list(self.tiles)
        coord_list.remove((0, 0))
        rand_coords = random.sample(coord_list, self.amount)
        for coord in rand_coords:
            self.tiles[coord].turn_mine()

        # create flag count
        self.flagCount = FlagCountLabel(master, self.amount)
        self.flagCount.grid()

    def flag(self, lower_flag):
        """MineSweeperFrame.flag(lowerFlag)
        lowers flag or raises flag count for label
        returns whether flag can be placed based on label flag count
        """
        if lower_flag:
            return self.flagCount.lower_count()
        else:
            self.flagCount.increase_count()
            return True

    def mine_surrounding(self, tile_coord):
        """MineSweeperFrame.mine_surrounding(tileCoord)
        returns the amount of mines surrounding a tile"""
        surrounding = self.surrounding_coordinates(tile_coord)
        surrounding_mine = 0
        for tile in surrounding:
            if self.tiles[tile].mine():
                surrounding_mine += 1
        return surrounding_mine

    def reveal_surrounding(self, tile_coord):
        """reveals surrounding tiles"""
        surrounding = self.surrounding_coordinates(tile_coord)
        for tile in surrounding:
            if (not self.tiles[tile].seen()) and (not self.tiles[tile].flagged()):  # only reveals if conditions met
                self.tiles[tile].reveal_tile()

                if self.mine_surrounding(tile) == 0:  # reveals surrounding if tile is has no mines surrounding
                    self.reveal_surrounding(tile)

    def surrounding_coordinates(self, tile_coord):
        """MineSweeperFrame.surrounding_coordinates(tileCoord)
        returns list of coordinates surrounding a coordinate"""
        x = tile_coord[0]
        y = tile_coord[1]
        surrounding = [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1),
                       (x + 1, y - 1)]
        return [tile for tile in surrounding if
                (tile[0] < self.width) and (tile[0] >= 0) and (tile[1] < self.height) and (tile[1] >= 0)]

    def player_loss(self):
        """MineSweeperFrame.playerLoss()
        Does all actions for when player loses"""
        messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
        for coord in list(self.tiles):
            if self.tiles[coord].mine():  # display all mines
                self.tiles[coord]['text'] = "*"
                self.tiles[coord]['bg'] = 'red'
            self.tiles[coord].disable_tile()  # disable all tiles

    def check_for_win(self):
        """MineSweeperFrame.check_for_win()
        Checks if player has won"""
        amount_revealed = 0
        winning_amount = (self.width * self.height) - self.amount
        for coord in list(self.tiles):
            if self.tiles[coord].seen():  # adds to amountReveal if tile is revealed
                amount_revealed += 1
            if amount_revealed == winning_amount:  # you win
                for tile in list(self.tiles):
                    self.tiles[tile].disable_tile()
                messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)


def play_minesweeper(width, height, amount):
    """play_minesweeper(width, height, amount)
    plays minesweeper with a board the entered width and height
    has 'amount' of mines"""

    if ((width * height) <= amount) or (amount == 0):
        print("Invalid amounts")
        return
    root = Tk()
    root.title('Mine Sweeper')
    MineSweeperFrame(root, width, height, amount)
    root.mainloop()


play_minesweeper(12, 8, 15)
