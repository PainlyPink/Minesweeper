class Pos:
    def __init__(self, pos: tuple[int, int] = (0, 0), board: tuple[int, int] = (9, 9)) -> None:
        self.pos = pos
        self.board = board
    
    def up(self):
        self.pos = (self.pos[0], (self.pos[1] - 1) % self.board[1])
    def down(self):
        self.pos = (self.pos[0], (self.pos[1] + 1) % self.board[1])
    def left(self):
        self.pos = ((self.pos[0] - 1) % self.board[0], self.pos[1])
    def right(self):
        self.pos = ((self.pos[0] + 1) % self.board[0], self.pos[1])

    def __repr__(self):
        return ','.join([str(i) for i in self.pos])


from os import system, name
def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')


import keyboard
def get_key():
    event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)
    if event.event_type == keyboard.KEY_DOWN:
        key: str = event.name.lower()
    else: return
    
    if key in ['up', 'w']:
        pos.up()
    elif key in ['left', 'a']:
        pos.left()
    elif key in ['down', 's']:
        pos.down()
    elif key in ['right', 'd']:
        pos.right()
        
    print(pos)


def main():
    while True:
        get_key()


if __name__ == "__main__":
    pos = Pos()
    clear_screen()
    main()