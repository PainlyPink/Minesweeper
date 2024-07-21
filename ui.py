import curses
import pyfiglet
import numpy as np

class MinesweeperMenu:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.menu = ('Play', 'Settings', 'About', 'Exit')
        self.rgb_values = [
            (208, 72, 72),
            (254, 185, 65),
            (231, 111, 81)
        ]
        self.opt = 0

    def get_256_colors(self):
        colors = []
        # Standard colors
        for i in range(8):
            colors.append(curses.color_content(i))
        # High-intensity colors
        for i in range(8, 16):
            colors.append(curses.color_content(i))
        # 6x6x6 color cube
        for r in [0, 95, 135, 175, 215, 255]:
            for g in [0, 95, 135, 175, 215, 255]:
                for b in [0, 95, 135, 175, 215, 255]:
                    colors.append((r, g, b))
        # Grayscale colors
        for i in range(24):
            v = 8 + i * 10
            colors.append((v, v, v))
        return np.array(colors)

    def find_closest_color(self, r, g, b, colors):
        distances = np.sqrt(np.sum((colors - np.array([r, g, b])) ** 2, axis=1))
        return np.argmin(distances)

    def init_colors(self):
        """Initialize color pairs using 256-color mode"""
        curses.start_color()
        try:
            colors = self.get_256_colors()
        except curses.error:
            self.stdscr.clear()
            self.print_center("256-color mode is not supported in this terminal.")
            self.print_center("Proceeding without colors. Press any key to continue...", 1)
            self.wait_for_key()
            return

        pairs = []
        for (r, g, b) in self.rgb_values:
            closest_color = self.find_closest_color(r, g, b, colors)
            pairs.append(closest_color)

        for i, color in enumerate(pairs, 1):
            curses.init_pair(i, color, curses.COLOR_BLACK)

    def print_center(self, text, offset=0):
        """Prints text in the center of the screen"""
        h, w = self.stdscr.getmaxyx()
        x, y = w // 2 - len(text) // 2, h // 2
        self.stdscr.addstr(y + offset, x, text)
        self.stdscr.refresh()

    def print_menu(self):
        """Prints menu with highlighted selection"""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        header = str(pyfiglet.figlet_format("* minesweeper *"))
        for i, line in enumerate(header.split('\n')):
            self.stdscr.addstr(i + 1, w // 2 - len(line) // 2, line, curses.color_pair(1))

        for opt, row in enumerate(self.menu):                
            x = w // 2 - 5
            y = h // 2 - len(self.menu) + opt
            if opt == self.opt:
                row = f'⟫ {row}'
                self.stdscr.addstr(y, x, row, curses.color_pair(2))
            else:
                self.stdscr.addstr(y, x, row, curses.color_pair(3))
        
        self.stdscr.refresh()
        
        # Add navigation instructions
        self.stdscr.addstr(h - 1, 0, "WASD or arrow keys to navigate...")
        self.stdscr.refresh()

    def wait_for_key(self): 
        while self.stdscr.getch() == -1:
            continue

    def on_enter(self):
        self.print_center(f"Entered {self.menu[self.opt]} !")
        if self.opt == 0:
            self.stdscr.clear()
            self.print_center("in Play")
            self.wait_for_key()
        elif self.opt == 1:
            self.stdscr.clear()
            self.print_center("in Settings")
            self.wait_for_key()
        elif self.opt == 2:
            self.stdscr.clear()
            self.print_center("in About")
            self.wait_for_key()
        elif self.opt == len(self.menu) - 1:  # Exit option
            exit()
    
    def main(self):
        """Main game loop"""
        self.stdscr.nodelay(True)  # Continue even if no key is pressed
        self.stdscr.timeout(100)   # Wait 100ms before continuing
        curses.curs_set(0)
        self.init_colors()
        
        self.print_menu()

        while True:
            key = self.stdscr.getch()
            if key == -1: continue
            
            if key in (curses.KEY_UP, 119):  # 119 is 'w'
                self.opt = (self.opt - 1) % len(self.menu)
            elif key in (curses.KEY_DOWN, 115):  # 115 is 's'
                self.opt = (self.opt + 1) % len(self.menu)
            elif key in (curses.KEY_ENTER, 32, 10, 13):  # Space, Enter keys
                self.on_enter()
            self.print_menu()

def start(stdscr):
    menu = MinesweeperMenu(stdscr)
    menu.main()

curses.wrapper(start)

# Clear the terminal screen
from os import system, name
system('cls' if name == 'nt' else 'clear')
