# Scrabble - text version
# by Lydia Ding
# 10/09/17

# Fun possible additions:
# Make it possible for user to add in new terms to the Dictionary
# The blank tile freebie in regular Scrabble
# 'AI' player, possibly with varying levels of skill
# An undo option (i.e., replaying a word during someone's turn)

# Possible changes:
# Put board, bag, and maybe dictionary classes into one single 'state' class?
# Reduce number of players to official scrabble default of 2 players only
# Make the board checking and score functions less bulky.

from classes import Board
from classes import Dictionary
from classes import Bag
from classes import Player
from random import shuffle

# dividers for display purposes
bigDiv = '''\n<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>\n'''
smallDiv = "\n                         -----\n"

def play_scrabble():
    #initialize blank board state, dictionary, bag, and blank players
    gameBoard = Board()
    gameDict = Dictionary("scrabble_dictionary.txt")
    gameBag = Bag()
    p1 = Player("")
    p2 = Player("")
    p3 = Player("")
    p4 = Player("")
    gamePlayers = [p1, p2, p3, p4]
    turn = 0
    isFirstPlay = True

    #Welcome
    print (bigDiv)
    print("Welcome to Scrabble!")
    #some more instructions and how to exit game, etc.
    print("Scrabble can be played by 2-4 players.")

    while True:
        numPlayers = input("How many players do you wish to play with? ")
        if (numPlayers=="2") or (numPlayers=="3") or (numPlayers=="4"):
            numPlayers = int(numPlayers)
            break

    # personalize player names
    for i in range(numPlayers):
        playerName = input("Nickname for player " + str(i + 1) + ": ")
        gamePlayers[i].set_name(playerName)

    # determine play order and display
    gamePlayers = set_order(gamePlayers, numPlayers)
    print("Players will play in the following random order:")
    print(", ".join([player.get_name() for player in gamePlayers]))

    # draw tiles and display
    for i in range(7):
        for player in gamePlayers:
            drawnTile = gameBag.draw_tile()
            player.add_tile(drawnTile)

    # while loop that calls newTurn and iterates through play order
    while True:
        print(bigDiv)
        curPlayer = gamePlayers[turn % numPlayers]
        # isFirstPlay = let new turn return false if the first play has been made
        isFirstPlay = new_turn(gameBoard, gameDict, gameBag, gamePlayers, turn, curPlayer, isFirstPlay)
        turn += 1

# sets order of play by randomly shuffling list of players
# returns a list with Player objects ordered in the order of play
def set_order(gamePlayers, numPlayers):
    gamePlayers = gamePlayers[0:numPlayers]
    shuffle(gamePlayers)
    return gamePlayers

# repeats each turn, cycling through each player according to play order
# displays the tile inventory of the current player,
# then gives the current player 4 options:
# 1. place some tiles on the board (make_play)
# 2. exchange 1-7 of their tiles for new ones from the bag (do_exchange)
# 3. pass turn
# 4. end the game (end_game)
# - 4 automatically happens when players are out of tiles anyways.

def new_turn(gameBoard, gameDict, gameBag, gamePlayers, turn, curPlayer, isFirstPlay):

    print(curPlayer.get_name() + ", it's your turn.")
    quitGame = input("\nTo quit, enter 'q'. To continue, enter any other key: ")
    if (quitGame == "q"):
        end_game(gamePlayers)

    print(smallDiv)
    gameBoard.display_board()
    print("\n")
    curPlayer.display_tiles()
    print(smallDiv)

    while True:
        turnAction = input("Skip (s), play (p), or exchange tiles (e)? ")
        if (turnAction == "p") or (turnAction == "s"):
            break
        # makes sure there are enough tiles to do an exchange
        elif (turnAction == "e"):
            numTiles = gameBag.num_tiles()
            if numTiles >= 7:
                break
            else:
                print("Not enough tiles in bag to do an exchange.    To skip, enter \'s\'\n    To play, enter \'p")
        else:
            print("Improper input. Please enter 's' for skip, 'p' for play, and 'e' for exchange.")

    if (turnAction == "p"):
        print("You have chosen to play.")
        print(smallDiv)
        gameBoard.display_board()
        print("\n")
        curPlayer.display_tiles()
        print(smallDiv)
        make_play(turn, curPlayer, gameBoard, gameDict, gameBag, isFirstPlay)
        # we are no longer on the first play
        isFirstPlay = False
        print(smallDiv)
        gameBoard.display_board()
        print("\n")
        curPlayer.display_tiles()
        # print("Your score is now " + str(curPlayer.get_score()))
    elif (turnAction == "s"):
        print("You have chosen to skip this turn.")
    else:
        print("You have chosen to exchange your tiles.")
        print(smallDiv)
        do_exchange(curPlayer, gameBag)

    # display player stats
    print(smallDiv)
    print("SCORES: ")
    for player in gamePlayers:
        print("    " + player.get_name() + " - " + str(player.get_score()))

    print(smallDiv)
    quitGame = input("To quit, enter 'q'. To continue, enter any other key: ")
    if (quitGame == "q"):
        end_game(gamePlayers)
    return isFirstPlay

