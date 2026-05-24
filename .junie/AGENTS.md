# Development Guide for mapwa

This document provides project-specific information for developers working on the **mapwa** Student RPG.

## 1. Build and Configuration

The project uses `pygame-ce` (Pygame Community Edition) and is configured with `uv`.

### Environment Setup
- **Python Version**: Python 3.14 or higher is required.
- **Dependencies**: The primary dependency is `pygame-ce`.
- **Installation**:
  ```bash
  py -3 -m pip install pygame-ce
  ```
  (Or use `uv` if available: `uv sync`)

### Running the Game
To start the game, run the `main.py` script:
```bash
py -3 main.py
```

### Hot Refresh (Development)
To run the game with hot refresh (automatic restart on code changes), use:
```bash
py -3 watch.py
```
This requires `watchdog`, which is included in the project dependencies.

## 2. Build and Deployment

### Web Deployment (pygbag)
The project is configured for web deployment using `pygbag`. 

#### Build for Web:
To package the game for the web (HTML5/WebAssembly):
```bash
uv run python -m pygbag --build --archive --disable-sound-format-error main.py
```
The output will be in the `build/web` directory. The `--archive` flag creates a compressed version suitable for upload to platforms like **Itch.io**. The `--disable-sound-format-error` flag is used to bypass errors related to unsupported audio formats (like .wav files) in some environments.

#### Local Web Preview:
To run a local web server to preview the game:
```bash
uv run python -m pygbag main.py
```
Then open your browser at `http://localhost:8000`. If you see a gray screen, try a hard refresh (**Ctrl + F5**) or try a different port: `uv run python -m pygbag --port 8001 main.py`.

## 3. Testing Information

### Headless Testing
Since this is a Pygame project, running tests in a CI or headless environment requires setting dummy video and audio drivers to avoid "No available video device" errors.

```python
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
```

### Running Tests
Tests are implemented using `pytest`. You can run all tests in the `tests/` directory:
```bash
py -3 -m pytest
```

### Adding New Tests
When adding tests for sprites or game logic:
1. Use `pytest` fixtures for setup and teardown.
2. Ensure `SDL_VIDEODRIVER` is set to `dummy` if the test doesn't require a window.
3. Add tests for movement, collision, and state changes in the `tests/` directory.

### Reference Test Example
The following pattern is verified to work for testing the `Player` movement:

```python
import os
import pytest

# Set dummy drivers BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from src.player import Player

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_player_movement():
    player = Player((0, 0), [])
    player.direction.x = 1 # Simulate right move
    player.move(player.speed)
    assert player.rect.x == player.speed
```

## 3. Additional Development Information

### Project Structure
- `main.py`: Entry point.
- `watch.py`: Watcher script for hot refresh.
- `src/game.py`: Main game loop and state management.
- `src/player.py`: Player sprite logic.

### Code Style
- **Clean Code**: Practice clean code by writing readable, maintainable, and well-structured code.
- **DRY Principle**: Practice the "Do Not Repeat Yourself" principle by avoiding code duplication through functions, classes, and modules.
- **Naming**: Uses `snake_case` for functions and variables, `PascalCase` for classes.
- **Constants**: Defined at the top of files (e.g., `SCREEN_WIDTH`, `TILE_SIZE`) in `UPPER_SNAKE_CASE`.
- **Sprite Groups**: The game uses `pygame.sprite.Group` for management and rendering.

### WebAssembly Compatibility (pygbag)
When developing features, keep these WASM-specific constraints in mind:
- **Async Loop**: The main game loop must be `async` and include `await asyncio.sleep(0)` to prevent the browser from hanging.
- **Font Loading**: Browsers often lack default system fonts. Always use a fallback pattern:
  ```python
  try:
      self.font = pygame.font.SysFont('Arial', 24)
  except:
      self.font = pygame.font.Font(None, 24)
  ```
- **Deterministic Logic**: Avoid heavy use of `random` or dynamic imports inside the `update` loop, as it can cause performance hitches in WASM.
- **Asset Paths**: Use forward slashes (`/`) for all file paths to ensure compatibility with the virtual file system.

### Import Management
Note that `src/game.py` manually adjusts `sys.path` to allow imports from its own directory. When adding new modules in `src/`, maintain consistency with this pattern or ensure absolute imports from the project root are used via `main.py`.

## 4. Feature List
- **Basic Movement**: Player can move in four directions using arrow keys or WASD.
- **Rooms**: Multiple rooms (Living Room, Bedroom, Outside, School).
- **NPCs**: Interaction with Mom (provides allowance and wanders around the house).
- **Bus System**: Ride the bus between Outside and School (₱20 fee to school, free home).
- **Location Display**: Temporary display of location names upon entering a new room.
- **Inventory System**: Functional inventory system that allows picking up and displaying items.
- **Money System**: Tracking and displaying player money with a custom icon.
- **Study Feature**: Gain 10 XP by interacting with the desk in the School room. Includes a 1-second studying animation.
- **School Door**: Exit the school room via a door to return to the Outside area.
