# Scrabble - text version
# by Lydia Ding
# created 10/09/17
# last modified 01/13/18

import random
import copy

class Game:
    def __init__(self):

        # dividers for display purposes
        self.bigDiv = '''\n<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>\n'''
        self.smallDiv = "\n                         -----\n"

        #initialize blank board state, dictionary, bag, and blank players
        self.gameDict = Dictionary("scrabble_dictionary.txt")
        self.gameBag = Bag()
        self.gameBoard = Board(self.gameBag, self.gameDict)
        self.gamePlayers = []
        self.turn = 0
        self.curPlayer = None
        self.isFirstPlay = True

    def play_scrabble(self):
        #Welcome
        print (self.bigDiv)
        print("Welcome to Scrabble!")
        print("Scrabble is a two player game.")

        # personalize player names
        for i in range(2):
            playerName = input("Nickname for player " + str(i + 1) + ": ")
            self.gamePlayers.append(Player(playerName))

        # determine play order and display
        random.shuffle(self.gamePlayers)
        print("Players will play in the following random order:")
        print(", ".join([player.get_name() for player in self.gamePlayers]))

        # draw tiles and display
        for i in range(7):
            for player in self.gamePlayers:
                drawnTile = self.gameBag.draw_tile()
                player.add_tile(drawnTile)

        # while loop that calls newTurn and iterates through play order
        while True:
            print(self.bigDiv)
            self.curPlayer = self.gamePlayers[self.turn % 2]
            # isFirstPlay = let new turn return false if the first play has been made
            self.new_turn()
            self.turn += 1

    # repeats each turn, cycling through each player according to play order
    # displays the tile inventory of the current player,
    # then gives the current player 4 options:
    # 1. place some tiles on the board (make_play)
    # 2. exchange 1-7 of their tiles for new ones from the bag (do_exchange)
    # 3. pass turn
    # 4. end the game (end_game)
    # - 4 automatically happens when players are out of tiles anyways.
    def new_turn(self):

        print(self.curPlayer.get_name() + ", it's your turn.")
        quitGame = input("\nTo quit, enter 'q'. To continue, enter any other key: ")
        if (quitGame == "q"):
            self.end_game()

        print(self.smallDiv)
        self.gameBoard.display_board()
        print("\n")
        self.curPlayer.display_tiles()
        print(self.smallDiv)

        while True:
            turnAction = input("Skip (s), play (p), or exchange tiles (e)? ")
            if (turnAction == "p") or (turnAction == "s"):
                break
            # makes sure there are enough tiles to do an exchange
            elif (turnAction == "e"):
                numTiles = self.gameBag.num_tiles()
                if numTiles >= 7:
                    break
                else:
                    print("Not enough tiles in bag to do an exchange.    To skip, enter \'s\'\n    To play, enter \'p")
            else:
                print("Improper input. Please enter 's' for skip, 'p' for play, and 'e' for exchange.")

        if (turnAction == "p"):
            print("You have chosen to play.")
            self.make_play()
        elif (turnAction == "s"):
            print("You have chosen to skip this turn.")
        else:
            print("You have chosen to exchange your tiles.")
            print(self.smallDiv)
            self.do_exchange()

        # display player stats
        print(self.smallDiv)
        print("SCORES: ")
        for player in self.gamePlayers:
            print("    " + player.get_name() + " - " + str(player.get_score()))

        print(self.smallDiv)
        quitGame = input("To quit, enter 'q'. To continue, enter any other key: ")
        if (quitGame == "q"):
            self.end_game()

    # returns the points that the play has incurred
    def make_play(self):

        print(self.smallDiv)
        self.gameBoard.display_board()
        print("\n")
        self.curPlayer.display_tiles()
        print(self.smallDiv)
        # get coordinates of first letter of word from player and confirm that the
        # slot indicated is not already occupied by a tile.
        print('''Below, please enter the coordinates of the FIRST letter (left- or
        topmost) of the sequence you wish to play.''')
        while True:
            while True:
                x = input("x (a-o): ").lower()
                if (len(x) == 1) and (x.isalpha()) and (ord(x) < 112):
                    x = ord(x) - 97
                    break
                print("Improper input. x coordinate must be a single letter between a-o.")

            while True:
                y = input("y (1-15): ")
                if (y.isdigit()) and (int(y) < 16):
                    y = int(y) - 1
                    break
                print("Improper input. y coordinate must be an integer between 1-15.")

            # double checks that slot is not already occupied by tile.
            if not(self.gameBoard.is_occupied(x, y)):
                break
            else:
                print("The slot you indicated already has a tile on it. Please try again.")

        # get orientation of word (Horizontal v. vertical) from player
        # set isHorizontal depending on player input
        while True:
            orientation = input('''Please enter 'h' for horizontal and 'v' for vertical.
            (Enter either if you are only playing one tile.): ''')
            if (orientation == "h") or (orientation == "v"):
                break
            else:
                print("Improper input.")

        isHorizontal = True if orientation == "h" else False
        isIntersection = False
        addTile = True
        nextCoor = (x, y)

        # set up the temporary board and inventory tracker in case the resulting move
        # needs to be replayed (i.e., we 'play' the move w/ temporary inventory and
        # board that can be reset to the permanent one).
        self.gameBoard.set_temp()
        self.curPlayer.set_temp()

        while addTile:
            # display board before play
            print(self.smallDiv)
            self.gameBoard.display_before(x, y)
            print("\n")
            self.curPlayer.display_tiles()
            print(self.smallDiv)

            while True:
                tile = input("Please enter the letter you wish to play: ").upper()
                if (len(tile) == 1) and self.curPlayer.contains_tile(tile):
                    print("You have elected to play a(n) " + tile + " tile.")
                    break
                elif len(tile) != 1:
                    print("One letter at a time please!")
                elif not(self.curPlayer.contains_tile(tile)):
                    print("The tile " + tile + " is not in your inventory.")

            # place tile onto temp board <-- DONE!
            # 1. intersect is true if current coordinate is adjacent to sth preexisting. check that.
            # 2. calculate the next space, depending on coordinate and H or V (if we're at the edge, tell them that and then stop.) <-- DONE.
            self.gameBoard.place_tile(x, y, tile)
            self.curPlayer.remove_tile(tile)
            if self.gameBoard.is_intersection(x, y, self.isFirstPlay):
                isIntersection = True
            nextCoor = self.gameBoard.next_coordinate(x, y, isHorizontal)

            # display board after play is done
            print(self.smallDiv)
            self.gameBoard.display_after()
            print("\n")
            self.curPlayer.display_tiles()
            print(self.smallDiv)

            if self.curPlayer.num_tiles() == 0:
                print("You have no tiles left to play.")
                addTile = False
            elif not(nextCoor):
                print("There are no more available spots for your next tile.")
                addTile = False
            else:
                while True:
                    choice = input("Would you like to play one more tile? ('y' for yes and 'n' for no.) ")
                    if (choice == "n"):
                        addTile = False
                        print("You have chosen to stop placing tiles this turn.")
                        break
                    elif choice == "y":
                        addTile = True
                        print("You've chosen to add another tile to the board.")
                        x, y = nextCoor[0], nextCoor[1]
                        break
                    else:
                        print("Please enter 'y' to play more tiles and 'n' to stop.")

        legalBoard = self.gameBoard.check_board()
        if not(legalBoard):
            print("The word you played results in a board with illegal words. Please try again.")
            self.curPlayer.undo_remove()
            self.make_play()
        elif not(isIntersection):
            print("The word you played is not adjacent to any preexisting tiles on the board. Please try again.")
            self.curPlayer.undo_remove()
            self.make_play()
        # if the above conditions are met, we set the game board to be permanent.
        else:
            print("Well done! You've made a successful play.")
            score = self.gameBoard.score_play(x, y, isHorizontal)
            self.curPlayer.increment_score(score)
            if not(self.gameBag.has_tiles()) and (self.curPlayer.num_tiles() == 0):
                self.end_game()
            else:
                tilesReplaced = 0
                toReplace = 7 - self.curPlayer.num_tiles()
                while (tilesReplaced < toReplace) and self.gameBag.has_tiles():
                    self.curPlayer.add_tile(self.gameBag.draw_tile())
                    tilesReplaced += 1
            self.gameBoard.confirm_play()
            # we are no longer on the first play
            self.isFirstPlay = False
            print(self.smallDiv)
            self.gameBoard.display_board()
            print("\n")
            self.curPlayer.display_tiles()

    # coordinates an exchange of 1-7 tiles between the player's inventory and the tile bag
    def do_exchange(self):
        while True:
            exchangeNum = int(input("You may exchange 1 to 7 tiles. Please enter the number you wish to exchange: "))
            if (exchangeNum > 0) and (exchangeNum < 8):
                print("You have chosen to exchange " + str(exchangeNum) + " tiles.")
                break
            else:
                print("Improper input. Please enter a digit between 1 and 7.")

        # select and remove the tiles to be exchanged from player
        tilesExchanged = []
        while len(tilesExchanged) < exchangeNum:
            print("Your tile inventory is now as follows:")
            self.curPlayer.display_tiles()
            exchangedTile = input("Please input the tile letter you wish to exchange: ")
            if self.curPlayer.contains_tile(exchangedTile):
                self.curPlayer.remove_tile(exchangedTile)
                self.curPlayer.display_tiles()
                tilesExchanged.append(exchangedTile)
                print(self.smallDiv)
            else:
                print("The tile " + exchangedTile + " is not in your letter inventory.")

        # replace the tiles removed with new tiles from bag
        for i in range(exchangeNum):
            newTile = self.gameBag.draw_tile()
            self.curPlayer.add_tile(newTile)
        print("Exchange complete. Your new tile inventory is as follows:")
        self.curPlayer.display_tiles()

        # place tiles removed from player's inventory into bag
        # this step occurs after everything else to prevent tiles removed from player
        # from being returned to them.
        for tile in tilesExchanged:
            self.gameBag.add_tile(tile)

    def end_game(self):
        # display closing stats
        winner = max(self.gamePlayers, key=lambda p: p.get_score())
        print(self.smallDiv)
        print("Congratulations, " + winner.get_name() + "!")
        print("You won the game with " + str(winner.get_score()) + " points.")
        print("FINAL SCORES: ")
        for player in self.gamePlayers:
            print("    " + player.get_name() + " - " + str(player.get_score()))
        print("Good effort to all. End of game!")
        print(self.bigDiv)
        exit()

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

    def contains_tile(self, tile):
        return (tile.upper() in self.tiles)

    def num_tiles(self):
        return len(self.tiles)

