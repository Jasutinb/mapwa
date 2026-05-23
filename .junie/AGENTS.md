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

## 2. Testing Information

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
- `src/game.py`: Main game loop and state management.
- `src/player.py`: Player sprite logic.

### Code Style
- **Naming**: Uses `snake_case` for functions and variables, `PascalCase` for classes.
- **Constants**: Defined at the top of files (e.g., `SCREEN_WIDTH`, `TILE_SIZE`) in `UPPER_SNAKE_CASE`.
- **Sprite Groups**: The game uses `pygame.sprite.Group` for management and rendering.

### Import Management
Note that `src/game.py` manually adjusts `sys.path` to allow imports from its own directory. When adding new modules in `src/`, maintain consistency with this pattern or ensure absolute imports from the project root are used via `main.py`.
