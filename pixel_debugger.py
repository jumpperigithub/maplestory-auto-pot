import time
import pyautogui
import keyboard
import mss
import numpy as np
from colorama import init

# Initialize Colorama for Windows compatibility
init()

def get_pixel_color(x, y):
    """Capture screen and get the corrected RGB color at (x, y)."""
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = np.array(sct.grab(monitor))  # Capture pixel
        b, g, r = img[0, 0, :3]  # Fix BGR to RGB
        return (r, g, b)

def rgb_to_ansi(r, g, b):
    """Convert RGB to an ANSI escape code for console color."""
    return f"\033[48;2;{r};{g};{b}m\033[38;2;{255-r};{255-g};{255-b}m"

print("Move the mouse to a position and press 'c' to capture color.")
print("Press 'q' to quit.")

while True:
    x, y = pyautogui.position()
    r, g, b = get_pixel_color(x, y)

    # Apply ANSI escape codes for background & text color
    color_code = rgb_to_ansi(r, g, b)
    reset_code = "\033[0m"

    print(f"\r{color_code} Mouse at ({x}, {y}) | Color: ({r}, {g}, {b}) {reset_code}", end="", flush=True)

    if keyboard.is_pressed("c"):
        print(f"\nCaptured: X={x}, Y={y} | Color=({r}, {g}, {b})")
        time.sleep(0.2)  # Prevent multiple captures from a single press

    if keyboard.is_pressed("q"):
        print("\nExiting...")
        break

    time.sleep(0.1)  # Reduce CPU usage
