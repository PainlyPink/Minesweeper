from os import system, name
from typing import Generator

import numpy as np


class Cell:
  """
  A cell in the minefield.

  Attributes:
    state (str): The state of the cell.
    is_mine (bool): Whether the cell contains a mine.
    is_revealed (bool): Whether the cell has been revealed.
    is_flagged (bool): Whether the cell has been flagged.
    adjacent_mines (int): The number of adjacent mines.
  """

  box = "?"
  mine = "\033[91mX\033[0m"
  flagged = "\033[93mF\033[0m"

  def __init__(self, is_mine: bool = False) -> None:
    self.state = Cell.box
    self.is_mine = is_mine
    self.is_revealed = False
    self.is_flagged = False
    self.adjacent_mines = 0

  def reveal(self) -> None | str:
    if self.is_revealed:
      return "Already Revealed"
    self.is_revealed = True
    if self.is_mine:
      self.state = Cell.mine
    else:
      self.state = "\033[96m" + str(self.adjacent_mines) + "\033[0m"
    return None

  def __str__(self) -> str:
    return self.state


Point = tuple[int, int]


class Field:
  """
  A minefield of a MineSweeper game.

  Attributes:
    rows (int): The number of rows in the minefield.
    cols (int): The number of columns in the minefield.
    mine_count (int): The number of mines in the minefield.
    grid (list[list[Cell]]): A 2D list of Cell objects.
    mines (list[Point]): A list of coordinates of all mines.
  """

  def __init__(self, size: tuple[int, int], mine_count: int) -> None:
    self.rows, self.cols = size
    self.mine_count = mine_count
    self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
    self.mines: list[tuple] = []
    self.setup()

  def setup(self) -> None:
    self.place_mines()
    self.calculate_adjacent_mines()

  def place_mines(self) -> None:
    positions = np.random.choice(self.rows * self.cols, self.mine_count, replace=False)

    # Place the mines
    for pos in positions:
      point = divmod(pos, self.cols)  # divmod(x, y) -> (x//y, x%y)
      self.cell_at(*point).is_mine = True
      self.mines.append(point)

  def calculate_adjacent_mines(self) -> None:
    # Calculate the number of adjacent mines for each cell
    for position in self.mines:
      for neighbor_position in get_neighbors(position, (self.rows, self.cols)):
        cell = self.cell_at(*neighbor_position)
        cell.adjacent_mines += 1

  def cell_at(self, row: int, col: int) -> Cell:
    return self.grid[row][col]

  def __str__(self) -> str:
    return "\n".join("  ".join(str(cell) for cell in row) for row in self.grid)


class Minefield:
  """
  A game of MineSweeper.

  Attributes:
    field (Field): The minefield.
    victory (bool): Whether the game has been won.
    flagged_count (int): The number of flagged cells.
  """

  def __init__(self, size: tuple[int, int], mine_count: int) -> None:
    self.field = Field(size, mine_count)
    self.victory = False
    self.flagged_count = 0
    self.revealed_count = 0
    self.modified_count = 0
    self.total_safe_cells = (size[0] * size[1]) - mine_count

  def reveal(self, point: Point) -> None:
    # TODO: better handle returns
    cell = self.field.cell_at(*point)

    # Reveal the cell, return if already revealed
    if cell.reveal():
      return

    # If it's a mine, game over
    if cell.is_mine:
      return

    self.modified_count += 1
    self.revealed_count += 1

    # Automatically reveal neighboring cells if no adjacent mines
    if cell.adjacent_mines == 0:
      self.reveal_neighbors(point)

    # Victory 🥳 ?
    if self.revealed_count == self.total_safe_cells:
      self.victory = True

  def reveal_neighbors(self, point: Point) -> None:
    # Reveal all non-mine neighbors
    for neighbour_position in get_neighbors(point, (self.field.rows, self.field.cols)):
      neighbour_cell = self.field.cell_at(*neighbour_position)
      if neighbour_cell.is_revealed or neighbour_cell.is_mine:
        continue
      self.reveal(neighbour_position)
      if neighbour_cell.adjacent_mines == 0:
        self.reveal_neighbors(neighbour_position)

  def display(self):
    print(self, self.modified_count, sep='\n')
    self.modified_count = 0

  def flag(self, point: Point) -> None:
    cell = self.field.cell_at(*point)

    if cell.is_revealed:
      return

    cell.is_flagged = not cell.is_flagged
    self.flagged_count += 1 if cell.is_flagged else -1
    cell.state = Cell.flagged if cell.is_flagged else Cell.box

  def __str__(self) -> str:
    return str(self.field)


# Memoize neighbor coordinates
neighbor_cache: dict[Point, Generator] = {}


def get_neighbors(point: Point, size: tuple[int, int]) -> Generator:
  """Generate all neighboring coordinates for a given point in a grid.

  Args:
    point: The point to generate neighbors for.
    size: The size of the grid.

  Yields:
    Generator: The coordinates of neighboring points.
  """
  if point not in neighbor_cache:
    rows, cols = size
    row, col = point

    extent = 1  # The extent of the neighborhood defaulted to only one cell around the point

    # Generate offsets and filter out invalid indices
    offsets = np.array(np.meshgrid(range(-extent, extent + 1), range(-extent, extent + 1))).T.reshape(-1, 2)
    offsets = offsets[(offsets != [0, 0]).any(axis=1)]  # Remove center point, it's not a neighbor

    # Generate neighbor coordinates
    neighbors = ((row + offset[0], col + offset[1])
                 for offset in offsets
                 if 0 <= row + offset[0] < rows
                 and 0 <= col + offset[1] < cols)

    # Cache the neighbor coordinates
    neighbor_cache[point] = neighbors

  yield from neighbor_cache[point]


def generate_move() -> tuple[int, int]:
  """Generate a random move within the Minefield dimensions."""
  row = np.random.randint(101)
  col = np.random.randint(101)
  return (row, col)


def main() -> None:
  mf = Minefield((101, 101), 1500)
  moves: set[tuple[int, int]] = set()

  while not mf.victory:
      # Generate a random move
    move = generate_move()

    # Check if the cell has already been revealed
    if mf.field.cell_at(*move).is_revealed:
      continue

    moves.add(move)
    mf.reveal(move)

    # Print the updated state of the minefield
    mf.display()
    input("Press Enter to continue...")
    system('cls' if name == 'nt' else 'clear')

  if mf.victory:
    print("YOU WIN!")
  else:
    print("Game Over! You hit a mine.")
  print(mf)


if __name__ == "__main__":
  main()
