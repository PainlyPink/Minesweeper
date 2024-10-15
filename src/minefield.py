from os import system as os_system, name as os_name
from functools import lru_cache
from collections import deque
from random import sample

from structs import Buffer, Size, Point, Cell, DistinctList, Visuals
from exceptions import *  # pylint: disable=unused-wildcard-import


FIELD_SIZE = Size(80, 80)
DIFFICULTY = 9


def validate_point(func):
  def wrapper(self, point: Point) -> Point:
    if point in self.revealed:
      raise CellAlreadyRevealedError
    if point in self.mine_points:
      raise MineHitError

    return func(self, point)
  return wrapper


class Minefield:
  def __init__(self, size: Size, mine_count: int, boom_point: Point) -> None:
    self.size = size
    self.flagged_count = 0

    self.revealed = DistinctList()
    self.mine_points: set[Point] = set()

    self.total_safe_cells = self.size.cells - mine_count

    self.field: dict[Point, Cell] = self.generate_field(mine_count, boom_point)
    self.reveal(boom_point)

  def generate_field(self, mine_count: int, boom_point: Point) -> dict[Point, Cell]:
    """Generate the minefield as a dictionary of points and cells."""
    # Step 1: Define safe zone
    safe_zone = self._calculate_safe_zone(boom_point)

    # Step 2: Create the minefield structure
    field, mine_neighbors = self._populate_field(mine_count, safe_zone)

    # Step 3: Count adjacent mines and update cells
    self._count_adjacent_mines(field, mine_neighbors)

    return field

  def _calculate_safe_zone(self, boom_point: Point) -> list[Point]:
    """Calculate the initial safe zone around the first click point."""
    extent = max(1, FIELD_SIZE.cells >> DIFFICULTY)  # x >> n == x // 2ⁿ
    safe_zone = get_neighbors(boom_point, self.size, include_self=True, extent=extent)

    return safe_zone

  def _populate_field(self, mine_count: int, safe_zone: list[Point]) -> tuple[dict[Point, Cell], list]:
    """
    Populate the minefield with mines and non-mine cells.
    Returns:
        - A dictionary representing the field (Point -> Cell)
        - A list of neighboring points to all mines, used for mine counting.
    """
    total_cells = self.size.cells
    unsafe_region = total_cells - len(safe_zone)

    # Generate random True/False values for mine placement
    mine_or_not = sample([True] * mine_count + [False] * (unsafe_region - mine_count), k=unsafe_region)

    field = {}
    mine_neighbors: list[Point] = []
    mine_index = 0

    # Populate the field with mines and non-mines
    for position in range(total_cells):
      point = Point(*divmod(position, self.size.rows))

      # If point is in the safe zone, it's not a mine
      if point in safe_zone:
        field[point] = Cell(is_mine=False)
      else:
        # Assign a mine or non-mine based on the precomputed random list
        is_mine = mine_or_not[mine_index]
        if is_mine:
          self.mine_points.add(point)
          mine_neighbors.extend(get_neighbors(point, self.size))

        # Add the cell to the field
        field[point] = Cell(is_mine)
        mine_index += 1

    return field, mine_neighbors

  def _count_adjacent_mines(self, field: dict[Point, Cell], mine_neighbors: list) -> None:
    """
    Count the number of mines around each cell and update their `adjacent_mines` attribute.
    """
    for point in mine_neighbors:
      if point in field:
        field[point].adjacent_mines += 1

  @validate_point
  def reveal(self, point: Point) -> None:
    (cell := self.cell_at(point)).reveal()
    self.revealed.append(point)

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

      for neighbor in get_neighbors(point, self.size, exclude=(*self.revealed, *self.mine_points)):
        print(neighbor)
        cell = self.cell_at(neighbor)

        cell.reveal()
        self.revealed.append(neighbor)

        if cell.adjacent_mines == 0:
          queue.append(neighbor)

  def flag(self, point: Point) -> None:
    if point in self.revealed:
      raise FlaggingRevealedCellError

    (cell := self.cell_at(point)).flag()
    self.flagged_count += 1 if cell.is_flagged else -1
    if not cell.is_mine:
      return

    if cell.is_flagged:
      self.revealed.append(point)
    else:
      self.revealed.remove(point)

  def is_victory(self) -> bool:
    return len(self.revealed) == self.total_safe_cells

  @lru_cache(maxsize=FIELD_SIZE.cells)
  def cell_at(self, point: Point) -> Cell:
    if point not in self.field:
      raise NotInFieldError
    return self.field[point]


@lru_cache(maxsize=FIELD_SIZE.cells)
def get_neighbors(
    point: Point, size: Size, exclude: tuple = tuple(), include_self=False, extent: int = 1
) -> list[Point]:
  """Generate and cache all neighboring coordinates for a given point in a grid."""

  neighbor_range = range(-extent, extent + 1)
  offsets = tuple(Point(x, y) for x in neighbor_range for y in neighbor_range if (x, y) != (0, 0))

  neighbors = [
      neighbor_point
      for offset in offsets
      if (neighbor_point := point + offset).is_within(size)
      and neighbor_point not in exclude
  ]

  if include_self:
    neighbors.append(point)
  return neighbors


def main():
  def move(prompt: str = "Move: ") -> tuple:
    inp = input(prompt).strip().split()
    p = Point(*map(int, inp[1:3]))
    t = inp[0]
    return t, p

  mf = Minefield(FIELD_SIZE, 2000, move("Start: ")[1])
  bf = Buffer(mf.field, FIELD_SIZE, Visuals()).display()

  while not mf.is_victory():
    t, p = move()
    os_system("clear" if os_name == "posix" else "cls")

    if t == "f":
      mf.flag(p)
      modified = [p]
    else:
      i = len(mf.revealed)
      mf.reveal(p)
      modified = mf.revealed[i:]

    bf.update(mf.field, modified).display()


if __name__ == "__main__":
  main()
