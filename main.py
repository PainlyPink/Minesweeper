# Class to manage the position on the board
class Pos:
    def __init__(self, board: tuple[int, int] = (9, 9)) -> None:
        # Initialize with default position and board size
        self.pos = (0, 0)  # Current position (x, y)
        self.board = board  # Board dimensions (width, height)
    
    # Move up on the board
    def up(self):
        # Wrap around vertically if necessary
        self.pos = (self.pos[0], (self.pos[1] - 1) % self.board[1])
    
    # Move down on the board
    def down(self):
        # Wrap around vertically if necessary
        self.pos = (self.pos[0], (self.pos[1] + 1) % self.board[1])
    
    # Move left on the board
    def left(self):
        # Wrap around horizontally if necessary
        self.pos = ((self.pos[0] - 1) % self.board[0], self.pos[1])
    
    # Move right on the board
    def right(self):
        # Wrap around horizontally if necessary
        self.pos = ((self.pos[0] + 1) % self.board[0], self.pos[1])

    # Get item by index (0 for x, 1 for y)
    def __getitem__(self, index: int):
        return self.pos[index]

    # Represent the position as a string
    def __repr__(self):
        return ','.join([str(i) for i in self.pos])

# Class to manage colored text
class Color:
    def __init__(self, value) -> None:
        self.value = value  # Text to be colored

    # Convert RGB to ANSI escape code for colored text
    def rgb(self, clr) -> str:
        if type(clr) == str:
            r, g, b = clr[4:-1].replace(',', '').split()
        else:
            r, g, b = clr
        return f"\033[38;2;{r};{g};{b}m{self.value}\033[0m".strip()

    # Predefined color methods
    def header(self) -> str: return self.rgb('rgb(54, 186, 152)')
    def select(self) -> str: return self.rgb('rgb(233, 196, 106)')
    def desc(self) -> str: return self.rgb('rgb(130, 150, 140)')
    def other(self) -> str: return self.rgb('rgb(231, 111, 81)')

# Function to clear the terminal screen
from os import system, name
def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')

# Function to display the menu or game board
def display():
    clear_screen()
    if menu_screen:
        # Display the menu
        print(Color("\tWelcome!\n").header())
        for i, key in enumerate(menu):
            if pos[1] == i:
                # Highlight the selected menu item
                print(Color(key).select())
                print(f'  {Color(menu[key]).desc()}')
            else:
                # Display other menu items
                print(Color(key).other())
    else:
        # Display the game board
        if grid.over: print(Color("\t\t\tITS OVER FOR YOU 🤫").rgb((255, 0, 0)))
        board = [row.copy() for row in grid.mine_values.matrix]
        # Show player position
        board[pos[1]][pos[0]] = '🕵️'
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if not (dx == dy == 0):
                    # Highlight surrounding cells
                    board[pos[1] + dy][pos[0] + dx] = Color(board[pos[1] + dy][pos[0] + dx]).select()
        for row in board:
            print(' '.join(str(cell) for cell in row))
        print(Color(f'\t\t\tUnboxed: {grid.unboxed}\t\tPos: {pos}').header())

# Function to handle the enter key action
def enter():
    global menu_screen, pos
    if menu_screen:
        # Handle menu actions
        if pos[1] == 0:
            menu_screen = False
            pos = Pos(size)
        elif pos[1] == 1:
            pass # Add controls handling here if needed
    else:
        # Handle game actions
        if not grid.over:
            grid.move(pos.pos)

# Function to get keyboard input and update the game state
import keyboard
def get_key():
    event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        key: str = event.name.lower()  # type: ignore
    else: return
    
    global menu_screen, pos
    if key in ['up', 'w']:
        pos.up()
    elif key in ['left', 'a']:
        pos.left()
    elif key in ['down', 's']:
        pos.down()
    elif key in ['right', 'd']:
        pos.right()
    elif key in ['enter', 'space']:
        enter()
    elif key == 'f':
        if not grid.over: grid.flag(pos.pos)
    elif key == 'esc':
        if menu_screen:
            exit()
        else:
            menu_screen = True
            pos = Pos((1, len(menu)))

    display()

# Main function to initialize and start the game
def main():
    display()
    while True:
        get_key()

# Entry point of the script
if __name__ == "__main__":
    # Initialize global variables
    menu_screen: bool = True  # Flag to indicate if the menu is displayed
    menu: dict[str, str] = {
        "Start": "enter to start...",
        "Controls": "controls here",
        "About": "i am cool",
        "Exit [esc]": "( ﾉ ﾟｰﾟ)ﾉ"
    }
    pos: Pos = Pos((1, len(menu)))  # Initialize position for the menu
    from minesweeper import Minesweeper  # Import the Minesweeper game
    size = (20, 20)  # Set the board size
    grid: Minesweeper = Minesweeper(size, 10)  # Initialize the Minesweeper game
    main()  # Start the game
