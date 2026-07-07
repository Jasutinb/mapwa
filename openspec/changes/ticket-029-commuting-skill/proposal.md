# Ticket 029: Add Commuting Skill

## Summary

Add Commuting as a skill trained by repeated travel.

## Notion Ticket

- Ticket: [Ticket 029 - Add Commuting Skill](https://app.notion.com/p/36ec34b0c901813c9445dfae8ceb2763)
- Status at planning time: Not started
- Type: Feature
- Epic: Skills & Progression
- Dependencies:
- Ticket 003
- Ticket 005

## Acceptance Criteria

- [ ] Commuting exists as a named skill in the skill progression model.
- [ ] Using supported travel routes can grant Commuting XP.
- [ ] Travel validation and fares continue to work.
- [ ] Skill XP is not granted when travel fails.
- [ ] Tests cover successful travel XP and failed-travel no-op behavior.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add Commuting as a skill identifier using the existing skill XP manager.
- Award Commuting XP only after valid successful travel, starting with the bus route.
- Ensure insufficient-funds or invalid-travel attempts do not grant XP.
- Add tests around successful bus travel and failed travel no-op behavior.

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