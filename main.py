from textual.app import App
from screens.intro_screen import IntroScreen
from textual import events

class UndertaleTUI(App): #our main app class
    
    CSS = """          # again asked gemini but this time it was very simple
    Screen {
        background: #000000;
    }
    """
    
    # Key Binding
    BINGINGS = [("q", "quit", "Quit Game")]
    
    def on_mount(self) -> None:
        self.push_screen(IntroScreen())
        
if __name__ == "__main__":
    app = UndertaleTUI()
    app.run()
    
def on_key(self, event: events.Key) -> None:
    if event.key == "escape":
        self.app.exit() # close on esc