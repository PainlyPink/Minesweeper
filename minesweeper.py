class Matrix2D:
    def __init__(self, val, size: tuple[int, int]) -> None:
        self.matrix = [[val for _ in range(size[0])] for _ in range(size[1])]
        self.size = size

    def __getitem__(self, pos):
        x, y = pos
        return self.matrix[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        self.matrix[y][x] = value

    def __repr__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def __iter__(self):
        for row in self.matrix:
            for value in row:
                yield value

    def __len__(self):
        return self.size[0] * self.size[1]


def mul(t: tuple[int, int], factor: int) -> tuple[int, int]:
    return t[0] * factor, t[1] * factor


def clear():
    from os import system, name
    system('cls' if name == 'nt' else 'clear')


class Minesweeper:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], mine_density: int) -> None:
        self.size = size
        self.n_mines = max(1, size[0] * size[1] * mine_density // 100)
        self.numbers = Matrix2D(0, size)
        self.chr_box = '📦'
        self.chr_flag = '\033[31m ψ\033[0m'
        self.chr_bomb = '💀'
        self.mine_values = Matrix2D(self.chr_box, size)
        self.mine_pos: set[tuple[int, int]] = set()
        self.flags: set[tuple[int, int]] = set()
        self.revealed: set[tuple[int, int]] = set()
        self.over = False
        self.set_mines(pos)
        self.set_values()
        self.reveal(pos)

    def get_neighbours(self, pos: tuple[int, int], factor: int = 1) -> list[tuple[int, int]]:
        x, y = pos
        res = [(x + dx, y + dy) for dx in range(-factor, factor + 1) for dy in range(-factor, factor + 1)
               if (dx, dy) != (0, 0) and 0 <= x + dx < self.size[0] and 0 <= y + dy < self.size[1]]
        return res

    def distance(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        from math import sqrt
        return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def set_mines(self, f_pos: tuple[int, int]):
        from random import choice
        from math import sqrt

        all_positions = [(x, y) for x in range(self.size[0]) for y in range(self.size[1])]
        bad_pos = set(self.get_neighbours(f_pos, 1) + [f_pos])
        valid_positions = [pos for pos in all_positions if pos not in bad_pos]
        spacing = sqrt((self.size[0] * self.size[1] / self.n_mines) - 1)
        
        max_attempts = 1000
        attempts = 0

        while len(self.mine_pos) < self.n_mines:
            pos = choice(valid_positions)
            if all(self.distance(pos, m_pos) > spacing for m_pos in self.mine_pos) or choice([False] * (self.size[0] * self.size[1]) + [True]):
                self.mine_pos.add(pos)
                self.numbers[pos] = -1
                attempts = 0
            else:
                attempts += 1

            if attempts > max_attempts:
                spacing *= 0.9
                attempts = 0

    def set_values(self):
        for pos in self.mine_pos:
            for n_pos in self.get_neighbours(pos):
                if self.numbers[n_pos] != -1:
                    self.numbers[n_pos] += 1

    def show_mines(self):
        for pos in self.mine_pos:
            self.mine_values[pos] = self.chr_bomb

    def reveal(self, pos: tuple[int, int]):
        if pos in self.revealed:
            return
        
        self.revealed.add(pos)
        if self.numbers[pos] == 0:
            self.mine_values[pos] = ' 0'
            for n_pos in self.get_neighbours(pos):
                self.reveal(n_pos)
        else:
            self.mine_values[pos] = f' {self.numbers[pos]}'

    def move(self, pos: tuple[int, int]):
        if self.numbers[pos] == -1:
            self.show_mines()
            self.mine_values[pos] = '☠️'
            self.over = True
            return -1
        else:
            self.reveal(pos)
            return 0

    def flag(self, pos: tuple[int, int]):
        if len(self.flags) >= self.n_mines or self.mine_values[pos] != self.chr_box or pos in self.flags or not (0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]):
            return -1
        self.mine_values[pos] = self.chr_flag
        self.flags.add(pos)


from random import randrange

while True:
    size = (18, 18)
    x, y = randrange(0, size[0]), randrange(0, size[1])
    m = Minesweeper((x, y), size, 10)
    print(m.n_mines)
    m.mine_values[(x, y)] = '🙏'
    m.show_mines()
    print(m.mine_values)
    input()
    clear()
