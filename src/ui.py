# hello_textual_css.py

from textual.app import App, ComposeResult
from textual.widgets import Button, Label
from textual.containers import Horizontal


class HelloWorld(App):
  CSS_PATH = "css/ui.tcss"

  def compose(self) -> ComposeResult:
    yield Label("Hello Textual", id="hello")
    yield Horizontal(
        Button("Hi", id="hi", variant="success"),
        Button("Bye", id="close", variant="warning"),
    )
    print("%d" % id(self))

  def on_button_pressed(self, event: Button.Pressed) -> None:
    self.exit(event.button.id)


if __name__ == "__main__":
  app = HelloWorld()
  app.run()
