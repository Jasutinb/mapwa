# Ticket 025: Add Social NPC Classmate

## Summary

Add a classmate NPC who introduces the Social skill through a simple school interaction. The first version should be deterministic, style-consistent with existing NPCs, and available through the same keyboard and mobile action path used by other interactable NPCs.

## Notion Ticket

- Ticket: [Ticket 025 - Add Social NPC: Classmate](https://app.notion.com/p/36ec34b0c9018138bc5bf6b2f99b256a)
- Status at planning time: In progress
- Type: Feature
- Epic: NPCs & Social
- Priority: P1
- Dependencies:
- Ticket 005
- Ticket 008

## Acceptance Criteria

- [ ] A classmate NPC appears in an existing school area without blocking core paths, doors, class markers, assignment markers, exam markers, or study/practice stations.
- [ ] The classmate uses the existing NPC visual style, starting from the player/Mom-style sprite references with classmate-specific personalization.
- [ ] Interacting with the classmate introduces the Social skill through clear dialogue.
- [ ] The first classmate interaction grants one-time Social XP when the skill system supports it.
- [ ] Repeated classmate interactions show repeat dialogue and do not grant Social XP again.
- [ ] PC `E` interaction and mobile action button interaction both trigger the same classmate behavior.
- [ ] Existing Mom, guard, attendant, food vendor, bus, study, class attendance, assignment, exam, sleep, inventory, map transition, and quest behavior remains unchanged.
- [ ] Focused tests cover classmate placement, PC interaction, mobile interaction parity, one-time Social XP, repeat dialogue, and pathing/non-blocking behavior.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add Social skill constants in `src/config.py`, including `SKILL_SOCIAL`, classmate intro XP, first-time dialogue, repeat dialogue, and action hint text.
- Add a `has_talked_to_classmate` flag to `GameState` so the Social XP reward happens once.
- Add a dedicated `classmate_sprites` group and helper methods on `Game`:
  - create the classmate NPC on the School map
  - find a nearby classmate
  - interact with the classmate
- Place the classmate in the School room near open floor, away from doors and existing markers.
- Add the classmate to the existing `E` interaction chain and rely on the existing mobile action-to-`E` mapping for mobile parity.
- Draw a proximity hint when near the classmate.
- Use the existing player/Mom sprite style with classmate-specific personalization.

## Approval Status

Approved by the user on July 7, 2026. Implementation is scoped to the Social NPC classmate behavior described above.

## Non-Goals

- No relationship meter, friendship levels, party system, romance, or multi-step social quest.
- No new room or map area.
- No new player control beyond the existing interaction action.
- No changes to Ticket 026 Lost Calculator quest beyond leaving the classmate ready for that future dependency.

## Risks

- The School room already contains several interactables, so interaction priority and placement must avoid accidental shadowing.
- Adding another NPC sprite group must be cleared on room rebuild to avoid stale sprites.
- The one-time Social XP flag must survive room changes and sleeping.
