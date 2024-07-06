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
    return (t[0] * factor, t[1] * factor)

def clear():
    from os import system, name
    system('cls' if name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], mine_density: int) -> None:
        self.over = False; self.size = size
        self.n_mines = size[0] * size[1] * mine_density // 100
        self.numbers = Matrix2D(0, size)
        self.chr_box = '📦'; self.chr_flag = '\033[31m ψ\033[0m'; self.chr_bomb = '💀'
        self.mine_values = Matrix2D(self.chr_box, size)
        self.mine_pos: set[tuple[int, int]] = set(); self.flags: list[tuple[int, int]] = []
        self.revealed: set[tuple[int, int]] = set()
        self.set_mines(pos)
        self.set_values()
        self.reveal(pos)
    
    def get_neighbours(self, pos: tuple[int, int], factor: int = 1) -> list[tuple[int, int]]:
        x, y = pos
        res = []
        dirs = [(i, j) for i in range(-factor, factor + 1) for j in range(-factor, factor + 1)]
        dirs.remove((0, 0))
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            in_check = -1 < nx < self.size[0] and -1 < ny < self.size[1]
            if not in_check: continue
            res.append((nx, ny))
        return res
        
    def set_mines(self, f_pos: tuple[int, int]):
        from random import randint
        bad_pos: list[tuple[int, int]]  = self.get_neighbours(f_pos, 2)
        bad_pos.append(f_pos)
        while len(self.mine_pos) < self.n_mines:
            i = randint(0, self.size[0] * self.size[1] - 1)
            pos = (i % self.size[0], i // self.size[0])
            if pos not in bad_pos and pos not in self.mine_pos:
                self.mine_pos.add(pos)
                self.numbers[pos] = -1
    
    def set_values(self):
        for pos in self.mine_pos:
            neighbours = self.get_neighbours(pos)
            for n_pos in neighbours:
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
            for i in self.get_neighbours(pos):
                if i not in self.revealed:
                    if self.numbers[i] == 0:
                        self.reveal(i)
                    else:
                        self.mine_values[i] = f' {self.numbers[i]}'
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
    
    def flag(self, pos: tuple[int, int]):
        valid: bool = len(self.flags) < self.n_mines
        valid = valid and -1 < pos[0] < self.size[0] and -1 < pos[1] < self.size[1]
        valid = valid and self.mine_values[pos] == self.chr_box
        if not valid: return 0
        self.mine_values[pos] = self.chr_flag
        self.flags.append(pos)
        
from random import randint
while True:
    size = (80, 80)
    x, y = randint(0, size[0] - 1), randint(0, size[1] - 1)
    m = Minesweeper((x, y), size, 10)
    print(m.mine_values)
    input()
    clear()