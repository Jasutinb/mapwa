# Ticket 016: Add Library Map Area

## Summary

Create a Library area connected to the School map where the player can train Academics, Math, or Discipline from separate study stations. The room should follow the existing Programming Lab and Electronics Lab pattern: clear entrance/exit pathing, keyboard and mobile action parity, focused tests, and one ticket PR.

## Acceptance Criteria

- [ ] The Library is registered as a room with a visible location name.
- [ ] The School map has a clear door/path to the Library, and the Library has a clear exit back to School.
- [ ] Entering or exiting the Library spawns the player on clear floor without colliding with walls, benches, stations, or other obstacles.
- [ ] The Library contains distinct interaction stations for Academics, Math, and Discipline.
- [ ] Pressing `E` near each station grants the matching skill XP and shows a confirmation dialogue.
- [ ] The mobile action button triggers the same station interactions as the keyboard action.
- [ ] Focused tests cover room links, clear door transitions, each station's XP reward, and mobile action parity.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 005
- Ticket 008

## Non-Goals

- No new quest is added for the Library in this ticket.
- No time-of-day, fatigue, borrowing, book inventory, or penalty system is added.
- No changes are made to existing Programming Lab, Electronics Lab, Admin Office, or gate behavior except where needed to avoid path blocking.

## Risks

- The ticket names Math and Discipline, but the current code only has Academics, Programming, and Electronics skill constants. This plan adds Math and Discipline as tracked skill IDs so the Library can fulfill the ticket literally.
- School already uses left, up, and right room links. The implementation should choose a Library entrance that does not break existing lab access and does not place the player into the school bench/desk or bus path.
- Adding three stations increases interaction overlap risk; station positions should be spaced so proximity hints and XP grants are deterministic.
