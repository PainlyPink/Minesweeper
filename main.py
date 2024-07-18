import curses
from subprocess import run, CalledProcessError

def check_and_install_keyboard(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.addstr(0, 0, "Checking for 'keyboard' module...")
    stdscr.refresh()
    
    try:
        import keyboard
        stdscr.addstr(1, 0, "Module 'keyboard' is already installed.")
        stdscr.addstr(2, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
    except ImportError:
        stdscr.addstr(1, 0, "Module 'keyboard' not installed.")
        stdscr.addstr(2, 0, "Consent to install module (y/n): ")
        stdscr.refresh()
        
        consent = stdscr.getch()
        if consent == ord('y'):
            stdscr.addstr(3, 0, "Installing 'keyboard' module...")
            stdscr.refresh()
            try:
                run(["pip", "install", "keyboard"], check=True)
                import keyboard  # Attempt to import the module again after installation
                stdscr.addstr(4, 0, "Module 'keyboard' installed successfully.")
                stdscr.addstr(5, 0, "Press any key to continue...")
                stdscr.refresh()
                stdscr.getch()
            except CalledProcessError:
                stdscr.addstr(4, 0, "Failed to install the 'keyboard' module. Please install it manually.")
                stdscr.addstr(5, 0, "Press any key to exit.")
                stdscr.refresh()
                stdscr.getch()
                exit(1)
            except ImportError:
                stdscr.addstr(4, 0, "Failed to import the 'keyboard' module even after installation.")
                stdscr.addstr(5, 0, "Press any key to exit.")
                stdscr.refresh()
                stdscr.getch()
                exit(1)
        else:
            stdscr.addstr(3, 0, "Aborting execution.")
            stdscr.addstr(4, 0, "Press any key to exit.")
            stdscr.refresh()
            stdscr.getch()
            exit(0)

if __name__ == "__main__":
    curses.wrapper(check_and_install_keyboard)
    from ui import main as ui_main
    ui_main()  # Call the main function from ui.py
