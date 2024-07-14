from ui import main as ui_main
from subprocess import run

try:
    import keyboard  # Attempt to import the keyboard module
except ImportError:
    print("Module 'keyboard' not installed.")
    if input("Consent to install module (y/n): ").lower() == 'y':
        run("pip install keyboard".split())
    else:
        print("Aborting execution.")
        exit()

if __name__ == "__main__":
    ui_main()  # Call the main function from ui.py

