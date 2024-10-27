from rich.text import Text

from textual.screen import Screen
from textual.coordinate import Coordinate
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label, Header, Button, Input, Footer

from game import Game
from structs import Point, Size, Visuals


def to_point(self) -> Point:
  return Point(self.column, self.row)


Coordinate.to_point = to_point


class MineTable(Screen):

  BINDINGS = [("q", "quit", "Quit")]

  def compose(self) -> ComposeResult:
    yield DataTable()
    yield Label("Loading...", id="chosen")
    yield Footer()

  def on_mount(self) -> None:
    self.table = self.query_one(DataTable)
    self.fill_table()

  def fill_table(self):
    size = game.minefield.size

    for column in range(size.cols):
      self.table.add_column(Text(f"{column:02}", justify="center"))

    cell = Visuals.hidden
    for row in range(size.rows):
      self.table.add_row(*(cell,) * size.cols, label=f"{row:02}")

  def on_data_table_cell_highlighted(self, event: DataTable.CellHighlighted):
    self.query_one("#chosen", Label).update(str(event.coordinate))

  def on_data_table_cell_selected(self, event: DataTable.CellSelected):
    self.update_table(event.coordinate)

  def update_table(self, coordinate: Coordinate) -> None:
    modified = game.play_move("r", coordinate.to_point())

    for point, cell in modified.items():
      self.table.update_cell_at(point.to_coordinate(), cell)

  def action_quit(self) -> None:
    self.app.pop_screen()


class SQLLogin(Screen):

  BINDINGS = [("q", "quit", "Quit")]

  def compose(self) -> ComposeResult:
    yield Label(Text("SQL LOGIN", style="bold", justify="center"))

    yield Label(Text("Host Name (Required)", style="bold"))
    yield Input(placeholder="host")

    yield Label(Text("User Name (Required)", style="bold"))
    yield Input(placeholder="user")

    yield Label(Text("Password (Required)", style="bold"))
    yield Input(placeholder="password", password=True)

    yield Label(Text("Database Name", style="bold"))
    yield Input(placeholder="database")

    yield Button("Login", variant="success", id="login")
    yield Label(Text("status", style="italic"), id="status")

    yield Footer()

  def on_button_pressed(self, event: Button.Pressed) -> None:
    credentials = self.query(Input)
    representation = ""
    for i in credentials:
      representation += i.value
    self.query_one("#status", Label).update(representation)

  def action_quit(self) -> None:
    self.app.pop_screen()


class ModalApp(App[None]):

  def compose(self) -> ComposeResult:
    yield Header()
    yield Button("Play", variant="success", id="play")
    yield Button("SQL login", variant="primary", id="sql")
    yield Button("Quit", variant="warning", id="quit")

  def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "play":
      self.push_screen(MineTable())
    elif event.button.id == "sql":
      self.push_screen(SQLLogin())
    elif event.button.id == "quit":
      self.exit()


if __name__ == "__main__":
  game = Game(Size(20, 20), 10)
  app = ModalApp()
  app.run()
