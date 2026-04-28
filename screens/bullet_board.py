from textual.screen import ModalScreen
from textual.widgets import    Label
from textual.containers import Container
from textual.app import ComposeResult
from textual.events import Key
import random
from assets.music_manager import play_sfx

class BulletBoard(ModalScreen): #csslater genrated by gemini
    CSS = """
    BulletBoard {
        align: center middle;
        background: 0%; 
    }
    #board-container {
        width: 42;
        height: 17;
        border: solid white;
        background: black;
        align: center middle;
    }
    #board-label {
        width: 100%;
        height: 100%;
        color: white;
    }
    """
    def __init__(self, duration= 5.0,spawn_rate= 0.3):
        super().__init__()
        self.width = 40
        self.height = 15
        
        self.player_x = self.width //2
        self.player_y = self.width //2
        self.invincibl = 0.0
        self.move_locked = False
        self.bullets = []
        self.time_left = duration
        self.hits_taken = 0
        self.loop_timer = None
        self.spawn_timer = None
        self.spawn_rate = spawn_rate
        
    def compose(self) -> ComposeResult:
        with Container (id="board-container"):
            yield Label ("", id='board-label')
    def on_mount(self): #physics run once every 0.05s
        self.loop_timer = self.set_interval (0.05, self.game_loop)
        self.spawn_timer =  self.set_interval (self.spawn_rate, self.spawn_bullet) #new bullet spawn
    def spawn_bullet(self): #(the pattern logic is purely by ai)
        # 🚨 THE PATTERN ENGINE
        # Pick a random attack style every time the timer ticks!
        pattern = random.choice(["scatter", "falling_wall", "shotgun_blast"])

        if pattern == "scatter":
            # Spawns 3 independent, totally random bullets
            for _ in range(3):
                speed = random.uniform(0.8, 1.8) 
                wall = random.choice(["top", "bottom", "left", "right"]) 
                
                if wall == "top":
                    bx, by = random.randint(1, self.width - 2), 0.0
                    dx, dy = random.uniform(-0.5, 0.5), speed
                elif wall == "bottom":
                    bx, by = random.randint(1, self.width - 2), float(self.height - 1)
                    dx, dy = random.uniform(-0.5, 0.5), -speed
                elif wall == "left":
                    bx, by = 0.0, random.randint(1, self.height - 2)
                    dx, dy = speed, random.uniform(-0.2, 0.2)
                else: # right
                    bx, by = float(self.width - 1), random.randint(1, self.height - 2)
                    dx, dy = -speed, random.uniform(-0.2, 0.2)

                self.bullets.append({"x": bx, "y": by, "dx": dx, "dy": dy})

        elif pattern == "falling_wall":
            # 🚨 NEW: Spawns a horizontal row of 5 bullets dropping together!
            start_x = random.randint(1, self.width - 6)
            speed = random.uniform(0.6, 1.0) # Walls move a bit slower
            
            for i in range(5):
                self.bullets.append({
                    "x": float(start_x + i), "y": 0.0,
                    "dx": 0.0, "dy": speed
                })

        elif pattern == "shotgun_blast":
            # 🚨 NEW: Spawns 3 bullets from the left wall spreading in a cone!
            start_y = float(random.randint(3, self.height - 4))
            speed = 1.5 # Shotguns are fast!
            
            self.bullets.append({"x": 0.0, "y": start_y, "dx": speed, "dy": -0.4}) # Angles Up
            self.bullets.append({"x": 0.0, "y": start_y, "dx": speed, "dy": 0.0})  # Shoots Straight
            self.bullets.append({"x": 0.0, "y": start_y, "dx": speed, "dy": 0.4})  # Angles Down
    def game_loop(self):
        self.time_left -= 0.05
        
        if self.invincibl > 0:
            self.invincibl -= 0.05
            
        #if time up
        if self.time_left <=0:
            self.end_game()
            return
        for b in self.bullets[:]:
            b["x"] += b["dx"]
            b["y"] += b["dy"]
            
            if b["y"] >= self.height or b["y"] < 0 or b["x"] >= self.width or b["x"] < 0:
                self.bullets.remove(b)
                continue
                
            if self.invincibl <= 0:
                if int(b["x"]) == self.player_x and int(b["y"]) == self.player_y:
                    self.hits_taken += 1
                    self.bullets.remove(b)
                    
                    self.invincibl = 1.5 
                    
                    play_sfx("hit") ###### too lazy to comment

        self.render_board()
        
    def render_board(self): #DEBUGGED WITH GEMINMI
        # 🚨 THE CLAMP (Keeps you in bounds)
        self.player_x = max(0, min(self.width - 1, self.player_x))
        self.player_y = max(0, min(self.height - 1, self.player_y))

        # Create an empty grid
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # 🚨 Draw Player (With Blinking I-Frames Logic!)
        if self.invincibl > 0:
            # Flashes on and off rapidly using math
            if int(self.invincibl * 10) % 2 == 0:
                grid[self.player_y][self.player_x] = "[dim white]♥[/dim white]"
        else:
            grid[self.player_y][self.player_x] = "[red]♥[/red]"

        # Draw Bullets
        for b in self.bullets:
            by, bx = int(b["y"]), int(b["x"])
            if 0 <= by < self.height and 0 <= bx < self.width:
                grid[by][bx] = "[white]*[/white]"

        # Render to screen
        display = "\n".join("".join(row) for row in grid)
        self.query_one("#board-label").update(display)
        
    def on_key (self, event: Key):
        if self.move_locked:
            return
        moved = False
        #move!
        if event.key == "up" and self.player_y > 0:
            self.player_y -= 1
        elif event.key == "down" and self.player_y < self.height - 1:
            self.player_y += 1
        elif event.key == "left" and self.player_x >0:
            self.player_x -= 1
        elif event.key == "right" and self.player_x < self.width -1:
            self.player_x += 1
        if moved:
            self.move_locked = True
            
            def unlock():
                self.move_locked = False
                
            self.set_timer(0.06, unlock)
    def end_game(self):
        self.loop_timer.stop()
        self.spawn_timer.stop()
        self.dismiss (self.hits_taken)