# Ticket 031: Simplify HUD Around Urgent Player State

## Summary

Refocus the always-visible HUD on urgent information only: Energy, Stress, current objective, and money.

## Notion Ticket

- Ticket: [Ticket 031 - Simplify HUD Around Urgent Player State](https://app.notion.com/p/36ec34b0c9018198b168f0d0a3cab854)
- Status at planning time: Not started
- Type: Feature
- Epic: UI/UX
- Dependencies:
- Ticket 018
- Ticket 019
- Ticket 024

## Acceptance Criteria

- [ ] The default HUD shows Energy, Stress, current objective, and money in a compact layout.
- [ ] Schedule, assignments, exams, and Grade Standing are not permanently rendered in the default play view.
- [ ] Location text, dialogue, inventory, and mobile controls do not overlap the urgent HUD.
- [ ] Desktop and mobile input paths remain usable after the layout change.
- [ ] Focused tests cover HUD state selection where practical.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Identify the current always-visible HUD elements in Game drawing code.
- Keep Energy, Stress, current objective, and money visible in a compact arrangement.
- Move or hide schedule, assignment, exam, and Grade Standing details from the default play view in coordination with the Student Planner ticket.
- Measure or test HUD rectangles so mobile controls, inventory, dialogue, and location text remain readable.

## Approval Status

Approved by the user on July 7, 2026. Implementation is scoped to the simplified default HUD described above.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.
