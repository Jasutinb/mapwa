# Ticket 037: Rebalance Grade Standing Rewards

## Summary

Make Grade Standing reward good student behavior instead of mostly acting as a punishment meter.

## Notion Ticket

- Ticket: [Ticket 037 - Rebalance Grade Standing Rewards](https://app.notion.com/p/396c34b0c90181689079c862bb954953)
- Status at planning time: Not started
- Type: Feature
- Epic: Academic Systems
- Dependencies:
- Ticket 021
- Ticket 022
- Ticket 023
- Ticket 024

## Acceptance Criteria

- [ ] Attending class on time can increase Grade Standing.
- [ ] Submitting assignments can increase Grade Standing.
- [ ] Early assignment submission can grant a small bonus if due-date timing is available.
- [ ] Failing exams and missing assignments still have meaningful consequences.
- [ ] Grade Standing changes are surfaced to the player through dialogue, notification, or planner feedback.
- [ ] Tests cover positive and negative Grade Standing changes.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Update Grade Standing balance constants for class attendance, assignment submission, early submission, exam pass, exam fail, and missed assignment outcomes.
- Hook positive Grade Standing changes into existing class and assignment success paths.
- Retain meaningful penalties for failed exams and missed assignments while avoiding double application.
- Surface Grade Standing changes through dialogue, notification, HUD, or planner feedback and cover positive/negative tests.

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