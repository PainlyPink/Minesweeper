import curses

menu = ('Home', 'Play', 'Scoreboard', 'Exit')

def init_colors():
    """initialize color pairs"""
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_MAGENTA)

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

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) + idx
        if idx == select_idx:
            stdscr.addstr(y, x, row, curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        
    stdscr.refresh()

def main(stdscr: curses.window):
    """main game loop"""
    curses.curs_set(0)
    init_colors()
    
    idx = 0
    print_menu(stdscr, idx)

    while 1:
        key = stdscr.getch()

        if key in (curses.KEY_UP, 119):
            idx = (idx - 1) % len(menu)
        elif key in (curses.KEY_DOWN, 115):
            idx = (idx + 1) % len(menu)
        elif key in (curses.KEY_ENTER, 32, 10, 13):
            print_center(stdscr, f"Entered {menu[idx]} !")
            stdscr.getch()

            if idx == len(menu) - 1:
                break
        print_menu(stdscr, idx)

curses.wrapper(main)

from os import system, name
system('cls' if name == 'nt' else 'clear')