# Terminal Scrabble

This is a no-frills text-based scrabble game that can be played on the terminal! One game can be played with anywhere from 2 to 4 players.

## How to start playing

Download scrabble.py, classes.py, and scrabble_dictionary into a directory of your choice. Make sure you have Python 3.5.1 or above installed. (It's possible that earlier versions work as well, but anything below 3.0 will not run properly.) To begin playing, simply use your computer's terminal to navigate to the corresponding folder and type:

```
python scrabble.py
```

If you have multiple versions of python installed, you may need to replace 'python' with 'python3'.

## Scrabble rules

In brief:

* 2-4 players take turns placing letter tiles on the board.
* Each turn, the tiles placed must connect with other tiles on the board to spell English words (in this case, words from the Official Scrabble Player's Dictionary - OSPD).
* Words can only be spelled from left to right, or from top to bottom; backwards and diagonal words are not permitted.
* Players accrue points for the tiles they play; at the end, the player with the most points wins.

For more detailed rules, you can look [here](http://www.ece.northwestern.edu/~robby/uc-courses/22001-2008-winter/scrabble.html) or peruse [here](https://en.wikibooks.org/wiki/Scrabble/Rules). [This](http://www.puzzlers.org/pub/wordlists/ospd.txt) is the OSPD word list I use to verify words played in the game.
