from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Container
from textual import on
from assets.player_stats import player

class MenuScreen(Screen): #css by gemini
    
    BINDINGS = [
        ("up", "app.focus_previous", "Move Up"),
        ("down", "app.focus_next", "Move Down"),
        ("escape", "dismiss", "Close Menu")
    ]
    
    CSS = """
    MenuScreen {
        /* 2. Move to Top Right Corner */
        align: right top;
        background: 0%; /* Transparent background behind the box */
    }
    #menu-container {
        width: 30; /* Make it narrower */
        height: auto;
        border: solid white;
        background: black;
        margin: 2 4; /* Add some spacing from the edges */
        padding: 1 1;
        layout: vertical;
    }
    #stats-label {
        color: white;
        text-style: bold;
        border-bottom: solid white;
        margin-bottom: 1;
        text-align: center;
    }
    Label {
        color: #aaaaaa;
        margin-top: 1;
    }
    .item-btn {
        width: 100%;
        margin: 0;
        background: black;
        color: white;
        border: none; 
        text-align: left;
    }
    /* Highlight the selected button */
    .item-btn:focus, .item-btn:hover {
        background: white;
        color: black;
        text-style: bold;
    }
    #btn-close {
        margin-top: 2;
        background: #333333;
        color: white;
        border: none;
        width: 100%;
        text-align: center;
    }
    #btn-close:focus {
        background: red;
        color: white;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="menu-container"):
            stats_text = f"{player['name']}\nLV {player['lv']}\nHP {player['hp']}/{player['max_hp']}\nG {player['gold']}"
            yield Label(stats_text, id="stats-label")
            
            yield Label("-- ITEMS --")
            for item in player["inventory"]:
                yield Button(item, classes="item-btn")
            yield Label("", id="feedback") #for after eating or using
            yield Button("Close Menu", id="btn-close")
        
    @on(Button.Pressed)
    def handle_buttons(self, event: Button.Pressed):
        if event.button.id == "btn-close":
            self.dismiss()
        
        elif "item-btn" in event.button.classes:
            item_name = str(event.button.label)
            
            # calc healingh!
            old_hp = player["hp"]
            player["hp"] = min(player["hp"] + 10, player["max_hp"])
            recovered = player["hp"] - old_hp
            
            # remove the item from inv
            if item_name in player["inventory"]:
                player["inventory"].remove(item_name)
            
            # disable btns, not glitch eating bro
            event.button.disabled = True
            #update visuals
            self.query_one("#feedback").update(f"You ate {item_name}.\nRecovered {recovered} HP!")
            new_stats = f"{player['name']}\nLV {player['lv']}\nHP {player['hp']}/{player['max_hp']}\nG {player['gold']}"
            self.query_one("#stats-label").update(new_stats)
            
            def refresh_menu():
                self.dismiss()
                self.app.push_screen(MenuScreen())
            
            self.set_timer(1.5, refresh_menu)