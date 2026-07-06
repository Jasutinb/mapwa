# Ticket 021: Add Attend Class Interaction

## Summary

Allow the player to attend scheduled classes using the weekly schedule foundation from Ticket 020. The interaction should let the player attend classes scheduled for the current day, grant skill XP for the class, prevent duplicate attendance rewards, and preserve the existing study/practice interactions.

## Acceptance Criteria

- [ ] The player can attend a scheduled class for the current day when they are in the matching room/location.
- [ ] Class attendance uses the schedule entries from Ticket 020 rather than duplicating class data.
- [ ] Each scheduled class can be attended at most once per in-game day.
- [ ] Attending a class grants configured skill XP for that class's schedule skill/category.
- [ ] Attending a class shows clear dialogue including the course name, XP gained, and whether the class has already been attended.
- [ ] The game tracks attended class identifiers per day and clears/rotates that tracking when the player sleeps into the next day.
- [ ] The interaction does not replace or break existing School study, Programming practice, Electronics practice, or Library study station actions.
- [ ] If the player tries to attend in a room with no scheduled class today, a clear no-class dialogue is shown.
- [ ] If the player tries to attend a class that was already attended today, XP is not granted again and a clear already-attended dialogue is shown.
- [ ] Keyboard and mobile action paths have the same attend-class behavior through the existing `E`/mobile action mapping.
- [ ] Focused tests cover successful attendance, duplicate blocking, wrong-room/no-class blocking, day reset, XP by skill, and mobile parity.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 020

## Non-Goals

- No time-of-day clock, lateness, absence penalties, grades, stress changes, or energy costs in this ticket unless explicitly approved before implementation.
- No assignments, exams, boss fights, or deadline mechanics.
- No schedule editing UI.
- No broad redesign of existing study/practice station interactions.

## Open Questions / Proposed Decisions

- Proposed interaction placement: add a distinct class attendance spot or marker per existing scheduled room, separate from current study/practice stations, so `E` near study/practice still does what it already does.
- Proposed attendance identifier: derive a stable class id from weekday, start label, course name, and room key.
- Proposed XP amount: use a new configured class attendance XP value, applied to the class entry's `skill`.
- Proposed day behavior: attendance state is keyed by `current_day`; sleeping naturally moves the player to a new day with no classes attended yet.
- Proposed no-class handling: only show the no-class dialogue when the player uses the class attendance spot in that room, not for unrelated interactions.

## Risks

- Reusing existing study/practice stations would create ambiguous `E` behavior and could break first-day or Hello World quest flows.
- The schedule has labels but no simulated clock, so attendance should mean "attend one of today's scheduled classes in this room," not "attend at the exact current time."
- Attendance tracking should remain small and deterministic so future grade, assignment, and exam systems can build on it.
