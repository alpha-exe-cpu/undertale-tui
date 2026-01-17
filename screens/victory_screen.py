from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Container
from textual import on

class VictoryScreen(ModalScreen):
    CSS = """
    VictoryScreen {
        align: center middle;
        background: 0%; 
    }
    #victory-box {
        width: 50;
        height: 12;
        border: double yellow;
        background: black;
        align: center middle;
        text-align: center;
    }
    Label {
        margin: 1 0;
        color: white;
    }
    Button {
        margin-top: 2;
        background: #ff9900;
        color: black;
    }
    """

    def __init__(self, exp_gained: int, gold_gained: int):
        super().__init__()
        self.exp = exp_gained
        self.gold = gold_gained

    def compose(self) -> ComposeResult:
        with Container(id="victory-box"):
            yield Label("VICTORY!", id="title")
            yield Label(f"* You won {self.exp} EXP and {self.gold} Gold.")
            yield Button("Continue", id="btn-continue")

    @on(Button.Pressed)
    def handle_continue(self, event: Button.Pressed):
        self.dismiss(True)