# keeps track of and makes changes to board state as game progresses
class Board:
    def __init__(self, gameBag, gameDict):
        # contain gameBag and gameDict in order to score and check the board
        # in methods score_play() and check_board()
        self.gameBag = gameBag
        self.gameDict = gameDict

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

    # copies board state to a temporary state
    def set_temp(self):
        self.tempState = copy.deepcopy(self.state)

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

    # given x,y coordinates, returns whether the place marked by the coordinates
    # is adjacent to any preexisting tiles (and therefore "intersects" with a
    # previous play).
    def is_intersection(self, x, y, isFirstPlay):
        # this step ensures that, if this is the first play, we check that the
        # tiles pass through the middle (8h) rather than through another word.
        if isFirstPlay:
            if x == 7 and y == 7:
                return True
        else:
            # check left, right, top, bottom -- respectively. return True if any are occupied.
            if ((x != 0 and self.state[y][x-1].isalpha()) or
            (x != 14 and self.state[y][x+1].isalpha()) or
            (y != 0 and self.state[y-1][x].isalpha()) or
            (y != 14 and self.state[y+1][x].isalpha())):
                return True
        # return False if we've gone through all four and found no occupied spaces.
        return False

    # given x,y coordinates, returns whether the space is occupied w/ a tile.
    def is_occupied(self, x, y):
        return self.state[y][x].isalpha()

    # scores the current play and returns the number of points earned that play.
    def score_play(self, x, y, isHorizontal):
        print("START: "+self.tempState[y][x])
        factor = 1
        # this is the score for the letter sequence that counts 'bonuses'
        multScore = 0
        # this is the score for the letter sequence that doesn't count bonuses
        baseScore = 0
        if isHorizontal:
            # go forward until we hit a terminator ('.' or the edge)
            curX = x
            while curX <= 14 and self.tempState[y][curX] != '.':
                baseScore += self.score_helper(curX, y, isHorizontal)
                newValue = self.tempState[y][curX]
                oldValue = self.state[y][curX]

                if not(oldValue.isalpha()):
                    placeFactor = self.pointMatrix[y][curX]
                    # if it's new and a word bonus, add it and * factor
                    if placeFactor % 10 == 0:
                        factor *= placeFactor//10
                        multScore += self.gameBag.get_value(self.tempState[y][curX])
                    # if it's new and not a word bonus, add it with place
                    else:
                        multScore += self.gameBag.get_value(self.tempState[y][curX]) * placeFactor
                # if it's old, add it without place
                else:
                     multScore += self.gameBag.get_value(oldValue)
                curX += 1
            # go backward; these will all be old tiles
            curX = x - 1
            while curX >= 0 and self.state[y][curX] != '.':
                multScore += self.gameBag.get_value(self.state[y][curX])
                curX -= 1
        else:
            # go down until we hit a terminator ('.' or the edge)
            curY = y
            while curY <= 14 and self.tempState[curY][x] != '.':
                baseScore += self.score_helper(x, curY, isHorizontal)
                newValue = self.tempState[curY][x]
                oldValue = self.state[curY][x]
                if not(oldValue.isalpha()):
                    # print("NEW: "+ newValue)
                    placeFactor = self.pointMatrix[curY][x]
                    # if it's new and a word bonus, add it and * factor
                    if placeFactor % 10 == 0:
                        factor *= placeFactor//10
                        multScore += self.gameBag.get_value(self.tempState[curY][x])
                    # if it's new and not a word bonus, add it with place
                    else:
                        multScore += self.gameBag.get_value(self.tempState[curY][x]) * placeFactor
                # if it's old, add it without place
                else:
                     multScore += self.gameBag.get_value(oldValue)
                curY += 1
            # go up; these will all be old tiles
            curY = y - 1
            while curY >= 0 and self.state[curY][x] != '.':
                multScore += self.gameBag.get_value(self.state[curY][x])
                curY -= 1
        print("MULT: " + str(multScore) + "\nBASE: " + str(baseScore) + "\nFACTOR: " + str(factor))
        return (multScore * factor) + baseScore

    def score_helper(self, x, y, isHorizontal):
        score = 0
        if isHorizontal:
            curY = y + 1
            # goes downwards
            while curY <= 14 and self.state[curY][x] != '.':
                score += self.gameBag.get_value(self.state[curY][x])
                curY += 1
            # goes upwards
            curY = y - 1
            while curY >= 0 and self.state[curY][x] != '.':
                score += self.gameBag.get_value(self.state[curY][x])
                curY -= 1
        else:
            curX = x + 1
            # goes to the right
            while curX <= 14 and self.state[y][curX] != '.':
                score += self.gameBag.get_value(self.state[y][curX])
                curX += 1
            # goes to the left
            curX = x - 1
            while curX >= 0 and self.state[y][curX] != '.':
                score += self.gameBag.get_value(self.state[y][curX])
                curX -= 1

        return score

    # iterates over the board and checks that each continuous sequence of letters
    # -- horizontal and vertical -- is a word in the Dictionary.
    # Called at the end of each play to ensure the new word and modifications to
    # existing ones are legal.
    def check_board(self):

        # horizontal check
        curWord = ""
        for row in self.tempState:
            for char in row:
                if char.isalpha():
                    curWord += char
                elif not(char.isalpha()) and curWord != "":
                    if len(curWord) > 1 and not(self.gameDict.look_up(curWord)):
                        return False
                    # reset
                    curWord = ""
            # check word we're on
            if curWord != "":
                if not(self.gameDict.look_up(curWord)):
                    return False
                # reset
                curWord = ""

        # vertical check
        curWord = ""
        for column in range(15):
            for row in range(15):
                char = self.tempState[row][column]
                if char.isalpha():
                    curWord += char
                elif not(char.isalpha()) and curWord != "":
                    if len(curWord) > 1 and not(self.gameDict.look_up(curWord)):
                        return False
                    # reset
                    curWord = ""
            # check word we're on
            if curWord != "":
                if not(self.gameDict.look_up(curWord)):
                    return False
                # reset
                curWord = ""

        # by default, returns true if we have gone through the entire board
        # without finding illegal words.
        return True

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

# contains all words in the Official Scrabble Players Dictionary (OSPD).
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

if __name__ == "__main__":
    game = Game()
    game.play_scrabble()
