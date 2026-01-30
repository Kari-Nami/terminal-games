This repository is to document my terminal game development journey and allow me to look back at my progress with using curses for creating games. These are all for educational purposes, so any code is free to use, copy, fork, etc. However, since this is my educational space, I will not be accepting any pull requests since I want all of this to be my learning journey.

**All code is written by me, so please don't feed it to AI :D**. Eventhough these are basic and common games, I still donot want my code to help feed these world-destroying machines.

# How To Use
Since all of these are written in python `curses`, which is not supported on windows, windows requires 1 extra step. Unix systems have curses pre-installed with python, so there is no need to manually install the library.

- **Unix Systems (MacOs, Linux, etc.):** curses should be pre-installed. If for some reason you don't have it, run `pip install curses` in your terminal and you're good to go.

- **Windows:** people created a version of curses that works on windows called `windows curses`. It is exactly the same as normal curses, so the only thing you need to do is run `pip install windows-curses` in your terminal.

Put all the files from 1 game into the same folder. After that either run the game in your terminal using `python file_name.py` or just run it in your IDE (works for pycharm, not sure for other IDEs).

# Game 1: Apple Eating Game
This is a basic game where the player moves a character around using either WASD or arrow keys to eat apples. Each eaten apple gives 1 point, and eating a normal apple has a chance to spawn a super apple, which gives 10 points. The goal of the game is to get as many points as possible within 30 seconds. The player can store their score in the scoreboard and a leaderboard of the top 10 players/scores is displayed in the game window.

## Iterations
The game has 2 versions: original attempt and a remake.

### Version 1
The board was printed on the main window using ASCII characters (| for vertical walls, - for horizontal walls, + for corners). The entire screen is cleared using `window.clear()` every frame. No countdown popup.

**Main issue:** constant clears made the game flicker every frame (~60 times a second).

Other issues include:
- I didn't like the look of the ASCII board outline (liked the look of popup-window outlines more)

- No countdown before the game starts dropped the player straight into the game, wasting about 2-3 seconds on examining the board & putting fingers on the movement keys.

- When time runs out and "time's out" popup appears, it keeps reading the inputs and stores them in the input buffer. This buffer is then printed on the next "name" page, making the page load with pre-typed characters.

### Version 2 (Main Version)
The board is a popup-window to have the pretty outlines and simplify character & apple location generation. Coordinates in popup-windows reset, with the top-left corner of the popup window being (0, 0) for anything inside it. This allows for the bounds of movement & generation to be within `1` (0 is outline) to `board-size`, instead of `board-starting-location + 1` (+1 to account for outline) to `board-starting-location + 1 + board-size`.

**Main fix:** Removed `window.clear()` every loop. Instead, simply re-draw the "old" locations of the character with empty spaces and apple locations when they are eaten. This greatly removes the number of characters/lines that need to be updated every loop, removing the annoying flickering and making the game bettew optimized.

I was going to add a countdown anyways, but decided to onyly add it to the new version as I want the old version to be a "hoarded failed attempt" lol. Added a popup before the game loop starts with a countdown, nothing special.

Right after the "time's out" popup, I clear the input buffer using `curses.flushinp()` which flushes the input buffer. This makes the next screen appear without any inputs from before displayed in the input field.
