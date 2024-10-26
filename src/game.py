from rich.text import Text

from minefield import Minefield
from structs import Buffer, Visuals, Point, Size

modified = dict[Point, Text]


class Game:

  def __init__(self, field_size: Size, mine_density: int):
    self.minefield = Minefield(field_size, mine_density)
    self.buffer = Buffer(self.minefield.field, Visuals())
    self.modified = self.minefield.get_modified()
    self.first_move = True

  def play_move(self, move_type: str, move: Point) -> modified:
    if self.first_move:
      return self.play_first_move(move)

    if move_type == "f":
      return self.flag(move)
    elif move_type == "r":
      return self.reveal(move)
    else:
      raise ValueError(f"Invalid move type: {move_type}")

  def play_first_move(self, move: Point) -> modified:
    self.minefield.boom(move)
    self.first_move = False
    return self.buffer.visualize(self.modified())

  def flag(self, point: Point) -> modified:
    self.minefield.flag(point)
    return self.buffer.visualize([point])

  def reveal(self, point: Point) -> modified:
    self.minefield.reveal(point)
    return self.buffer.visualize(self.modified())


if __name__ == "__main__":
  Game(Size(55, 120), 10)
