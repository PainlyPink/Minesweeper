import curses
import pyfiglet

menu = ('Home', 'Play', 'Scoreboard', 'Exit')

def init_colors():
    """initialize color pairs"""
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

def print_center(stdscr: curses.window, text: str):
    """prints text in center of screen"""
    h, w = stdscr.getmaxyx()
    x, y = w // 2 - len(text) // 2, h // 2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def print_menu(stdscr: curses.window, select_idx: int):
    """prints menu with highlighted selection"""
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    header = str(pyfiglet.figlet_format("* minesweeper *"))
    for i, line in enumerate(header.split('\n')):
        stdscr.addstr(i + 1, w // 2 - len(line) // 2, line, curses.color_pair(3))

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) + idx
        if idx == select_idx:
            stdscr.addstr(y, x, row, curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        
    # Add navigation instructions
    stdscr.addstr(h - 1, 0, "WASD or arrow keys to navigate...")
    stdscr.refresh()

def main(stdscr: curses.window):
    """main game loop"""
    stdscr.nodelay(True)  # Continue even if no key is pressed
    stdscr.timeout(100)   # Wait 100ms before continuing
    curses.curs_set(0)
    init_colors()
    
    idx = 0
    print_menu(stdscr, idx)

    while True:
        key = stdscr.getch()

        if key in (curses.KEY_UP, 119):  # 119 is 'w'
            idx = (idx - 1) % len(menu)
        elif key in (curses.KEY_DOWN, 115):  # 115 is 's'
            idx = (idx + 1) % len(menu)
        elif key in (curses.KEY_ENTER, 32, 10, 13):  # Space, Enter keys
            print_center(stdscr, f"Entered {menu[idx]} !")
            if idx == len(menu) - 1:  # Exit option
                break
            stdscr.getch()

        print_menu(stdscr, idx)

curses.wrapper(main)

# Clear the terminal screen
from os import system, name
system('cls' if name == 'nt' else 'clear')
