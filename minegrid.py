import random

class Board:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], n_mines: int) -> None:
        self.cpos = pos
        self.size_x = size[0]
        self.size_y = size[1]
        self.n_mines = n_mines
        self.board = [[0] * self.size_x for _ in range(self.size_y)]
        self.mine_positions = []
        self.initial_safe_zone = self.get_initial_safe_zone()
        self.place_mines()
        self.calculate_neighboring_mines()

    def get_initial_safe_zone(self) -> list[tuple[int, int]]:
        directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        initial_safe_zone = [(self.cpos[0] + dx, self.cpos[1] + dy) for dx, dy in directions]
        return [(x, y) for x, y in initial_safe_zone if 0 <= x < self.size_x and 0 <= y < self.size_y]

    def place_mines(self) -> None:
        mines = 0
        while mines < self.n_mines:
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            if self.board[y][x] == 0 and (x, y) not in self.initial_safe_zone:
                self.mine_positions.append((x, y))
                self.board[y][x] = -1
                mines += 1

    def calculate_neighboring_mines(self) -> None:
        directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]
        for x, y in self.mine_positions:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size_x and 0 <= ny < self.size_y and self.board[ny][nx] != -1:
                    self.board[ny][nx] += 1

    def display_board(self) -> None:
        for row in self.board:
            print(f'\t{"  ".join("*" if cell == -1 else str(cell) for cell in row)}')

    def get_cell_value(self, x: int, y: int) -> int:
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            return self.board[y][x]
        else:
            raise ValueError("Position out of bounds")

if __name__ == "__main__":
    cpos = (2, 6)
    board = Board(cpos, (9, 9), n_mines=10)
    print(board.get_initial_safe_zone())
    board.board[6][2] = 9
    board.display_board()
    cell_value = board.get_cell_value(*cpos)
    print(f"Value at position {cpos}: {cell_value}")
