# Ticket 027: Add Finance Skill

## Summary

Add Finance as a later-game skill focused on budgeting and money management.

## Notion Ticket

- Ticket: [Ticket 027 - Add Finance Skill](https://app.notion.com/p/36ec34b0c90181ba9ed4ca229c382cb5)
- Status at planning time: Not started
- Type: Feature
- Epic: Skills & Progression
- Dependencies:
- Ticket 002
- Ticket 017

## Acceptance Criteria

- [ ] Finance exists as a named skill in the skill progression model.
- [ ] At least one money-management activity can grant Finance XP.
- [ ] Finance progression is displayed wherever skill progress is normally shown.
- [ ] Money, cafeteria, and allowance systems keep their existing behavior.
- [ ] Tests cover Finance XP gain and persistence through normal state transitions.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add Finance as a first-class skill identifier using the existing skill XP manager.
- Choose one low-risk money-management activity as the initial Finance XP source, such as budgeting dialogue or a cafeteria/economy interaction.
- Render Finance wherever skill XP is already displayed.
- Keep allowance, money spending, and cafeteria behavior unchanged except for the explicit XP reward.

## Approval Status

Approved by the user on July 8, 2026. Implementation is scoped to adding Finance as a tracked skill and one low-risk Finance XP source without changing existing money behavior.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.
