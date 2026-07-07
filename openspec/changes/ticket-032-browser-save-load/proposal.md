# Ticket 032: Add Browser Save and Load From GameState

## Summary

Serialize and restore GameState so player progress survives browser refreshes and future system growth.

## Notion Ticket

- Ticket: [Ticket 032 - Add Browser Save and Load From GameState](https://app.notion.com/p/36ec34b0c901815799a3dc25fa008b52)
- Status at planning time: Not started
- Type: Feature
- Epic: Core Systems
- Dependencies:
- Ticket 001
- Ticket 002
- Ticket 004
- Ticket 005
- Ticket 009
- Ticket 018
- Ticket 019
- Ticket 020
- Ticket 022
- Ticket 023
- Ticket 024

## Acceptance Criteria

- [ ] Player can save and load progress in desktop development runs.
- [ ] Player progress can survive a browser refresh in the web build where browser storage is available.
- [ ] Loading restores the same room and the major GameState fields.
- [ ] Corrupt, missing, or older saves do not crash the game.
- [ ] Automated tests cover serialization, missing saves, and at least one round-trip restore.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Introduce a SaveSystem boundary that serializes GameState to a versioned dictionary or JSON payload.
- Add desktop local-file persistence and browser-compatible persistence where pygbag storage APIs are available.
- Restore the same room and important player state, including money, Energy, Stress, Grade Standing, quests, assignments, exams, and inventory.
- Handle missing, corrupt, or older saves gracefully with tests.

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