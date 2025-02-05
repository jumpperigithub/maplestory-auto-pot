import time
import keyboard
import mss
import numpy as np
from colorama import init

# Initialize Colorama for Windows support
init()

DEBUG_MODE = True

# Health bar coordinates
HEALTH_BAR_X = 838
HEALTH_BAR_Y = 1390

FULL_HEALTH_COLOR = (255, 0, 0)
LOW_HEALTH_COLOR = (255, 255, 255)

# Mana bar coordinates
MANA_BAR_X = 1140
MANA_BAR_Y = 1389

FULL_MANA_COLOR = (0, 153, 255)
LOW_MANA_COLOR = (255, 255, 255)

# Define keys
HEAL_KEY = "delete"
MANA_KEY = "end"

# Check that the game is on the correct screen
# Test this by checking UI elements or colors unique to the game screen
GAME_SCREEN_COLOR = (255, 137, 15)
GAME_SCREEN_X = 129
GAME_SCREEN_Y = 1382

def get_pixel_color(x, y):
    """Capture screen and get the corrected RGB color at (x, y)."""
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = np.array(sct.grab(monitor))  # Capture pixel
        b, g, r = img[0, 0, :3]  # Fix BGR to RGB
        return (r, g, b)

def rgb_to_ansi(r, g, b):
    """Convert RGB to an ANSI escape code for terminal color."""
    return f"\033[48;2;{r};{g};{b}m\033[38;2;{255-r};{255-g};{255-b}m"

print("Bot started. Press 'q' to quit.")

while True:
    # Clear console output
    print("\033[H\033[J", end="")
    
    # Check that the game is on correct screen
    e, f, g = get_pixel_color(GAME_SCREEN_X, GAME_SCREEN_Y)
    if (e, f, g) == GAME_SCREEN_COLOR:
        print("\nGame screen detected.")
    else:
        print("\nGame screen not detected. Please move the game to the correct screen.")
        continue
    
    # Get the color of the health bar pixel
    r, g, b = get_pixel_color(HEALTH_BAR_X, HEALTH_BAR_Y)

    # Debug mode: Print detected color in the terminal with background color
    if DEBUG_MODE:
        color_code = rgb_to_ansi(r, g, b)
        reset_code = "\033[0m"
        print(f"\r{color_code} Health Bar Color: ({r}, {g}, {b}) at ({HEALTH_BAR_X}, {HEALTH_BAR_Y}) {reset_code}", end="", flush=True)

    # Check if HEALTH is low
    if (r, g, b) != FULL_HEALTH_COLOR:
        # Debug rgb
        print(f"\nHealth Bar Color: ({r}, {g}, {b})")
        print("\n⚠️ Health is low! Drinking potion... ⚠️")
        keyboard.press_and_release(HEAL_KEY)
        time.sleep(0.5)

    # Get the color of the mana bar pixel
    h, i, j = get_pixel_color(MANA_BAR_X, MANA_BAR_Y)
    # Debug mode: Print detected color in the terminal with background color
    if DEBUG_MODE:
        color_code = rgb_to_ansi(h, i, j)
        reset_code = "\033[0m"
        print(f"\r{color_code} Mana Bar Color: ({r}, {g}, {b}) at ({MANA_BAR_X}, {MANA_BAR_Y}) {reset_code}", end="", flush=True)


    # Check if MANA is low
    if (h, i, j) != FULL_MANA_COLOR:
        # Debug rgb
        print(f"\nMana Bar Color: ({r}, {g}, {b})")
        print("\n⚠️ Mana is low! Drinking potion... ⚠️")
        keyboard.press_and_release(MANA_KEY)
        time.sleep(0.5)
    

    # Quit if 'q' is pressed
    if keyboard.is_pressed("q"):
        print("\nBot stopped.")
        break

    time.sleep(0.1) # Reduce CPU usage
