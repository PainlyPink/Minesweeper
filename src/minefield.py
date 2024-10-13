from os import system as os_system, name as os_name
from functools import lru_cache
from random import sample
from exceptions import *

from structs import Size, Point, Cell, Buffer, Visuals


class Minefield:
  def __init__(self, size: Size, mine_count: int, boom_point: Point) -> None:
    self.size = size
    self.flagged_count = 0
    self.revealed: set[Point] = set()
    self.mine_points: set[Point] = set()
    self.total_safe_cells = self.size.cells - mine_count
    self.setup(mine_count, boom_point)

  def setup(self, mine_count: int, boom_point: Point) -> None:
    self.field: dict[Point, Cell] = self.generate_field(mine_count, boom_point)
    self.reveal(boom_point)

  def generate_field(self, mine_count: int, boom_point: Point) -> dict[Point, Cell]:
    # Initial click safe zone region
    safe_zone = get_neighbors(boom_point, self.size, include_self=True, extent=1)

    # Total number of cells
    total_cells = self.size.cells

    # Number of unsafe cells (not in the safe zone)
    unsafe_region = total_cells - len(safe_zone)

    # Generate random mines for the unsafe region
    mine_or_not = sample([True] * mine_count + [False] * (unsafe_region - mine_count), k=unsafe_region)

    field = {}
    mine_index = 0  # Keep track of the current index in `mine_or_not`
    mine_neighbors: list[Point] = []

    # Populate the field
    for position in range(total_cells):
      point = Point(*divmod(position, self.size.rows))

      # If the point is in the safe zone, it's guaranteed to not be a mine
      if point in safe_zone:
        field[point] = Cell(is_mine=False)
      else:
        # Use the next value from `mine_or_not` for non-safe zone points
        is_mine = mine_or_not[mine_index]

        # If the point is a mine, add its neighbors to `mine_neighbors`
        if is_mine:
          self.mine_points.add(point)
          mine_neighbors.extend(get_neighbors(point, self.size))

        field[point] = Cell(is_mine)
        mine_index += 1

    # Count the number of mines around each cell (optimized)
    for point in mine_neighbors:
      field[point].adjacent_mines += 1

    return field

  def reveal(self, point: Point) -> None:
    if point in self.revealed:
      raise CellAlreadyRevealedError

    if point in self.mine_points:
      raise MineHitError

    self.revealed.add(point)
    (cell := self.cell_at(point)).reveal()

    # Automatically reveal neighboring cells if no adjacent mines
    if cell.adjacent_mines == 0:
      self.reveal_neighbors(point)

  def reveal_neighbors(self, point: Point) -> None:
    """
    Iteratively reveal all neighboring cells around a given point.
    """
    for neighbor in get_neighbors(point, self.size):
      if neighbor in self.revealed or neighbor in self.mine_points:
        continue

      self.reveal(neighbor)

  def flag(self, point: Point) -> None:
    if point in self.revealed:
      raise FlaggingRevealedCellError

    (cell := self.cell_at(point)).flag()
    self.flagged_count += 1 if cell.is_flagged else -1

  def cell_at(self, point: Point) -> Cell:
    if point not in self.field:
      raise NotInFieldError
    return self.field[point]


@lru_cache(maxsize=None)
def get_neighbors(point: Point, size: Size, include_self=False, extent: int = 1) -> set[Point]:
  """Generate and cache all neighboring coordinates for a given point in a grid."""

  neighbor_range = range(-extent, extent + 1)
  offsets = tuple(Point(x, y) for x in neighbor_range for y in neighbor_range if (x, y) != (0, 0))

  neighbors = set(
      neighbor_point
      for offset in offsets
      if (neighbor_point := point + offset).is_within(size)
  )

  if include_self:
    neighbors.add(point)
  return neighbors


os_system('cls' if os_name == 'nt' else 'clear')
FIELD_SIZE = 10
mf = Minefield(Size(*(FIELD_SIZE,) * 2), 2 * FIELD_SIZE, Point(*sample(range(FIELD_SIZE), k=2)))
buffer = Buffer(mf.field, mf.size, Visuals())
buffer.display()
