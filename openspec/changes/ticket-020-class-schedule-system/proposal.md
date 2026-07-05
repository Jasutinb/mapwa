# Ticket 020: Add Class Schedule System

## Summary

Create a simple weekly class schedule system that builds on the existing `current_day` and sleep loop. The game does not yet have a time-of-day clock or class attendance interaction, so this ticket should add schedule data, weekday derivation, current-day lookup helpers, and a lightweight in-game readout that future class attendance, assignments, and exams can reuse.

## Acceptance Criteria

- [ ] The game defines a weekly class schedule with stable class entries for school days.
- [ ] Each class entry includes at least a course name, weekday, start label, end label, room/location label, and skill/category.
- [ ] The current weekday is derived deterministically from `current_day`.
- [ ] Sleeping into the next day advances the weekday used by the schedule.
- [ ] The game can return the classes scheduled for the current day in display order.
- [ ] The game can return a concise "next class" or "no classes today" summary for UI and future systems.
- [ ] A lightweight schedule readout is visible without overlapping existing money, XP, energy, stress, inventory, or mobile controls.
- [ ] Weekends or configured free days return no classes and a clear free-day summary.
- [ ] The schedule system has no attendance rewards or penalties yet; Ticket 021 should own attending class.
- [ ] No new keyboard-only control is added. If a new player-facing control becomes necessary, mobile parity must be included in this ticket.
- [ ] Focused tests cover weekday derivation, schedule lookup, day advancement, free days, summary text, and HUD/readout layout.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 004
- Ticket 005

## Non-Goals

- No attend-class interaction, XP rewards, grade changes, lateness, absences, or stress penalties in this ticket.
- No time-of-day clock, minute-by-minute simulation, alarms, calendar UI, or schedule editing.
- No assignment deadlines or exam scheduling; those belong to later milestone tickets.
- No new map areas unless the implementation needs labels for already-existing rooms.

## Open Questions / Proposed Decisions

- Proposed weekday mapping: Day 1 starts on Monday, then cycles through Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.
- Proposed first schedule: weekday-only sample classes mapped to existing skills and current school rooms, such as Academics, Math, Programming, Electronics, and Discipline.
- Proposed readout: a compact top-left or top-center text block showing day/weekday and today's next class/free-day summary, with tests ensuring it does not overlap existing HUD rectangles.
- Proposed future handoff: Ticket 021 should use the helper APIs from this ticket to validate whether the player can attend a class.

## Risks

- The HUD already has several elements after Tickets 017-019; schedule text must stay compact and tested for overlap.
- Without a time-of-day clock, "next class" can only mean the first or currently relevant class for the day. The copy should avoid implying minute-level scheduling.
- Schedule data should live in a small dedicated module or structured constants so future class attendance and exams do not duplicate it.
