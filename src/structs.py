from dataclasses import dataclass
from textual.coordinate import Coordinate

from exceptions import ItemInListError


@dataclass
class Visuals:
  """Stores visual symbols for different cell states."""

  hidden: str = "📦"
  mine: str = "🎆"
  flag: str = "🚩"
  empty: str = "⬛"


class DistinctList(list):

  def append(self, item):
    if item in self:
      raise ItemInListError(f"Item `{item}` already exists in list.")
    super().append(item)


@dataclass(frozen=True)
class Point:
  """Represents a point (x, y) in the grid."""

  x: int
  y: int

  def is_within(self, size: "Size") -> bool:
    """Check if the point is within the given size boundaries."""
    return 0 <= self.x < size.cols and 0 <= self.y < size.rows

  def __add__(self, other: "Point") -> "Point":
    """Add two points together and return a new Point."""
    return Point(self.x + other.x, self.y + other.y)

  def __lt__(self, other):
    if self.y == other.y:
      return self.x < other.x
    return self.y < other.y

  def to_coordinate(self) -> Coordinate:
    """Convert the point to a coordinate."""
    return Coordinate(self.y, self.x)


@dataclass(frozen=True)
class Size:
  """Represents the size of the minefield (rows, cols)."""

  rows: int
  cols: int

  @property
  def cells(self) -> int:
    """Return the total number of cells."""
    return self.rows * self.cols


class Cell:
  """Represents a cell in the minefield."""

  def __init__(self, is_mine: bool = False) -> None:
    self.is_mine = is_mine
    self.is_revealed = False
    self.is_flagged = False
    self.adjacent_mines = 0

  def flag(self) -> None:
    """Toggle the flagged state of the cell."""
    if not self.is_revealed:  # Can't flag a revealed cell
      self.is_flagged = not self.is_flagged
    else:
      self.is_flagged = False

  def reveal(self) -> "Cell":
    """Reveal the cell."""
    self.is_revealed = True
    return self

  def visual(self, visuals: Visuals) -> str:
    """Return a visual representation of the cell."""
    if not self.is_revealed:
      return visuals.flag if self.is_flagged else visuals.hidden
    if self.is_mine:
      return visuals.mine
    return str(self.adjacent_mines) if self.adjacent_mines > 0 else visuals.empty

  def __str__(self):
    string = f"is_revealed: {self.is_revealed}, adjacent_mines: {
        self.adjacent_mines}, is_mine: {self.is_mine}, is_flagged: {self.is_flagged}"
    return string


class Buffer:
  """Manages the display buffer of the minefield."""

  def __init__(self, field: dict[Point, Cell], visuals: Visuals) -> None:
    self.field = field
    self.visuals = visuals

  def visualize(self, field_points) -> dict[Point, str]:
    """Update the display buffer with the given field."""
    display = {}
    for point in field_points:
      display[point] = self.cell_at(point).visual(self.visuals)
    return display

  def cell_at(self, point: Point) -> Cell:
    """Return the cell at the given point."""
    return self.field[point]


@dataclass
class Holder:

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __repr__(self):
    return self.__dict__.__repr__()
