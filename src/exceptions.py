class MineHitError(Exception):
  """Raised when a mine is hit."""


class CellAlreadyRevealedError(Exception):
  """Raised when a player attempts to flag an already revealed cell."""


class NotInFieldError(Exception):
  """Raised when a player attempts to reveal a cell at a point not in the field."""


class FlaggingRevealedCellError(CellAlreadyRevealedError):
  """Raised when a player attempts to flag a revealed cell."""
