# Ticket 036: Add Student Planner Menu

## Summary

Create a phone/menu-style Student Planner that contains schedule, assignments, exams, Grade Standing, and objectives.

## Notion Ticket

- Ticket: [Ticket 036 - Add Student Planner Menu](https://app.notion.com/p/396c34b0c90181919dfdd4edbb0bc843)
- Status at planning time: Not started
- Type: Feature
- Epic: UI/UX
- Dependencies:
- Ticket 020
- Ticket 022
- Ticket 023
- Ticket 024
- Ticket 031

## Acceptance Criteria

- [ ] Player can open and close the Student Planner on desktop.
- [ ] Player can open and close the Student Planner on mobile controls.
- [ ] Planner displays schedule, assignments, exams, Grade Standing, and current objective when those systems have data.
- [ ] Planner handles empty states clearly without debug-looking text.
- [ ] Default HUD no longer needs to permanently render planner-owned details.
- [ ] Tests cover the PC and mobile control paths for opening the planner.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add an open/close Planner state or overlay reachable from desktop controls and a matching mobile control.
- Render schedule, assignments, exams, Grade Standing, and current objective in the planner with empty states.
- Ensure the default HUD can stay simplified once planner-owned details move there.
- Test desktop and mobile open/close paths plus planner content selection.

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