from ui import main as ui_main
from subprocess import run, CalledProcessError

try:
    import keyboard  # Attempt to import the keyboard module
except ImportError:
    print("Module 'keyboard' not installed.")
    consent = input("Consent to install module (y/n): ").strip().lower()
    if consent == 'y':
        try:
            run(["pip", "install", "keyboard"], check=True)
            import keyboard  # Attempt to import the module again after installation
            print("Module 'keyboard' installed successfully.")
        except CalledProcessError:
            print("Failed to install the 'keyboard' module. Please install it manually.")
            exit(1)
        except ImportError:
            print("Failed to import the 'keyboard' module even after installation.")
            exit(1)
    else:
        print("Aborting execution.")
        exit(0)

if __name__ == "__main__":
    ui_main()  # Call the main function from ui.py
