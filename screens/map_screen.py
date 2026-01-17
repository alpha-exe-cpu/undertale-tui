from textual.screen import Screen
from textual.widgets import Label, Static
from textual.app import ComposeResult
from textual.events import Key
from textual.containers import Container
import random

from screens.battle_screen import BattleScreen

class MapScreen(Screen):
    # css = gem iniiiiiiiiii
    CSS = """
    MapScreen {
        align: center middle;
        background: black;
    }
    #map-container {
        width: auto;
        height: auto;
        border: solid white;
        background: #000000;
        color: white;
        text-align: center;
    }
    """
    
    # WORLD_MAP BY GEMINI
    WORLD_MAP = [
        "########################################",
        "#......................................#",
        "#..##################################..#",
        "#..#................................#..#",
        "#..#..#######..###################..#..#",
        "#..#..#.....#..#.................#..#..#",
        "#..#..#.....#..#.................#..#..#",
        "#..#..#.....#..#.................#..#..#",
        "#..####.....####.................#..#..#",
        "#...................................#..#",
        "#..##################################..#",
        "#......................................#",
        "########################################"
    ]
    
    def __init__(self):
        super().__init__()
        self.player_x = 2
        self.player_y = 1
        self.step_taken = 0
        
    def compose(self) -> ComposeResult:
        with Container(id="map-container"):
            yield Label("", id="map-label")