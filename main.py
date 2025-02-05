from dataclasses import dataclass
from typing import Tuple
import keyboard
import mss
import numpy as np
import time
import random
import tkinter as tk
from tkinter import ttk

@dataclass
class Point:
    x: int
    y: int

# Constants. UPDATE THESE VALUES TO MATCH YOUR GAME
# USE pixel_debugger.py TO FIND THE CORRECT COORDINATES AND COLORS
# RUN "python pixel_debugger.py" and move the mouse to the desired position
# Press 'q' to quit the app and get the RGB color values and coordinates
GAME_CONFIG = {
    'screen_check': {
        'position': Point(129, 1382),
        'color': (255, 137, 15)
    },
    'health': {
        'position': Point(838, 1390),
        'full_color': (255, 0, 0),  # Changed from blue to red
        'key': 'delete'
    },
    'mana': {
        'position': Point(1140, 1389),
        'full_color': (0, 153, 255),
        'key': 'end'
    }
}

class StatusOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bot Status")
        self.root.geometry("150x30+0+0")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.8)
        self.root.overrideredirect(True)
        
        # Status label
        self.status_label = ttk.Label(
            self.root, 
            text="▶ RUNNING", 
            font=('Arial', 12, 'bold'),
            foreground='green'
        )
        self.status_label.pack(pady=5)
    
    def update_status(self, is_paused: bool):
        self.root.after(0, self._do_update, is_paused)
    
    def _do_update(self, is_paused: bool):
        if is_paused:
            self.status_label.config(text="⏸ PAUSED", foreground='red')
        else:
            self.status_label.config(text="▶ RUNNING", foreground='green')
    
    def update(self):
        try:
            self.root.update()
        except Exception as e:
            print(f"Error updating overlay: {e}")
    
    def cleanup(self):
        try:
            self.root.destroy()
        except:
            pass

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
    
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        screenshot = np.array(self.sct.grab(monitor))
        # Convert numpy uint8 to regular Python ints
        b, g, r = map(int, screenshot[0, 0, :3])
        return (r, g, b)
    
    def __del__(self):
        self.sct.close()

class ResourceMonitor:
    def __init__(self, position: Point, full_color: Tuple[int, int, int], key: str, name: str, screen: ScreenCapture):
        self.position = position
        self.full_color = full_color
        self.key = key
        self.name = name
        self.screen = screen
        self.color_tolerance = 30 
        self.last_replenish_time = 0

    def get_color(self) -> Tuple[int, int, int]:
        return self.screen.get_pixel_color(self.position.x, self.position.y)

    def needs_replenish(self) -> bool:
        r, g, b = self.get_color()
        fr, fg, fb = self.full_color
        return (abs(r - fr) > self.color_tolerance or 
                abs(g - fg) > self.color_tolerance or 
                abs(b - fb) > self.color_tolerance)

    def replenish(self):
        random_delay = random.uniform(0, 0.1)
        time.sleep(random_delay)
        keyboard.press_and_release(self.key)
        print(f"\n⚠️ {self.name} is low! Drinking potion... (delayed {int(random_delay*1000)}ms)")
        time.sleep(0.5)

    def debug_info(self) -> str:
        current_color = self.get_color()
        color_diff = tuple(abs(c1 - c2) for c1, c2 in zip(current_color, self.full_color))
        return (f"{self.name} at ({self.position.x}, {self.position.y})\n"
                f"  Expected: RGB{self.full_color}\n"
                f"  Got:      RGB{current_color}\n"
                f"  Diff:     RGB{color_diff} (tolerance: {self.color_tolerance})")

class GameState:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.screen = ScreenCapture()
        self.health = ResourceMonitor(
            GAME_CONFIG['health']['position'],
            GAME_CONFIG['health']['full_color'],
            GAME_CONFIG['health']['key'],
            'Health',
            self.screen
        )
        self.mana = ResourceMonitor(
            GAME_CONFIG['mana']['position'],
            GAME_CONFIG['mana']['full_color'],
            GAME_CONFIG['mana']['key'],
            'Mana',
            self.screen
        )
        self.debug_buffer = []
        self.paused = False
        self.last_pause_time = 0
        self.overlay = StatusOverlay()
        keyboard.unhook_all()
        keyboard.on_press_key("page up", self._handle_pause_key, suppress=True)
        keyboard.on_press_key("F12", self._handle_quit_key, suppress=True)
        self.running = True
    
    def _handle_pause_key(self, event):
        try:
            self.toggle_pause()
        except Exception as e:
            print(f"Error handling pause: {e}")
        return False  # Don't suppress other handlers

    def _handle_quit_key(self, _):
        self.running = False

    def toggle_pause(self):
        current_time = time.time()
        if current_time - self.last_pause_time > 0.3:
            self.paused = not self.paused
            self.last_pause_time = current_time

    def print_debug(self):
        print("\033[H\033[J", end="")
        print("\nCurrent Status:")
        print("\n".join(self.debug_buffer))
        self.debug_buffer = []  # Clear buffer

    def is_game_screen_active(self) -> bool:
        screen_check = GAME_CONFIG['screen_check']
        color = self.screen.get_pixel_color(
            screen_check['position'].x,
            screen_check['position'].y
        )
        return color == screen_check['color']

    def run(self):
        print("\033[H\033[J", end="")
        print("Bot started. Press 'F12' to quit.")
        
        try:
            while self.running:
                # Update overlay each loop
                self.overlay.update_status(self.paused)
                self.overlay.update()

                # Check game screen and pause status
                if not self.is_game_screen_active() or self.paused:
                    if self.paused:
                        self.debug_buffer.append("\nBot is PAUSED")
                        self.debug_buffer.append("Press 'page up' to resume")
                    else:
                        self.debug_buffer.append("\nGame screen not detected.")
                    self.print_debug()
                    time.sleep(0.1)
                    continue

                # Normal operation
                self.debug_buffer.append("\nGame screen detected.")
                self.debug_buffer.append(f"Status: {'RUNNING' if not self.paused else 'PAUSED'}")

                if self.debug_mode:
                    self.debug_buffer.append(self.health.debug_info())
                    self.debug_buffer.append(self.mana.debug_info())
                
                self.print_debug()

                if self.health.needs_replenish():
                    self.health.replenish()

                if self.mana.needs_replenish():
                    self.mana.replenish()
                
                time.sleep(0.1)

        except Exception as e:
            # Clear console
            print("\033[H\033[J", end="")
            self.debug_buffer.append(f"Error in main loop: {e}")
            time.sleep(0.1)

        finally:
            self.overlay.cleanup()
            keyboard.unhook_all()

if __name__ == "__main__":
    game = GameState(debug_mode=True)
    try:
        game.run()
    except KeyboardInterrupt:
        game.overlay.cleanup()