# Ticket 040: Split Game Responsibilities Into Systems

## Summary

Reduce Game class responsibilities by extracting focused systems while preserving current behavior.

## Notion Ticket

- Ticket: [Ticket 040 - Split Game Responsibilities Into Systems](https://app.notion.com/p/396c34b0c90181369f46d2b92b422a34)
- Status at planning time: Not started
- Type: Chore
- Epic: Core Architecture
- Dependencies:
- Ticket 018
- Ticket 019
- Ticket 020
- Ticket 021
- Ticket 022
- Ticket 023
- Ticket 024
- Ticket 031
- Ticket 032
- Ticket 036

## Acceptance Criteria

- [ ] Game no longer directly owns every academic interaction and HUD drawing detail.
- [ ] Existing movement, rooms, NPC interaction, transport, academic actions, inventory, and mobile controls still work.
- [ ] Refactor is covered by existing tests plus targeted regression tests for moved logic.
- [ ] Pygbag/WASM async loop compatibility is preserved.
- [ ] No unrelated gameplay balance changes are bundled into this refactor.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Identify cohesive seams inside Game for AcademicSystem, HUDRenderer, RoomFactory or room definitions, InteractionSystem, and SaveSystem boundaries.
- Move behavior in small, testable steps while preserving public Game behavior and existing tests.
- Avoid gameplay balance changes; behavior changes belong in their own tickets.
- Run targeted regression tests for moved logic and full lint/test suite before PR.

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