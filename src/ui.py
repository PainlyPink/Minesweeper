from time import monotonic
from rich.text import Text

from textual.screen import Screen
from pyfiglet import figlet_format
from textual.reactive import reactive
from textual.containers import Container
from textual.coordinate import Coordinate
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Label, Header, Button, Input, Footer, Static

import sql
from game import Game
from structs import Point, Size, Visuals
from exceptions import Victory, CellAlreadyRevealedError, MineHitError


def to_point(self) -> Point:
  return Point(self.column, self.row)


Coordinate.to_point = to_point
sqlcon: sql.sql = None


class TimeDisplay(Static):
  """A widget to display elapsed time."""

  start_time = reactive(monotonic)
  time = reactive(0.0)
  total = reactive(0.0)

  def on_mount(self) -> None:
    """Event handler called when widget is added to the app."""
    self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

  def update_time(self) -> None:
    """Method to update time to current."""
    self.time = self.total + (monotonic() - self.start_time)

  def watch_time(self, time: float) -> None:
    """Called when the time attribute changes."""
    self.update(Text(f"{time:005.2f}s", style="bold bright_black"))

  def start(self) -> None:
    """Method to start (or resume) time updating."""
    self.start_time = monotonic()
    self.update_timer.resume()

  def stop(self):
    """Method to stop the time display updating."""
    self.update_timer.pause()
    self.total += monotonic() - self.start_time
    self.time = self.total


class MineTable(Screen):

  BINDINGS = [("q", "quit", "Quit")]
  DEFAULT_CSS = """
    TimeDisplay {
      text-align: left;
    }
    DataTable {
      padding: 0;
    }
    Button {
      height: auto;
      width: auto;
    }"""

  def compose(self) -> ComposeResult:
    yield TimeDisplay()
    yield DataTable()
    yield Label("Loading...", id="chosen")
    yield Button("<-", variant="primary")
    yield Footer()

  def on_mount(self) -> None:
    global game
    game = Game(Size(9, 9), 10)

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
    self.query_one("#chosen", Label).update(Text(f"\n😺\n{event.coordinate}", style="italic bright_black"))

  def on_data_table_cell_selected(self, event: DataTable.CellSelected):
    self.update_table(event.coordinate)

  def update_table(self, coordinate: Coordinate) -> None:
    if game.first_move:
      self.query_one(TimeDisplay).start()

    try:
      modified = game.play_move("r", coordinate.to_point())
    except (CellAlreadyRevealedError, MineHitError):  # noqa: F405
      self.query_one(TimeDisplay).stop()
      return self.end_game()
    except Victory:  # noqa: F405
      self.query_one(TimeDisplay).stop()
      return self.end_game(True)

    for point, cell in modified.items():
      self.table.update_cell_at(point.to_coordinate(), cell)

  def end_game(self, victory: bool = False) -> None:
    self.table.cursor_type = "none"
    revealed = game.buffer.visualize_all(victory)
    label = self.query_one("#chosen", Label)

    for point, cell in revealed.items():
      self.table.update_cell_at(point.to_coordinate(), cell)

    status = "lose"
    if victory:
      label.update("\n😺🎉")
      status = "win"
    else:
      label.update("\n😿")

    if sqlcon:
      sqlcon.insert(status, self.query_one(TimeDisplay).time)
      label.update(Text(f"{label.renderable}\nSQL committed.", style="italic green"))
    else:
      label.update(Text(f"{label.renderable}\nCould not fetch sql user.", style="italic red"))

  def on_button_pressed(self) -> None:
    self.action_quit()

  def action_quit(self) -> None:
    self.app.pop_screen()


class SQLLogin(Screen):

  BINDINGS = [("q", "quit", "Quit")]

  DEFAULT_CSS = """
    * {
      text-align: left;
    }
  """

  def compose(self) -> ComposeResult:
    if not sql.LOGGED_IN:
      yield from self.login_page()
    else:
      yield from self.statistics_page()
    yield Footer()

  def login_page(self):
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

  def on_button_pressed(self) -> None:
    status = self.query_one("#status", Label)

    inputs = self.query(Input)
    credentials = [input.value for input in inputs]

    try:
      global sqlcon
      sqlcon = sql.sql(*credentials)
    except Exception as e:
      status.update(Text(f"failed\n{e}", style="italic red"))
    else:
      status.update(Text("success", style="italic green"))
      sql.LOGGED_IN = True

    self.recompose()

  def statistics_page(self):
    yield Label(Text("STATISTICS", style="bold", justify="center"))
    yield DataTable()

  def on_mount(self):
    if not sql.LOGGED_IN:
      return

    self.query_one(Label).update("Game Stats")
    self.table = self.query_one(DataTable)

    if sqlcon:
      rows = iter(sqlcon.pull())
      self.table.add_columns(*next(rows))
      self.table.add_rows(rows)
    else:
      self.table.add_columns("match_id", "win_or_lose", "time")
      self.table.add_rows(
          (
              (1, "win", 12.34),
              (2, "lose", 23.68),
              (3, "win", 54.23),
              (4, "lose", 146.23),
          )
      )

  def action_quit(self) -> None:
    self.app.pop_screen()


class ModalApp(App[None]):

  DEFAULT_CSS = """
    .center {
      text-align: center;
    }
  """

  def compose(self) -> ComposeResult:
    self.title = "Py-Quantum Minesweeper"
    yield Header(show_clock=True, classes="center")
    yield Static(Text(figlet_format("*Mine Quanto*"), style="bold red", justify="full"))
    yield Container(
        Button("Play", variant="success", id="play"),
        Button("SQL", variant="primary", id="sql"),
        Button("Quit", variant="warning", id="quit"),
        classes="center",
    )

  def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "play":
      self.push_screen(MineTable())
    elif event.button.id == "sql":
      self.push_screen(SQLLogin())
    elif event.button.id == "quit":
      self.exit()


if __name__ == "__main__":
  app = ModalApp()
  app.run()
