from random import sample
from typing import Callable
from collections import deque
from os import system as os_system, name as os_name

from structs import Buffer, Size, Point, Cell, DistinctList, Visuals, Holder
from exceptions import MineHitError, CellAlreadyFlaggedError, CellAlreadyRevealedError, NotInFieldError


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
    self.count = Holder(mines=mine_count, safe=safe_count, flagged=0)

    self.cells = Holder(revealed=DistinctList(), mines=set(), flagged=set())

    self.field = self.set_field()
    self.neighbors = self.set_neighbors()

  def set_field(self) -> dict[Point, Cell]:
    points = ((x, y) for x in range(self.size.cols) for y in range(self.size.rows))
    return {Point(*point): Cell() for point in points}

  def set_neighbors(self) -> dict[Point, list[Point]]:
    return {point: self.calculate_neighbors(point) for point in self.field}

  @validate_point(check_bounds=True)
  def boom(self, point: Point) -> None:
    extent = max(1, self.size.cells >> self.count.safe)
    safe_zone = self.calculate_neighbors(point, extent=extent)
    mine_points = self.generate_mine_points(set(safe_zone) | {point})

    self.set_mines(mine_points)
    self.reveal(point)

  def generate_mine_points(self, safe_zone: set[Point]) -> list[Point]:
    field = set(self.field)

    return sample(tuple(field.difference(safe_zone)), k=self.count.mines)

  def set_mines(self, mine_points: list[Point]) -> None:
    for mine_point in mine_points:
      self.cell_at(mine_point).is_mine = True
      self.cells.mines.add(mine_point)
      self.increment_mine_neighbors(mine_point)

  def increment_mine_neighbors(self, point: Point) -> None:
    for neighbor in self.neighbors_of(point):
      self.cell_at(neighbor).adjacent_mines += 1

  @validate_point(check_bounds=True, check_revealed=True, check_mines=True)
  def reveal(self, point: Point) -> None:
    revealed = self.cells.revealed
    mines_and_flagged = self.cells.mines | self.cells.flagged
    queue = deque([point])

    while queue:
      point = queue.popleft()
      if point in revealed or point in mines_and_flagged:
        continue

      (cell := self.cell_at(point)).reveal()
      revealed.append(point)

      if cell.adjacent_mines == 0:
        queue.extend(self.neighbors_of(point))

  @validate_point(check_bounds=True, check_revealed=True)
  def flag(self, point: Point) -> None:
    (cell := self.cell_at(point)).flag()

    if cell.is_flagged:
      self.cells.flagged.add(point)
      self.count.flagged += 1
    else:
      self.cells.flagged.discard(point)
      self.count.flagged -= 1

  def get_modified(self) -> Callable:
    modified_count = len(self.cells.revealed)

    def _() -> list[Point]:
      nonlocal modified_count
      previous = modified_count
      modified_count = len(self.cells.revealed)

      return self.cells.revealed[previous:]

    return _

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

    in_bound = lambda point: point.is_within(self.size)  # noqa: E731
    neighbors = filter(in_bound, (point + offset for offset in offsets))

    return neighbors


def main():
  def move(prompt: str = "Move: ") -> tuple[str, Point]:
    inp = input(prompt).strip().split()
    p = Point(*map(int, inp[1:3]))
    t = inp[0]
    return t, p

  FIELD_SIZE = Size(10, 10)
  mf = Minefield(FIELD_SIZE, 10)
  bf = Buffer(mf.field, FIELD_SIZE, Visuals())

  bf.show()
  p = move()[1]
  os_system("clear" if os_name == "posix" else "cls")

  modified = mf.get_modified()
  mf.boom(p)
  bf.visualize(modified()).show()

  while not mf.is_victory():
    t, p = move()
    os_system("clear" if os_name == "posix" else "cls")

    if t == "f":
      mf.flag(p)
      bf.visualize([p])
    else:
      mf.reveal(p)
      bf.visualize(modified())

    bf.show()


if __name__ == "__main__":
  main()
