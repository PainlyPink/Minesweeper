import curses
import pyfiglet
import numpy as np
from minesweeper import Minesweeper

class Game(Minesweeper):
    pass

class MinesweeperMenu:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.menu = ('Play', 'Settings', 'About', 'Exit')
        self.color_themes = {
            'red': (
                (208, 72, 72),
                (254, 185, 65),
                (220, 111, 81)
            ),
            'purple': (
                (116, 105, 182),
                (224, 174, 208),
                (172, 135, 197)
            )
        }
        # header, selected, unselected
        self.show_colors = ((252, 220, 148), (120, 171, 168), (200, 207, 160))
        self.rgb_values = self.color_themes['red'] + self.show_colors
        self.opt = 0
        
        self.stdscr.nodelay(True)  # Continue even if no key is pressed
        self.stdscr.timeout(100)   # Wait 100ms before continuing
        curses.curs_set(0)
        self.init_colors()

    def init_colors(self):
        """Initialize color pairs using 256-color mode"""

        def get_256_colors():
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

        def find_closest_color(r, g, b, colors):
            distances = np.sqrt(np.sum((colors - np.array([r, g, b])) ** 2, axis=1))
            return np.argmin(distances)
        
        curses.start_color()
        try:
            colors = get_256_colors()
        except curses.error:
            self.stdscr.clear()
            self.print_center("256-color mode is not supported in this terminal.")
            self.print_center("Proceeding with limited colors. Press any key to continue...", 1)
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_WHITE)
            curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_WHITE)
            self.wait_for_key()
            return

        pairs = []
        for (r, g, b) in self.rgb_values:
            closest_color = find_closest_color(r, g, b, colors)
            pairs.append(closest_color)

        for i, color in enumerate(pairs, 1):
            curses.init_pair(i, color, curses.COLOR_BLACK)

    def print_center(self, text, offset=0, color_pair=0, Xoffset=0):
        """Prints text in the center of the screen"""
        h, w = self.stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        if Xoffset != 0:
            x = w // 2 - Xoffset
        y = h // 2
        self.stdscr.addstr(y + offset, x, text, curses.color_pair(color_pair))
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
            y = h // 2 - len(self.menu) + opt + 3
            if opt == self.opt:
                row = f'⟫ {row}'
                self.stdscr.addstr(y, x, row, curses.color_pair(2))
            else:
                self.stdscr.addstr(y, x, row, curses.color_pair(3))
        
        self.stdscr.addstr(h - 1, 0, "WASD or arrow keys to navigate...")
        self.stdscr.refresh()

    def wait_for_key(self): 
        while self.stdscr.getch() == -1:
            continue

    def on_enter(self):
        if self.opt == 0:  # play
            self.stdscr.clear()
            self.lets_game()
        
        elif self.opt == 1:  # settings
            self.stdscr.clear()
            self.print_center("Color Theme", -6, 4)
            
            menu = tuple(self.color_themes.keys())
            Xoffset = len(max(menu)) + 2
            opt = 0
            while True:
                for i in range(len(menu)):
                    if i == opt:
                        self.print_center(f"⟫ {menu[i]}", -1 + i, 5, Xoffset)
                    else:
                        self.print_center(f"  {menu[i]}", -1 + i, 6, Xoffset)
                self.stdscr.addstr(self.stdscr.getmaxyx()[0] - 1, 0, "Select theme with [enter] or [space]...")

                key = self.stdscr.getch()
                if key in (curses.KEY_UP, 119):  # 119 is 'w'
                    opt = (opt - 1) % len(menu)
                elif key in (curses.KEY_DOWN, 115):  # 115 is 's'
                    opt = (opt + 1) % len(menu)
                elif key in (10, 32):  # Enter keys
                    self.rgb_values = self.color_themes[menu[opt]] + self.show_colors
                    self.init_colors()
                    break
                elif key == 27:
                    break
        
        elif self.opt == 2:  # about
            self.stdscr.clear()
            self.print_center("About", -6, 4)  # Using color pair 4 (magenta)
            self.print_center("Schrodinger has placed a few of his beloved cats inside these mysterious boxes.", -3, 6)  # Using color pair 5 (cyan)
            self.print_center("The uncertainty of whether they are alive or not weighs heavily on his mind.", -2, 6)
            self.print_center("His faith in you compels him to seek your assistance.", -1, 6)
            self.print_center("Aid Schrodinger in reuniting with his precious cats. Alive...", 0, 6)
            self.wait_for_key()
        
        elif self.opt == len(self.menu) - 1:  # Exit option
            self.is_game = False
    
    def lets_game(self):
        """Play Minesweeper !"""
        ms = Minesweeper((21, 21), 10)
        pos = (0, 0)
        while not ms.over:
            pass
    
    def main(self):
        """Main game loop"""
        
        self.is_game = True
        self.print_menu()
        while self.is_game:
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
print(r"ヾ(＾ ∇ ＾).")
