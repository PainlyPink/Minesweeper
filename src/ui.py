from random import random

from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label
from textual.coordinate import Coordinate


class UpdatingTableExampleApp(App[None]):

  def compose(self) -> ComposeResult:
    yield DataTable()
    yield Label("Nothing chosen", id="chosen")

  def on_mount(self) -> None:
    table = self.query_one(DataTable)

    columns = 20
    rows = 20
    for column in range(columns):
      table.add_column(f"col{column}")
    value = Text("--", justify="center")
    for n in range(rows):
      table.add_row(*(value,) * columns, label=str(n))

  def on_data_table_cell_selected(self, event: DataTable.CellSelected):
    self.query_one("#chosen", Label).update(str(event.coordinate))
    self.update_table(event.coordinate)

  def update_table(self, coordinate: Coordinate) -> None:
    table = self.query_one(DataTable)
    table.update_cell_at(coordinate, random())


if __name__ == "__main__":
  UpdatingTableExampleApp().run()
