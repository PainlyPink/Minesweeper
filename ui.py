from minesweeper import Minesweeper  # Import the Minesweeper game
from time import time, sleep

# Class to manage the position on the board
class Pos:
    def __init__(self, board: tuple[int, int] | tuple = (9, 9)) -> None:
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
    def __init__(self, text) -> None:
        self.text = text  # Text to be colored

    # Convert RGB to ANSI escape code for colored text
    def rgb(self, clr) -> str:
        if type(clr) == str:
            r, g, b = clr[4:-1].replace(',', '').split()
        else:
            r, g, b = clr
        return f"\033[38;2;{r};{g};{b}m{self.text}\033[0m".strip()

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
    global grid, menu_screen, pos
    clear_screen()
    if menu_screen:
        # Display the menu
        print(Color("\tWelcome to the Quantum Minesweeper! 🐈‍\n").header())
        for i, key in enumerate(menu):
            if pos[1] == i:
                # Highlight the selected menu item
                print(Color(key).select())
                print(f'  {Color(menu[key].replace('\n', '\n  ')).desc()}')
            else:
                # Display other menu items
                print(Color(key).other())
    else:
        elapsed_time = 0
        if grid.start_time is not None:
            elapsed_time = int(time() - grid.start_time)

        header = Color(f'Flags left: {grid.n_mines - len(grid.flags)}\t\t\tElapsed time: {elapsed_time}s\n').desc()

        # Calculate the number of spaces for indentation
        header_width = len(header)
        board_width = size[0] * 2 - 1
        nspaces = (header_width - board_width) // 4
        print(nspaces)
            
        print(f'{' ' * (-nspaces//2) if nspaces < 0 else ''}' + header)
        if grid.win():
            # From mines to happy cats 😺
            for mpos in grid.mine_pos:
                grid.mine_values[mpos] = '😺'
            grid.mine_values[(pos[0], pos[1])] = '🥳'
            print(grid.mine_values)
            restart()
            return
        if grid.over: 
            print(Color("\t\t\tITS OVER 🙀").rgb((255, 0, 0)))
            print(grid.mine_values)
            restart()
            return

        # Display the game board
        board = [row.copy() for row in grid.mine_values.matrix]
        # Show player position
        board[pos[1]][pos[0]] = '🕵️'
        # Highlight neighbouring positions
        for npos in grid.get_neighbours(pos.pos):
            board[npos[1]][npos[0]] = Color(board[npos[1]][npos[0]]).select()

        for row in board:
            print(f'{' ' * nspaces if nspaces > 0 else ''}' + ' '.join(str(cell) for cell in row))

# Function to restart board play
def restart():
    global grid, menu_screen, pos
    menu_screen = True
    pos = Pos((1, len(menu)))
    grid = Minesweeper(size, 10)
    sleep(0.2)
    while True:
        if keyboard.read_event(suppress=True).event_type == keyboard.KEY_UP:
            break
    display()
    sleep(0.2)

# Function to handle the enter key action
def enter():
    global menu_screen, pos
    if menu_screen:
        # Handle menu actions
        if pos[1] == 0:
            menu_screen = False
            pos = Pos(size)
        elif pos[1] == len(menu) - 1:
            exit()
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
    
    global menu_screen, pos, grid
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
            grid = Minesweeper(size, 10)

    display()

# Main function to initialize and start the game
def main():
    display()
    print(Color("Suppresses other key actions while running").rgb((255, 0, 0)))
    while True:
        get_key()

# Initialize global variables
menu_screen: bool = True  # Flag to indicate if the menu is displayed
menu: dict[str, str] = {
    "Start": "[enter] to start...",
    "Controls": "[wasd] OR [←↑↓→] to move\n[enter] to open box\n[f] to flag box",
    "About": "Schrodinger has placed a few of his beloved cats inside these mysterious boxes\nThe uncertainty of whether they are alive or not weighs heavily on his mind\nHis faith in you compels him to seek your assistance\nAid Schrodinger in reuniting with his precious cats. Alive...",
    "Exit [esc]": "(ﾉ⚆_⚆)ﾉ"
}
pos: Pos = Pos((1, len(menu)))  # Initialize position for the menu
size = (21,) * 2  # Set the board size
grid: Minesweeper = Minesweeper(size, 10)  # Initialize the Minesweeper game
# main()  # Start the game
