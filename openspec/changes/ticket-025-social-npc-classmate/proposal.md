# Ticket 025: Add Social NPC: Classmate

## Summary

Add a classmate NPC who introduces the Social skill.

## Notion Ticket

- Ticket: [Ticket 025 - Add Social NPC: Classmate](https://app.notion.com/p/36ec34b0c9018138bc5bf6b2f99b256a)
- Status at planning time: In progress
- Type: Feature
- Epic: NPCs & Social
- Dependencies:
- Ticket 005
- Ticket 008

## Acceptance Criteria

- [ ] A classmate NPC exists in an appropriate school area.
- [ ] The player can interact with the classmate using existing PC and mobile interaction paths.
- [ ] Dialogue introduces the Social skill in-world.
- [ ] The interaction can grant or unlock initial Social skill progression if the skill system supports it.
- [ ] Existing NPC, dialogue, room transition, and mobile control behavior continues to work.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add a classmate NPC using existing NPC sprite/style conventions and place them in a school area that already supports interaction prompts.
- Define classmate dialogue that introduces Social progression and points toward future social quests without requiring those future quests.
- If Social is not yet a skill constant, add it through the existing skill XP path with focused tests.
- Verify the E/action-button interaction path works on PC and mobile.

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