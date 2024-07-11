class Pos:
    def __init__(self, board: tuple[int, int] = (9, 9)) -> None:
        self.pos = (0, 0)
        self.prev = self.pos
        self.board = board
    
    def up(self):
        self.prev = self.pos
        self.pos = (self.pos[0], (self.pos[1] - 1) % self.board[1])
    def down(self):
        self.prev = self.pos
        self.pos = (self.pos[0], (self.pos[1] + 1) % self.board[1])
    def left(self):
        self.prev = self.pos
        self.pos = ((self.pos[0] - 1) % self.board[0], self.pos[1])
    def right(self):
        self.prev = self.pos
        self.pos = ((self.pos[0] + 1) % self.board[0], self.pos[1])

    def __getitem__(self, index: int):
        return self.pos[index]

    def __repr__(self):
        return ','.join([str(i) for i in self.pos])


class Color:
    def __init__(self, value) -> None:
        self.value = value

    def rgb(self, text: str, clr) -> str:
        if type(clr) == str:
            r, g, b = clr[4:-1].replace(',', '').split()
        else:
            r, g, b = clr
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def header(self) -> str: return self.rgb(self.value, 'rgb(54, 186, 152)')
    def select(self) -> str: return self.rgb(self.value, 'rgb(233, 196, 106)')
    def desc(self) -> str: return self.rgb(self.value, 'rgb(130, 150, 140)')
    def other(self) -> str: return self.rgb(self.value, 'rgb(231, 111, 81)')


from os import system, name
def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')


def display():
    clear_screen()
    if menu_screen:
        print(Color("\tWelcome!\n").header())
        for i, key in enumerate(menu):
            if pos[1] == i:
                print(Color(key).select())
                print(f'  {Color(menu[key]).desc()}')
            else:
                print(Color(key).other())
    else:
        board = [row.copy() for row in grid.mine_values.matrix]
        board[pos[1]][pos[0]] = '🕵️ '
        for row in board:
            print(' '.join(str(cell) for cell in row))


def enter():
    global menu_screen, pos
    if menu_screen:
        if pos[1] == 0:
            menu_screen = False
            pos = Pos(size)
        elif pos[1] == 1:
            pass # stuff
    else:
        grid.move(pos.pos)


import keyboard
def get_key():
    event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        key: str = event.name.lower() # type: ignore
    else: return
    
    if key in ['up', 'w']:
        pos.up()
    elif key in ['left', 'a']:
        pos.left()
    elif key in ['down', 's']:
        pos.down()
    elif key in ['right', 'd']:
        pos.right()
    elif key == 'enter':
        enter()

    display()


def main():
    display()
    while True:
        get_key()


if __name__ == "__main__":
    menu_screen: bool = True
    menu: dict[str, str] = {
        "Start": "enter to start...",
        "Controls": "controls here",
        "About": "i am cool",
        "Exit [esc, q, x]": "( ﾉ ﾟｰﾟ)ﾉ"
    }
    pos: Pos = Pos((1, len(menu)))
    from minesweeper import Minesweeper
    size = (20, 20)
    grid: Minesweeper = Minesweeper(size, 10)
    main()