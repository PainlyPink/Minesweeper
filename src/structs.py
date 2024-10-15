from dataclasses import dataclass

from exceptions import ItemInListError


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

  def is_within(self, size: 'Size') -> bool:
    """Check if the point is within the given size boundaries."""
    return 0 <= self.x < size.cols and 0 <= self.y < size.rows

  def __add__(self, other: 'Point') -> 'Point':
    """Add two points together and return a new Point."""
    return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Size:
  """Represents the size of the minefield (rows, cols)."""
  rows: int
  cols: int

  @property
  def cells(self) -> int:
    """Return the total number of cells."""
    return self.rows * self.cols


@dataclass
class Visuals:
  """Stores visual symbols for different cell states."""
  hidden: str = "\033[96m■\033[0m"
  mine: str = "\033[91m⌀\033[0m"
  flag: str = "\033[93m⚑\033[0m"
  empty: str = "0"


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
    string = self.visual(Visuals())
    string += f"\nis_mine: {self.is_mine}, is_revealed: {self.is_revealed}"
    string += f"\nis_flagged: {self.is_flagged}, adjacent_mines: {self.adjacent_mines}"
    return string


class Buffer:
  """Manages the display buffer of the minefield."""

  def __init__(self, field: dict[Point, Cell], size: Size, visuals: Visuals) -> None:
    self.size = size
    self.visuals = visuals
    self.buffer = self._initialize_buffer(field)

  def _initialize_buffer(self, field: dict[Point, Cell]) -> list[list[str]]:
    """Initialize the buffer with current cell visuals."""
    return [
        [field[Point(x, y)].visual(self.visuals) for x in range(self.size.cols)]
        for y in range(self.size.rows)
    ]

  def update(self, field: dict[Point, Cell], modified_points: list[Point]) -> "Buffer":
    """Update only the modified cells in the buffer."""
    for point in modified_points:
      self.buffer[point.y][point.x] = field[point].visual(self.visuals)
    return self

  def display(self) -> "Buffer":
    """Display the current buffer."""
    for row in self.buffer:
      print(" ".join(row))
    return self

  def cell_at(self, point: Point) -> str:
    """Retrieve the visual of a cell at a specific point."""
    return self.buffer[point.y][point.x]
