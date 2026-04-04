# Undertale TUI
### A terminal-based RPG experience.

Built with the Textual framework, this project brings the iconic mechanics of Undertale—exploration, turn-based combat, and the Mercy system—directly to the command line.

---

## Key Features

* **Dynamic World Map:** Navigate the Ruins with real-time collision detection and ASCII-based rendering.
* **Active Combat Engine:**
    * **Timing Minigames:** High-stakes Fight and Defend mechanics based on rhythmic precision.
    * **ACT System:** Interact with monsters to find non-violent paths to victory.
    * **Item Management:** Use your inventory to heal mid-battle.
* **TUI Architecture:** Uses CSS-style styling, multi-layered screens, and custom widgets for a smooth terminal experience.
* **RNG Encounters:** Random monster encounters with a safe-step cooldown timer.
* **Audio Integration:** Dedicated music manager using Pygame to sync audio with map exploration and battle states.

---

## Controls

The game is optimized for a standard PC keyboard.

| Key | Action |
| :--- | :--- |
| **Arrow Keys** | Move Character / Navigate Menu Buttons |
| **Enter / Space** | Select Option / Confirm / Hit Timing Bar |
| **C** | Open Character Menu |
| **S** | Open Shop |
| **T** | Talk / Interact |
| **Esc** | Go back / Exit sub-menus |

---

## Installation and Launch

### Prerequisites
* **Python 3.10+**
* A modern terminal with 256-color support.
* **Textual:** The core framework required for the terminal user interface.
* **Pygame or Pygame-ce:** Required for audio and music playback.

### Quick Start
1. **Clone the Repository:**
    
        git clone https://github.com/adrish-biswas/undertale-tui.git
        cd undertale-tui

2. **Install Requirements:**
    
        pip install textual pygame-ce

3. **Launch the Game:**
    
        python main.py

---

## Project Structure

* **main.py**: The entry point of the application.
* **screens/**: Logic for the Map, Battle, Menu, and Victory screens.
* **assets/**: Monster data, player stats, and ASCII sprites.
* **widgets/**: Custom UI components like the DialogueBox.

---

## Disclaimer
This is a fan-made tribute. Undertale is a trademark of Toby Fox. This project is for educational and hobbyist purposes.

---

**Developed by Adrish Biswas**
*Stay Determined.*
