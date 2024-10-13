import logging
from os import system as os_system, name as os_name
from functools import lru_cache
from random import sample
from exceptions import *

from structs import Size, Point, Cell, Buffer, Visuals


logging.basicConfig(level=logging.DEBUG)
FIELD_SIZE = Size(10, 10)


class Minefield:
  def __init__(self, size: Size, mine_count: int, boom_point: Point) -> None:
    self.size = size
    self.flagged_count = 0
    self.revealed: list[Point] = []
    self.mine_points: list[Point] = []
    self.total_safe_cells = self.size.cells - mine_count
    self.setup(mine_count, boom_point)

  def setup(self, mine_count: int, boom_point: Point) -> None:
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
    return get_neighbors(boom_point, self.size, include_self=True, extent=1)

  def _populate_field(self, mine_count: int, safe_zone: list[Point]) -> tuple[dict[Point, Cell], list[Point]]:
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
          self.mine_points.append(point)
          mine_neighbors.extend(get_neighbors(point, self.size))
        field[point] = Cell(is_mine)
        mine_index += 1

    return field, mine_neighbors

  def _count_adjacent_mines(self, field: dict[Point, Cell], mine_neighbors: list[Point]) -> None:
    """
    Count the number of mines around each cell and update their `adjacent_mines` attribute.
    """
    for point in mine_neighbors:
      if point in field:
        field[point].adjacent_mines += 1

  def reveal(self, point: Point) -> None:
    if point in self.revealed:
      raise CellAlreadyRevealedError

    if point in self.mine_points:
      raise MineHitError

    self.revealed.append(point)
    (cell := self.cell_at(point)).reveal()

    logging.debug(f"Revealed {point}: {cell.visual(Visuals())}")

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

  def is_victory(self) -> bool:
    return len(self.revealed) == self.total_safe_cells

  @lru_cache(maxsize=FIELD_SIZE.cells)
  def cell_at(self, point: Point) -> Cell:
    if point not in self.field:
      raise NotInFieldError
    return self.field[point]


@lru_cache(maxsize=FIELD_SIZE.cells)
def get_neighbors(point: Point, size: Size, include_self=False, extent: int = 1) -> list[Point]:
  """Generate and cache all neighboring coordinates for a given point in a grid."""

  neighbor_range = range(-extent, extent + 1)
  offsets = tuple(Point(x, y) for x in neighbor_range for y in neighbor_range if (x, y) != (0, 0))

  neighbors = [
      neighbor_point
      for offset in offsets
      if (neighbor_point := point + offset).is_within(size)
  ]

  if include_self:
    neighbors.append(point)
  return neighbors


Minefield(FIELD_SIZE, 10, Point(4, 4)).reveal(Point(0, 0))