# returns the points that the play has incurred
def make_play(turn, curPlayer, gameBoard, gameDict, gameBag, isFirstPlay):

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
        if not(gameBoard.is_occupied(x, y)):
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
    gameBoard.set_temp()
    curPlayer.set_temp()

    while addTile:
        # display board before play
        print(smallDiv)
        gameBoard.display_before(x, y)
        print("\n")
        curPlayer.display_tiles()
        print(smallDiv)

        while True:
            tile = input("Please enter the letter you wish to play: ").upper()
            if (len(tile) == 1) and curPlayer.contains_tile(tile):
                print("You have elected to play a(n) " + tile + " tile.")
                break
            elif len(tile) != 1:
                print("One letter at a time please!")
            elif not(curPlayer.contains_tile(tile)):
                print("The tile " + tile + " is not in your inventory.")

        # place tile onto temp board <-- DONE!
        # 1. intersect is true if current coordinate is adjacent to sth preexisting. check that.
        # 2. calculate the next space, depending on coordinate and H or V (if we're at the edge, tell them that and then stop.) <-- DONE.
        gameBoard.place_tile(x, y, tile)
        curPlayer.remove_tile(tile)
        if gameBoard.is_intersection(x, y, isFirstPlay):
            isIntersection = True
        nextCoor = gameBoard.next_coordinate(x, y, isHorizontal)

        # display board after play is done
        print(smallDiv)
        gameBoard.display_after()
        print("\n")
        curPlayer.display_tiles()
        print(smallDiv)

        if curPlayer.num_tiles() == 0:
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

    # DO IT AGAIN IF WORDS ON BOARD ARE ILLEGAL or INTERSECT IS FALSE.
    # MAYBE ASK PLAYER TO CONFIRM PLAY AS WELL? rn we just automatically confirm it if it's legal.
    legalBoard = check_board(gameBoard, gameDict)
    if not(legalBoard):
        print("The word you played results in a board with illegal words. Please try again.")
        curPlayer.undo_remove()
        make_play(turn, curPlayer, gameBoard, gameDict, gameBag, isFirstPlay)
    elif not(isIntersection):
        print("The word you played is not adjacent to any preexisting tiles on the board. Please try again.")
        curPlayer.undo_remove()
        make_play(turn, curPlayer, gameBoard, gameDict, gameBag, isFirstPlay)
    # if the above conditions are met, we set the game board to be permanent.
    else:
        print("Well done! You've made a successful play.")
        score = gameBoard.score_play()
        curPlayer.increment_score(score)
        if not(gameBag.has_tiles()) and (curPlayer.num_tiles() == 0):
            end_game(gamePlayers)
        else:
            tilesReplaced = 0
            toReplace = 7 - curPlayer.num_tiles()
            while (tilesReplaced < toReplace) and gameBag.has_tiles():
                curPlayer.add_tile(gameBag.draw_tile())
                tilesReplaced += 1
        gameBoard.confirm_play()

# iterates over the board and checks that each continuous sequence of letters
# -- horizontal and vertical -- is a word in the Dictionary.
# Called at the end of each play to ensure the new word and modifications to
# existing ones are legal.
def check_board(gameBoard, gameDict):
    boardState = gameBoard.get_temp()

    # horizontal check
    curWord = ""
    for row in boardState:
        for char in row:
            if char.isalpha():
                curWord += char
            elif not(char.isalpha()) and curWord != "":
                if len(curWord) > 1 and not(gameDict.look_up(curWord)):
                    return False
                # reset
                curWord = ""
        # check word we're on
        if curWord != "":
            if not(gameDict.look_up(curWord)):
                return False
            # reset
            curWord = ""

    # vertical check
    curWord = ""
    for column in range(15):
        for row in range(15):
            char = boardState[row][column]
            if char.isalpha():
                curWord += char
            elif not(char.isalpha()) and curWord != "":
                if len(curWord) > 1 and not(gameDict.look_up(curWord)):
                    return False
                # reset
                curWord = ""
        # check word we're on
        if curWord != "":
            if not(gameDict.look_up(curWord)):
                return False
            # reset
            curWord = ""

    # by default, returns true if we have gone through the entire board
    # without finding illegal words.
    return True

# coordinates an exchange of 1-7 tiles between the player's inventory and the tile bag
def do_exchange(curPlayer, gameBag):
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
        curPlayer.display_tiles()
        exchangedTile = input("Please input the tile letter you wish to exchange: ")
        if curPlayer.contains_tile(exchangedTile):
            curPlayer.remove_tile(exchangedTile)
            curPlayer.display_tiles()
            tilesExchanged.append(exchangedTile)
            print(smallDiv)
        else:
            print("The tile " + exchangedTile + " is not in your letter inventory.")

    # replace the tiles removed with new tiles from bag
    for i in range(exchangeNum):
        newTile = gameBag.draw_tile()
        curPlayer.add_tile(newTile)
    print("Exchange complete. Your new tile inventory is as follows:")
    curPlayer.display_tiles()

    # place tiles removed from player's inventory into bag
    # this step occurs after everything else to prevent tiles removed from player
    # from being returned to them.
    for tile in tilesExchanged:
        gameBag.add_tile(tile)

def end_game(gamePlayers):
    # display closing stats
    winner = max(gamePlayers, key=lambda p: p.get_score())
    print(smallDiv)
    print("Congratulations, " + winner.get_name() + "!")
    print("You won the game with " + str(winner.get_score()) + " points.")
    print("FINAL SCORES: ")
    for player in gamePlayers:
        print("    " + player.get_name() + " - " + str(player.get_score()))
    print("Good effort to all. End of game!")
    print(bigDiv)
    exit()

if __name__ == "__main__":
    play_scrabble()
