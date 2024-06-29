import random

class Size:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

def place_mines(n_mines: int) -> None:
    grid: list[list[int]] = board
    mines: int = 0
    while mines < n_mines:
        x: int = random.randint(0, board_size.x - 1)
        y: int = random.randint(0, board_size.y - 1)
        if grid[y][x] == 0:
            mine_pos.append((x, y))
            grid[y][x] = -1
            mines += 1

def display_board() -> None:
    for row in board:
        print(f'\t{" ".join("*" if cell == -1 else str(cell) for cell in row)}')

def calculate_neighboring_mines():
    directions: list[tuple[int, int]] = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
    directions.remove((0, 0))
    
    for x, y in mine_pos:
        for dx, dy in directions:
            if x < -dx or y < -dy:
                continue
            pos = (x + dx, y + dy)
            if pos not in mine_pos:
                try:
                    board[pos[1]][pos[0]] += 1
                except IndexError:
                    pass

board_size: Size = Size(9, 9)
board: list[list[int]] = [[0] * board_size.x for _ in range(board_size.y)]
mine_pos: list[tuple[int, int]] = []
n_mines: int = sum((board_size.x, board_size.y)) // 2
place_mines(n_mines)
calculate_neighboring_mines()
print(f'{'-' * 34}')
display_board()
print(f'{'-' * 34}')
print(f"No. of mines: {n_mines}")
