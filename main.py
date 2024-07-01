from os import system, name
import keyboard

def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')
    
def rgb(text: str, clr) -> str:
    if type(clr) == str:
        r, g, b = clr[4:-1].replace(',', '').split()
    else:
        r, g, b = clr
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def play(dx: int, dy: int):
    global pos_x, pos_y
    board[pos_y][pos_x] = piece
    pos_x = (pos_x + dx) % board_size[0]
    pos_y = (pos_y + -dy) % board_size[1]
    board[pos_y][pos_x] = player
    display_board()

def display_board() -> None:
    clear_screen()
    for row in board:
        for i in row:
            if i == player:
                print(rgb(i, 'rgb(230, 185, 166)'), end=' ')
            else:
                print(rgb(i, 'rgb(47, 54, 69)'), end=' ')
        print()

def display_menu(step: int) -> None:
    clear_screen()
    print(rgb("\tWelcome!", 'rgb(54, 186, 152)'))
    global pos_menu
    pos_menu = (pos_menu - step) % len(menu)
    for i in range(len(menu)):
        if i == pos_menu:
            s = f'{menu[i] + description[i]}'
            print(rgb(f'-> {s}', 'rgb(233, 196, 106)'))
        else:
            print(rgb(f'{menu[i]}', 'rgb(231, 111, 81)'))

def menu_choice() -> None:
    if pos_menu == 0:
        global start; start = not start
        display_board()
    elif pos_menu == len(menu) - 1:
        quit()

def get_key() -> None:
    global game
    if not game: return
    event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_UP:
        key: str = event.name.lower()
    else: return

    global start
    if start:
        if key in ['esc', 'x', 'q']:
            start = not start
            global pos_x, pos_y
            board[pos_y][pos_x] = piece
            pos_x = pos_y = 0
            board[pos_y][pos_x] = player
            display_menu(pos_menu)
        elif key in ['up', 'w']:
            play(0, 1)
        elif key in ['left', 'a']:
            play(-1, 0)
        elif key in ['down', 's']:
            play(0, -1)
        elif key in ['right', 'd']:
            play(1, 0)
    else:
        if key in ['esc', 'x', 'q']:
            quit()
        elif key in ['up', 'w']:
            display_menu(1)
        elif key in ['down', 's']:
            display_menu(-1)
        elif key == 'enter':
            game = False
            menu_choice()
            game = True

def main() -> None:
    clear_screen()
    display_menu(0)
    while True:
        get_key()

if __name__ == "__main__":
    game: bool = True; start: bool = False
    menu: list[str] = ['Start', 'Controls', 'About', 'Exit [esc, x, q]']
    description: list[str] = [':\n\tenter to start...', ':\n\twasd OR arrows to move\n\tenter to open box\n\tf to flag box', ':\n\tmade by me', '\n\t🥺']
    pos_menu: int = 0; pos_x: int = 0; pos_y: int = 0
    board_size: tuple[int, int] = (9, 9)
    piece: str = '📦'; player: str = ' ψ'
    board: list[list] = [[piece for _ in range(board_size[0])] for _ in range(board_size[1])]
    board[pos_y][pos_x] = player
    main()
