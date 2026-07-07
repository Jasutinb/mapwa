# Ticket 041: Add Grade Standing Labels and Consequences

## Summary

Make Grade Standing emotionally readable with labels and tie it to rewards, consequences, and dialogue.

## Notion Ticket

- Ticket: [Ticket 041 - Add Grade Standing Labels and Consequences](https://app.notion.com/p/396c34b0c9018116be44cbb41e329462)
- Status at planning time: Not started
- Type: Feature
- Epic: Academic Systems
- Dependencies:
- Ticket 024
- Ticket 036
- Ticket 037

## Acceptance Criteria

- [ ] Grade Standing displays both number and label where appropriate.
- [ ] Labels update correctly as Grade Standing changes.
- [ ] At least one meaningful reward or consequence is connected to Grade Standing.
- [ ] Content is clear without turning the HUD into a dashboard.
- [ ] Tests cover label thresholds and any new gate or reward logic.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add a Grade Standing label helper with thresholds for Excellent, Good, Stable, At Risk, and Probation.
- Display number plus label wherever Grade Standing is shown, especially the planner once available.
- Implement one lightweight consequence or reward tied to a standing band, such as dialogue, feedback, or eligibility.
- Test threshold boundaries and the chosen reward/consequence gate.

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