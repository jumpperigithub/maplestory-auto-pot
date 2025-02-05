# MapleStory Health and Mana Bot

This script was done for a old childhood game MapleStory (The old and original version) in a brief afternoon tea moment.  It is a bot designed to monitor and replenish health and mana in the game by detecting specific pixel colors on the screen. It uses keyboard automation to press keys when health or mana is low.

Classes:
  Point: A dataclass representing a point on the screen with x and y coordinates.
  StatusOverlay: A class to create and manage a Tkinter overlay showing the bot's status.
  ScreenCapture: A class to capture screen pixels and get their RGB color.
  ResourceMonitor: A class to monitor a specific resource (health or mana) and replenish it if needed.
  GameState: A class to manage the overall game state, including checking if the game screen is active, toggling pause, and running the main loop.

Constants:
  GAME_CONFIG: A dictionary containing configuration for screen check, health, and mana positions and colors.

## How to use

# Python

This script requires Python 3.6 or higher.

First install the required packages by running `pip install -r requirements.txt`.

> Configure the GAME_CONFIG constants in `main.py` with the correct color and position values and key binds that you use for replenishing health and mana in the game.

Configuration:
  - Update the GAME_CONFIG constants in `main.py` with the correct color and position values and key binds that you use for replenishing health and mana in the game.
  - Run the `get_pixel_color.py` script (with `python get_pixel_color.py`) to find the RGB color and pixel coordinates of the health and mana
  - Adjust the color tolerance in the ResourceMonitor class if needed.

Usage:
  - Run the script to start the bot by running `python main.py`.
  - The bot will start monitoring the game screen and health/mana levels.
  - If health or mana is low, the bot will press the corresponding key to replenish it.
  - The bot checks if the pixels are filled with the correct color and if not, it will press the corresponding key to replenish it.
  - Your coordinates/positions will determine what level of health/mana you want to replenish at. 
  - Press 'page up' to pause/resume the bot.
  - Press 'F12' to quit the bot.