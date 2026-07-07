# Ticket 034: Add Basic Test Coverage for Core Managers

## Summary

Add unit tests for core systems once they exist.

## Notion Ticket

- Ticket: [Ticket 034 - Add Basic Test Coverage for Core Managers](https://app.notion.com/p/36ec34b0c90181c698a8d29137479940)
- Status at planning time: Not started
- Type: Chore
- Epic: Developer Experience
- Dependencies:
- Ticket 001
- Ticket 002
- Ticket 005
- Ticket 009

## Acceptance Criteria

- [ ] Core manager behavior has focused unit tests once the managers exist.
- [ ] Tests use dummy SDL drivers where pygame initialization is required.
- [ ] Tests remain deterministic and avoid opening a visible game window.
- [ ] The suite documents important state, movement, collision, and manager contracts.
- [ ] Full pytest and ruff commands pass before PR.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Inventory manager/state tests cover add/remove/use/check behavior that is not already covered by gameplay tests.
- Skill XP, quest, room/state, and other extracted manager tests are added as those managers exist in the current codebase.
- Tests use dummy SDL drivers before pygame initialization and remain deterministic in headless CI.
- Keep this ticket focused on coverage; do not refactor managers unless a small testability seam is required and approved.

## Approval Status

This OpenSpec proposal captures the current ticket plan before coding. Confirm the implementation plan with the user before creating the ticket branch and changing game code.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.