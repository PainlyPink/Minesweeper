from os import system as os_system, name as os_name
from collections import deque
from random import sample

from structs import Buffer, Size, Point, Cell, DistinctList, Visuals, Count, CellTypes
from exceptions import *


FIELD_SIZE = Size(10, 13)
DIFFICULTY = 9
EXTENT = max(1, FIELD_SIZE.cells >> DIFFICULTY)  # x >> n == x // 2ⁿ


def validate_point(check_bounds=True, check_revealed=False, check_mines=False, check_flagged=False):
  def decorator(func):
    def wrapper(self, point: Point, *args, **kwargs) -> Point:

      if check_bounds and not point.is_within(self.size):
        raise NotInFieldError
      if check_revealed and point in self.cells.revealed:
        raise CellAlreadyRevealedError
      if check_mines and point in self.cells.mines:
        raise MineHitError
      if check_flagged and point in self.cells.flagged:
        raise CellAlreadyFlaggedError

      return func(self, point, *args, **kwargs)
    return wrapper
  return decorator


class Minefield:

  def __init__(self, size: Size, mine_density: int) -> None:
    self.size = size

    mine_count = self.size.cells * mine_density // 100
    safe_count = self.size.cells - mine_count
    self.count = Count(
        mines=mine_count,
        safe=safe_count,
        flagged=0
    )

    self.cells = CellTypes(
        revealed=DistinctList(),
        mines=DistinctList(),
        flagged=DistinctList()
    )

    self.field = self.set_field()
    self.neighbors = self.set_neighbors()

  def set_field(self) -> dict[Point, Cell]:
    points = ((x, y) for x in range(self.size.cols) for y in range(self.size.rows))
    return {Point(*point): Cell() for point in points}

  def set_neighbors(self) -> dict[Point, list[Point]]:
    return {point: self.calculate_neighbors(point) for point in self.field}

  @validate_point(check_bounds=True)
  def boom(self, point: Point) -> None:
    safe_zone = self.calculate_neighbors(point, extent=EXTENT)
    mine_points = self.generate_mine_points(set(safe_zone) | {point})

    self.set_mines(mine_points)
    self.reveal(point)

  def generate_mine_points(self, safe_zone: set[Point]) -> list[Point]:
    field = set(self.field)

    return sample(tuple(field.difference(safe_zone)), k=self.count.mines)

  def set_mines(self, mine_points: list[Point]) -> None:
    for mine_point in mine_points:
      self.cell_at(mine_point).is_mine = True
      self.cells.mines.append(mine_point)
      self.increment_mine_neighbors(mine_point)

  def increment_mine_neighbors(self, point: Point) -> None:
    for neighbor in self.neighbors_of(point):
      self.cell_at(neighbor).adjacent_mines += 1

  @validate_point(check_bounds=True, check_revealed=True, check_mines=True)
  def reveal(self, point: Point) -> None:
    (cell := self.cell_at(point)).reveal()
    self.cells.revealed.append(point)

    # Automatically reveal neighboring cells if no adjacent mines
    if cell.adjacent_mines == 0:
      self.reveal_neighbors(point)

  def reveal_neighbors(self, start_point: Point) -> None:
    """
    Iteratively reveal all neighboring cells around a given point using a breadth-first approach.
    This avoids hitting the recursion limit by using a queue for the iterative reveal process.
    """
    queue = deque([start_point])

    while queue:
      point = queue.popleft()

      safe_to_reveal = lambda point: (cell := self.cell_at(point)).is_revealed == cell.is_mine == False
      neighbors = filter(safe_to_reveal, self.neighbors_of(point))  # yields the result

      for neighbor in neighbors:
        cell = self.cell_at(neighbor)

        cell.reveal()
        self.cells.revealed.append(neighbor)

        if cell.adjacent_mines == 0:
          queue.append(neighbor)

  @validate_point(check_bounds=True, check_revealed=True)
  def flag(self, point: Point) -> None:
    (cell := self.cell_at(point)).flag()
    self.count.flagged += 1 if cell.is_flagged else -1

    if not cell.is_mine:
      return

    # Flagged a mine, commit greatness

  def is_victory(self) -> bool:
    return len(self.cells.revealed) == self.count.safe

  @validate_point(check_bounds=True)
  def cell_at(self, point: Point) -> Cell:
    return self.field[point]

  @validate_point(check_bounds=True)
  def neighbors_of(self, point: Point) -> list[Point]:
    return self.neighbors[point]

  def calculate_neighbors(self, point: Point, extent: int = 1):
    """
    Calculate the neighbors of a given point using the Moore neighborhood.
    """

    neighbor_range = range(-extent, extent + 1)
    offsets = (Point(x, y) for x in neighbor_range for y in neighbor_range if (x, y) != (0, 0))

    in_bound = lambda point: point.is_within(self.size)
    neighbors = filter(in_bound, (point + offset for offset in offsets))

    return neighbors


def main():
  def move(prompt: str = "Move: ") -> tuple[str, Point]:
    inp = input(prompt).strip().split()
    p = Point(*map(int, inp[1:3]))
    t = inp[0]
    return t, p

  mf = Minefield(FIELD_SIZE, 10)
  print(mf.count.mines)
  bf = Buffer(mf.field, FIELD_SIZE, Visuals()).display()
  p = move()[1]
  os_system("clear" if os_name == "posix" else "cls")
  mf.boom(p)
  bf.update(mf.field, mf.cells.revealed).display()

  while not mf.is_victory():
    t, p = move()
    os_system("clear" if os_name == "posix" else "cls")

    if t == "f":
      mf.flag(p)
      modified = [p]
    else:
      i = len(mf.cells.revealed)
      mf.reveal(p)
      modified = mf.cells.revealed[i:]

    bf.update(mf.field, modified).display()


if __name__ == "__main__":
  main()
