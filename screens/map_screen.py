from textual.screen import Screen
from textual.widgets import Label, Static
from textual.app import ComposeResult
from textual.events import Key
from textual.containers import Container
import random
import time
from screens.menu_screen import MenuScreen
from screens.shop_screen import ShopScreen
from assets.music_manager import play_music
from widgets.dialogue_box import DialogueBox
from assets.player_stats import player
from assets.maps_data import MAPS
import traceback

#btlscr import
from screens.battle_screen import BattleScreen

class MapScreen(Screen): #css = geminiiiiii
    CSS = """
    MapScreen {
        /* 🚨 CRITICAL: This tells the screen it has two levels */
        layers: base overlay;
        align: center middle;
        background: black;
    }

    #map-container {
        /* 🚨 CRITICAL: Puts the map on the bottom level */
        layer: base;
        
        /* Your styling */
        width: auto;
        height: auto;
        border: solid white;
        background: #000000;
        color: white;
        text-align: center;
    }
    """

    def __init__(self):
        super().__init__()
        # add dynamic maps
        self.current_map_id = player.get ("current_map", "ruins_start")
        self.map_data = MAPS[self.current_map_id]
        self.player_x = player.get("x", 2) 
        self.player_y = player.get("y", 1) #fix saving
        self.steps_taken = 0
        self.frozen = False #new
        self.safe_until = 0 # new 2
        self.facing = "down" #new 3 for signs

    def compose(self) -> ComposeResult:
        with Container(id="map-container"):
            yield Label("", id="map-label")

    def on_mount(self):
        self.render_map()
        self.query_one("#map-label").focus()
        play_music("ruins")
    def on_screen_resume(self):
        play_music("ruins")

    def render_map(self):
        # copy map to draw plyr
        display_map = []
        
        for y, row in enumerate(self.map_data["layout"]):
            if y == self.player_y:
                
                row_chars = list(row)
                row_chars[self.player_x] = "[cyan]@[/cyan]"
                display_map.append("".join(row_chars))
            else:
                display_map.append(row)
        
        #join rows with \n
        full_text = "\n".join(display_map)
        self.query_one("#map-label").update(full_text)

    def on_key(self, event: Key):
        if self.frozen:
            return
        if event.key == "c":
            self.app.push_screen(MenuScreen())
            return #added menuscreen 
        if event.key == "s":
            self.app.push_screen(ShopScreen())
            return #added shop
        if event.key == "t":
            if not self.query("DialogueBox"):
                box = DialogueBox("* Greetings, human.\n* I am a text box.")
                box.styles.layer = "overlay"
                self.mount(box)
        if self.query("DialogueBox"): 
            return
        
        if event.key  == "z" or event.key == "enter":
            look_x = self.player_x
            look_y = self.player_y
            
            if self.facing == "up":
                look_y -=1
            elif self.facing  == "down":
                look_y +=1
            elif self.facing  == "left":
                look_x -=1
            elif self.facing  == "right":
                look_x +=1
                
            #check if sign (or for entity in th future)+ help taken from gemini
            if 0 <= look_y < len(self.map_data["layout"]) and 0 <= look_x < len(self.map_data["layout"][0]):
                if self.map_data["layout"][look_y][look_x] == "S":
                    box = DialogueBox("* It's a sign.\n* it works!")
                    box.styles.layer = "overlay"
                    self.mount(box)
            return
        # calc pos
        target_x = self.player_x
        target_y = self.player_y

        if event.key == "up":
            target_y -= 1
            self.facing = "up"
        elif event.key == "down":
            target_y += 1
            self.facing ="down"
        elif event.key == "left":
            target_x -= 1
            self.facing = "left"
        elif event.key == "right":
            target_x += 1
            self.facing = "right"
        else:
            return

        # wall detection
        if 0 <= target_y < len(self.map_data["layout"]) and 0 <= target_x < len(self.map_data["layout"][0]):
            # check
            tile = self.map_data["layout"][target_y][target_x]
            if tile != "#" and  tile !="S":
                if tile == 'D': #door logic 9the big one)  
                    target_map, new_x, new_y = self.map_data["doors"][(target_x, target_y)]
                    self.current_map_id= target_map
                    self.map_data = MAPS[target_map]
                    self.player_x = new_x
                    self.player_y = new_y
                    player["current_map"] = target_map
                    player["x"] = new_x
                    player["y"] = new_y
                    self.render_map()
                    return
                    ###DEBUGGED WITH GEMINI
                elif tile == "B":
                    boss_id = self.map_data ["boss"][(target_x, target_y)]
                    self.frozen = True
                    self.query_one ("#map-container").border_title = f"[red]! BOSS: {boss_id.upper()} ![/red]"
                    self.query_one ("#map-label").focus()
                    
                    def start_boss_battle():
                        def on_return(result):
                            self.frozen = False
                            self.query_one("#map-container").border_title = ""
                            self.query_one("#map-label").focus()
                            self.render_map()
                        try:
                            # Try to launch the boss fight
                            self.app.push_screen(BattleScreen(boss_id=boss_id), on_return)
                        except Exception as e:
                            # 1. Change the border to tell you where to look
                            self.query_one("#map-container").border_title = "[red]CRASH! Check crash.log[/red]"
                            
                            # 2. Dump the FULL error into a text file!
                            with open("crash.log", "w") as f:
                                f.write(traceback.format_exc())
                    self.set_timer(1.5, start_boss_battle)
                    return
                                #allow movin
                self.player_x = target_x
                self.player_y = target_y
                player["x"] = target_x
                player["y"] = target_y
                self.steps_taken += 1
                self.check_encounter()
                self.render_map()
    def check_encounter(self):
        if time.time() < self.safe_until: # add safe for 2 min logic
            return
        #if monsterr!
        if random.random() < 0.05: 
            #freeze
            self.frozen = True
            
            #vusal
            self.query_one("#map-container").border_title = "[red]! ENCOUNTER ![/red]"
            
            def start_battle():
                def on_return(result):
                    self.frozen = False 
                    self.query_one("#map-container").border_title = "" 
                    self.query_one("#map-label").focus() 
                    wait_time = random.randint(60, 120)
                    self.safe_until = time.time() + wait_time # restart timer
                
                self.app.push_screen(BattleScreen(), on_return)

            self.set_timer(1.5, start_battle)