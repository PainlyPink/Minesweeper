from random import choice

from rich.text import Text

from textual.coordinate import Coordinate
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label

from game import Game
from structs import Point, Size, Visuals


def to_point(self) -> Point:
  return Point(self.column, self.row)


Coordinate.to_point = to_point


class MineTable(App[None]):

  def compose(self) -> ComposeResult:
    yield DataTable()
    yield Label("Nothing chosen", id="chosen")

  def on_mount(self) -> None:
    self.table = self.query_one(DataTable)
    self.fill_table()

  def fill_table(self):
    size = game.minefield.size

    for column in range(size.cols):
      self.table.add_column(Text(f"{column:02}", justify="center"))

    cell = Text(Visuals.hidden, justify="center")
    for row in range(size.rows):
      self.table.add_row(*(cell,) * size.cols, label=f"{row:02}")

  def on_data_table_cell_highlighted(self, event: DataTable.CellHighlighted):
    self.query_one("#chosen", Label).update(str(event.coordinate))

  def on_data_table_cell_selected(self, event: DataTable.CellSelected):
    self.update_table(event.coordinate)

  def update_table(self, coordinate: Coordinate) -> None:
    modified = game.play_move("r", coordinate.to_point())
    center = lambda text: Text(text, justify="center")  # noqa: E731

    for point, cell in modified.items():
      self.table.update_cell_at(point.to_coordinate(), center(cell))


if __name__ == "__main__":
  game = Game(Size(20, 20), 10)
  app = MineTable()
  app.run()
