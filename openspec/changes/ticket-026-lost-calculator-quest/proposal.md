# Ticket 026: Add Quest: Lost Calculator

## Summary

Create a small side quest about helping a classmate find a lost calculator.

## Notion Ticket

- Ticket: [Ticket 026 - Add Quest: Lost Calculator](https://app.notion.com/p/36ec34b0c901814f8f66f94248fc105f)
- Status at planning time: Not started
- Type: Content
- Epic: Quests
- Dependencies:
- Ticket 009
- Ticket 012
- Ticket 025

## Acceptance Criteria

- [ ] A classmate can start the Lost Calculator quest.
- [ ] The calculator appears in an appropriate location while the quest is active.
- [ ] The player can pick up and return the calculator.
- [ ] Quest state prevents duplicate rewards or repeated completion.
- [ ] PC and mobile interaction paths can complete the quest.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add Lost Calculator quest definitions using the existing quest-state foundation.
- Use the classmate NPC as quest giver and completion target.
- Spawn or reveal the calculator item only while the quest is active, then allow pickup through the inventory/item path.
- Prevent duplicate completion rewards by recording quest completion state.
- Test start, pickup, return, and mobile interaction flow.

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