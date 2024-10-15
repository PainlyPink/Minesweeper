class MineHitError(RuntimeError):
  """Raised when a mine is hit."""


class CellAlreadyRevealedError(RuntimeError):
  """Raised when a player attempts to flag an already revealed cell."""


class NotInFieldError(RuntimeError):
  """Raised when a player attempts to reveal a cell at a point not in the field."""


class FlaggingRevealedCellError(CellAlreadyRevealedError):
  """Raised when a player attempts to flag a revealed cell."""


class ItemInListError(ValueError):
  """Raised when an item is already in the distinct list."""


class NoMoreFlagsError(RuntimeError):
  """Raised when a player attempts to flag a cell without any flags."""
