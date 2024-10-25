from minefield import Minefield
from structs import Buffer, Visuals, Point, Size


class Game:
  def __init__(self, field_size: Size, mine_density: int):
    self.minefield = Minefield(field_size, mine_density)
    self.buffer = Buffer(self.minefield.field, field_size, Visuals())
    self.modified = self.minefield.get_modified()
    self.main()

  def clear_screen(self):
    """Clear the screen based on the operating system."""
    from os import system as os_system, name as os_name
    os_system("clear" if os_name == "posix" else "cls")

  def get_move(self, prompt: str = "Move: ") -> tuple[str, Point]:
    """Get player input and process the move."""
    move = input(prompt).strip().split()
    move_point = Point(*map(int, move[1:3]))
    move_type = move[0]
    return move_type, move_point

  def main(self):
    self.play_first_move()

    while not self.minefield.is_victory():
      self.clear_screen()
      self.buffer.show()
      self.play_move()

  def play_first_move(self):
    self.clear_screen()
    print(f"Size: {self.minefield.size}, Mines: {self.minefield.count.mines}")
    self.buffer.show()

    _, move = self.get_move()
    self.minefield.boom(move)
    self.buffer.visualize(self.modified())

  def play_move(self):
    move_type, move = self.get_move()

    if move_type == "f":
      self.flag(move)
    else:
      self.reveal(move)

  def flag(self, point: Point):
    self.minefield.flag(point)
    self.buffer.visualize([point])

  def reveal(self, point: Point):
    self.minefield.reveal(point)
    self.buffer.visualize(self.modified())


if __name__ == "__main__":
  Game(Size(55, 120), 10)
