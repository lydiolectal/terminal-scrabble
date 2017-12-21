# Scrabble - text version
# by Lydia Ding
# 10/09/17

import random
import copy

# stores score and tile inventory for every player in the game
class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.tiles = []
        self.toRemove = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_score(self):
        return self.score

    def increment_score(self, increment):
        self.score = int(self.score + increment)

    def get_tiles(self):
        return self.tiles

    def display_tiles(self):
        print("| " + " ".join(self.tiles) + " |")

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.tiles.sort()

    def set_temp(self):
        self.toRemove = []

    def remove_tile(self, tile):
        tile = tile.upper()
        self.tiles.remove(tile)
        self.toRemove.append(tile)

    def undo_remove(self):
        for tile in self.toRemove:
            self.tiles.append(tile)
        self.toRemove = []

    # checks that self.tiles contains all the letters within word
    # (i.e., that the letters in word are a subset of the tile inventory)
    # false if no, true if yes
    # def contains_word(self, word):
    #     word = word.upper()
    #     return set(list(word)) <= set(self.tiles)

    def contains_tile(self, tile):
        return (tile.upper() in self.tiles)

    def num_tiles(self):
        return len(self.tiles)

# keeps track of and makes changes to board state as game progresses
class Board:
    def __init__(self):
        self.turn = 0
        # state tracks tiles placed on the board
        # - used to display the current state of the board to players
        self.state = [['.']*15 for _ in range(15)]
        self.state[7][7] = '*'

        self.tempState = [['.']*15 for _ in range(15)]
        self.tempState[7][7] = '*'

        # pointMatrix tracks which spots double or triple points
        # - used to calculate point allocation
        # - slots with 2 or 3 double/triple the points incurred by a letter.
        # - slots with 20 or 30 double/triple the points incurred by the word
        # to which the tile belongs.
        self.pointMatrix = [[30, 1, 1, 2, 1, 1, 1, 30, 1, 1, 1, 2, 1, 1, 30],
        [1, 20, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 20, 1],
        [1, 1, 20, 1, 1, 1, 2, 1, 2, 1, 1, 1, 20, 1, 1],
        [2, 1, 1, 20, 1, 1, 1, 2, 1, 1, 1, 20, 1, 1, 2],
        [1, 1, 1, 1, 20, 1, 1, 1, 1, 1, 20, 1, 1, 1, 1],
        [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1],
        [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
        [30, 1, 1, 2, 1, 1, 1, 20, 1, 1, 1, 2, 1, 1, 30],
        [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
        [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1],
        [1, 1, 1, 1, 20, 1, 1, 1, 1, 1, 20, 1, 1, 1, 1],
        [2, 1, 1, 20, 1, 1, 1, 2, 1, 1, 1, 20, 1, 1, 2],
        [1, 1, 20, 1, 1, 1, 2, 1, 2, 1, 1, 1, 20, 1, 1],
        [1, 20, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 20, 1],
        [30, 1, 1, 2, 1, 1, 1, 30, 1, 1, 1, 2, 1, 1, 30]]

        # FIX THIS THIS IS HORRIBLE DESIGN
        self.tileValues = {
        "E":1, "A":1, "I":1, "O":1, "N":1, "R":1, "T":1, "L":1, "S":1, "U":1,
        "D":2, "G":2, "B":3, "C":3, "M":3, "P":3, "F":4, "H":4, "V":4, "W":4,
        "Y":4, "K":5, "J":8, "X":8, "Q":10, "Z":10}

    # copies board state to a temporary state
    def set_temp(self):
        self.tempState = copy.deepcopy(self.state)

    def get_temp(self):
        return self.tempState

    # sets the board state to the temporary state
    def confirm_play(self):
        self.state = copy.deepcopy(self.tempState)

    # display current state of board
    def display_board(self):
        print("      a  b  c  d  e  f  g  h  i  j  k  l  m  n  o ")
        for i in range(15):
            if (i < 9):
                print("   " + str(i+1) + "  " + "  ".join(self.state[i]))
            else:
                print("   " + str(i+1) + " " + "  ".join(self.state[i]))

    # display current state of temp board
    def display_after(self):
        print("      a  b  c  d  e  f  g  h  i  j  k  l  m  n  o ")
        for i in range(15):
            if (i < 9):
                print("   " + str(i+1) + "  " + "  ".join(self.tempState[i]))
            else:
                print("   " + str(i+1) + " " + "  ".join(self.tempState[i]))

    # display current state of temp board and marks the spot that will be played this turn with a '+'
    def display_before(self, x, y):
        tempTemp = self.tempState.copy()
        tempTemp[y][x] = "+"
        print("      a  b  c  d  e  f  g  h  i  j  k  l  m  n  o ")
        for i in range(15):
            if (i < 9):
                print("   " + str(i+1) + "  " + "  ".join(self.tempState[i]))
            else:
                print("   " + str(i+1) + " " + "  ".join(self.tempState[i]))

    # - Places tile into board matrix according to coordinates given
    # - assumes coordinate and word are correct in format + range
    def place_tile(self, x, y, tile):
        self.tempState[y][x] = tile

        # # if it's the first turn, check that word passes through middle *.
        # if turn == 0:
        #     if isHorizontal:
        #         for i in range(wordLength):
        #             if self.tempState[y][x + i] == "*":
        #                 properIntersection = True
        #             self.tempState[y][x + i] = word[i]
        #     else:
        #         for j in range(wordLength):
        #             if self.tempState[y + j][x] == "*":
        #                 properIntersection = True
        #             self.tempState[y + j][x] = word[j]
        #
        # # otherwise, check that the word they played intersects w/ other tiles.
        # else:
        #     if isHorizontal:
        #         for i in range(wordLength):
        #             self.tempState[y][x + i] = word[i]
        #
        #     else:
        #         for j in range(wordLength):
        #             self.tempState[y + j][x] = word[j]
        #
        # return properIntersection

    # given x,y coordinates, returns whether the place marked by the coordinates
    # is adjacent to any preexisting tiles (and therefore "intersects" with a
    # previous play).
    def is_intersection(self, x, y, isFirstPlay):
        # this step ensures that, if this is the first play, we check that the
        # tiles pass through the middle (8h) rather than through another word.
        if isFirstPlay:
            print("FIRST PLAY ?!?")
            if x == 7 and y == 7:
                return True
        else:
            print("WE ARE NOT ON THE FIRST PLAY ANYMORE.")
            print("X: " + str(x) + " Y: " + str(y))
            # check left, right, top, bottom -- respectively. return True if any are occupied.
            if ((x != 0 and self.state[y][x-1].isalpha()) or
            (x != 14 and self.state[y][x+1].isalpha()) or
            (y != 0 and self.state[y-1][x].isalpha()) or
            (y != 14 and self.state[y+1][x].isalpha())):
                print("hooray...?")
                return True
        # return False if we've gone through all four and found no occupied spaces.
        return False

    # given x,y coordinates, returns whether the space is occupied w/ a tile.
    def is_occupied(self, x, y):
        return self.state[y][x].isalpha()

    # TODO: test and call this in main game.
    # scores the current play and returns the number of points earned that play.
    def score_play(self):
        totalScore = 0
        factor = 1
        for row in range(15):
            wordScore = 0
            isNewWord = False
            for col in range(15):
                oldValue = self.state[row][col]
                newValue = self.tempState[row][col]
                # if the tile is already on the old board, calculate only the
                # letter score, without bonus points.
                if oldValue.isalpha():
                    wordScore += self.tileValues[oldValue]
                elif newValue.isalpha():
                    placeFactor = self.pointMatrix[row][col]
                    isNewWord = True
                    if (placeFactor % 10) == 0:
                        factor = factor * (placeFactor/10)
                        # find some way to access letter score
                        wordScore += self.tileValues[newValue]
                    else:
                        # find some way to access letter score
                        wordScore += placeFactor * self.tileValues[newValue]
                # if it's not a letter in either
                elif (not(oldValue.isalpha() or newValue.isalpha())) and wordScore != 0:
                    if isNewWord:
                        totalScore += wordScore
                    wordScore = 0
                    isNewWord = False
        return int(totalScore * factor)

    # given x,y coordinates, returns a tuple containing the coordinates of the
    # next empty spot (skips over any already occupied spaces). Returns false
    # if we are at an edge.
    def next_coordinate(self, x, y, isHorizontal):
        if isHorizontal:
            if x == 14:
                return False
            elif not(self.state[y][x + 1].isalpha()):
                return (x + 1, y)
            else:
                return self.next_coordinate(x + 1, y, isHorizontal)

        else:
            if y == 14:
                return False
            elif not(self.state[y + 1][x].isalpha()):
                return (x, y + 1)
            else:
                return self.next_coordinate(x, y + 1, isHorizontal)

    # given the length of a word, its orientation, and coordinates,
    # - returns the segment of the points matrix that applies to the area
    # covered by the word. Used to calculate the points incurred during
    # a given play
    # def get_points(self, x, y, isHorizontal, word):
    #     wordLength = len(word)
    #
    #     miniMatrix = []
    #     if isHorizontal:
    #         for i in range(wordLength):
    #             miniMatrix.append(self.pointMatrix[y][x + i])
    #
    #     else:
    #         for j in range(wordLength):
    #             miniMatrix.append(self.pointMatrix[y + j][x])
    #     return miniMatrix

# keeps track of tile bag, and allows players to draw and exchange tiles
class Bag:
    def __init__(self):
        self.tiles = {
        "E":12, "A":9, "I":9, "O":8, "N":6, "R":6, "T":6, "L":4, "S":4, "U":4,
        "D":4, "G":3, "B":2, "C":2, "M":2, "P":2, "F":2, "H":2, "V":2, "W":2,
        "Y":2, "K":1, "J":1, "X":1, "Q":1, "Z":1}

        self.tileValues = {
        "E":1, "A":1, "I":1, "O":1, "N":1, "R":1, "T":1, "L":1, "S":1, "U":1,
        "D":2, "G":2, "B":3, "C":3, "M":3, "P":3, "F":4, "H":4, "V":4, "W":4,
        "Y":4, "K":5, "J":8, "X":8, "Q":10, "Z":10}

    # return a letter from the Bag inventory, and delete
    # returns False if Bag is empty
    def draw_tile(self):
        if not(self.has_tiles()):
            return False
        else:
            drawnTile = random.choice(list(self.tiles))
            if self.tiles[drawnTile] == 1:
                del self.tiles[drawnTile]
            else:
                self.tiles[drawnTile] -= 1
            return drawnTile

    def add_tile(self, tile):
        tile = tile.upper()
        if tile in self.tiles:
            self.tiles[tile] += 1
        else:
            self.tiles[tile] = 1

    def exchange_tile(self, tile):
        newTile = self.draw_tile()
        self.add_tile(tile)
        return newTile

    # returns the score value of a given letter tile
    # - to be multiplied with point matrix to calculate points
    def get_value(self, tile):
        return self.tileValues[tile]

    # returns True if Bag still has tiles; False if empty.
    def has_tiles(self):
        return bool(self.tiles)

    def num_tiles(self):
        numTiles = 0
        for letter in self.tiles:
            numTiles += self.tiles[letter]
        return numTiles

# contains all words in the Official Scrabble Players Dictionary (OSPD),
# as well as inflectional versions of words contained therein.
class Dictionary:
    def __init__(self, dictFile):
        self.wordSet = set()
        f = open(dictFile, "r")
        for line in f:
            self.wordSet.add(line.strip('\n').upper())

    def look_up(self, word):
        return(word in self.wordSet)

    def add_entry(self, word):
        wordSet.add(word.upper())
