import curses
import pyfiglet

menu = ('Play', 'Settings', 'About', 'Exit')

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

def print_menu(stdscr: curses.window, select_opt: int):
    """prints menu with highlighted selection"""
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    header = str(pyfiglet.figlet_format("* minesweeper *"))
    for i, line in enumerate(header.split('\n')):
        stdscr.addstr(i + 1, w // 2 - len(line) // 2, line, curses.color_pair(3))

    for opt, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) + opt
        if opt == select_opt:
            stdscr.addstr(y, x, row, curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        
    # Add navigation instructions
    stdscr.addstr(h - 1, 0, "WASD or arrow keys to navigate...")
    stdscr.refresh()

def wait_for_key(stdscr: curses.window): 
    while stdscr.getch() == -1:
        continue

def on_enter(stdscr: curses.window):
    print_center(stdscr, f"Entered {menu[opt]} !")
    # menu = ('Play', 'Settings', 'About', 'Exit')
    if opt == 0:
        stdscr.clear()
        print_center(stdscr, "in play")
        wait_for_key(stdscr)
    elif opt == 1:
        stdscr.clear()
        print_center(stdscr, "in Settings")
        wait_for_key(stdscr)
    elif opt == 2:
        stdscr.clear()
        print_center(stdscr, "in About")
        wait_for_key(stdscr)
    elif opt == len(menu) - 1:  # Exit option
        exit()

def main(stdscr: curses.window):
    """main game loop"""
    stdscr.nodelay(True)  # Continue even if no key is pressed
    stdscr.timeout(100)   # Wait 100ms before continuing
    curses.curs_set(0)
    init_colors()
    
    global opt
    opt = 0
    print_menu(stdscr, opt)

    while True:
        key = stdscr.getch()
        if key == -1: continue
        
        if key in (curses.KEY_UP, 119):  # 119 is 'w'
            opt = (opt - 1) % len(menu)
        elif key in (curses.KEY_DOWN, 115):  # 115 is 's'
            opt = (opt + 1) % len(menu)
        elif key in (curses.KEY_ENTER, 32, 10, 13):  # Space, Enter keys
            on_enter(stdscr)
        print_menu(stdscr, opt)

curses.wrapper(main)

# Clear the terminal screen
from os import system, name
system('cls' if name == 'nt' else 'clear')
