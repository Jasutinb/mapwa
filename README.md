# Mapwa

Mapwa is a student-life RPG built with Python and `pygame-ce`. You balance a school day around classes, assignments, exams, quests, money, energy, stress, skills, and grade standing while moving between home and the Mapúa Intramuros campus.

The project runs as a desktop game during development and is packaged for the browser with pygbag.

## Gameplay loop

1. Prepare at home, collect important items, and talk with family.
2. Commute to Intramuros and enter campus.
3. Attend classes, study, practice skills, complete assignments, and take exams.
4. Manage money, energy, stress, inventory, quests, and grade standing.
5. Return home, sleep to advance the day, and continue from a local save.

Current locations include the living room, bedroom, outside, Intramuros, school entrance, admin office, school, programming lab, electronics lab, library, and cafeteria.

## Controls

| Action | Desktop | Mobile |
| --- | --- | --- |
| Move | Arrow keys or `WASD` | Direction pad |
| Interact / confirm | `E` | Action button |
| Use inventory slots | `1`–`5` | Tap an inventory slot |
| Open / close menu | `Esc` | Menu button |
| Open / close Student Planner | `P` | Planner button |
| Navigate menu choices | Arrow keys or `WASD` | Direction pad |

The pause menu includes Save Game and Load Game. Desktop runs store progress in `mapwa-save.json`; browser builds use local storage when it is available.

## Setup

Mapwa requires Python 3.14 or newer and uses [uv](https://docs.astral.sh/uv/) for dependency management.

```powershell
uv sync --dev
```

## Run locally

Start the desktop game:

```powershell
uv run python main.py
```

Start it with automatic restart when Python files change:

```powershell
uv run python watch.py
```

The watcher enables the development loadout. Tests are excluded from its restart trigger.

## Quality checks

Run the same lint and test commands used by CI:

```powershell
uv run pytest -n auto
uv run ruff check .
```

On Windows, the repository helper runs both commands with dummy SDL drivers:

```powershell
./run-checks.ps1
```

## Browser build

Preview the pygbag build locally at `http://localhost:8000`:

```powershell
uv run python -m pygbag --disable-sound-format-error main.py
```

Create the deployable `build/web.zip` archive on Windows:

```powershell
./run-build.ps1
```

The CI/CD workflow runs lint and tests, builds the web archive, and deploys successful `master` pushes to itch.io.

## Roadmap

### Implemented

- Multi-room home, commute, Intramuros, and campus exploration.
- Keyboard and mobile control parity for movement, interaction, inventory, and menus.
- Inventory, money, transport fares, food purchases, and save/load persistence.
- Day progression, class attendance, assignments, exams, energy, stress, and grade standing.
- Programming, electronics, finance, commuting, health, and social skill progression.
- First-day, Hello World, lost-calculator, and classmate activity quest flows.
- Headless automated tests, pygbag packaging, and continuous deployment.

### Planned next

- Student planner menu for schedule, assignment, exam, and quest details.
- Grade-standing rewards and clearer standing labels and consequences.
- Exam-readiness warnings and a stronger first-day onboarding flow.
- Smaller game-system modules to reduce the responsibilities in `Game`.

Roadmap delivery is tracked in Notion and implemented through ticket-specific OpenSpec changes. Planned items can change as tickets are refined and approved.

## Project structure

- `main.py` — asynchronous game entry point.
- `src/` — gameplay, state, UI, map, persistence, and manager modules.
- `tests/` — deterministic pytest coverage configured for headless pygame.
- `openspec/changes/` — active ticket proposals, task lists, and behavioral specs.
- `openspec/changes/archive/` — completed ticket changes after merge and Notion closure.
- `.github/workflows/ci-cd.yml` — Windows CI, web build, and deployment pipeline.

## Contribution workflow

Ticket work follows:

`Notion ticket → OpenSpec proposal/tasks/spec → approval → branch/worktree → implementation → tests → PR → verification comment → CI/CD → merge → Notion update → OpenSpec archive`

See [AGENTS.md](AGENTS.md) for the authoritative development, testing, control-parity, WebAssembly, visual-style, and ticket-workflow rules.
