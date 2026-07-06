# Ticket 022: Add Assignment System

## Summary

Create an assignment system with deterministic assignment data, day-based deadlines, completion rewards, and missed-deadline consequences. The current game has `current_day`, weekly schedules, class attendance, skills, energy, stress, and sleep; this ticket should build on those systems without adding a full time-of-day clock or grade-standing stat yet.

## Acceptance Criteria

- [ ] The game defines assignment records with stable IDs, title, related skill/category, assigned day, due day, reward XP, and completion status.
- [ ] Assignments can be created from deterministic starter data and/or schedule-linked class data without duplicating schedule definitions unnecessarily.
- [ ] Active assignments are stored in game state and survive room changes.
- [ ] The player can view a concise assignment summary in the HUD or another existing lightweight UI surface without overlapping current HUD/mobile UI.
- [ ] The player can complete an available assignment through an in-world interaction that uses the existing `E`/mobile action path.
- [ ] Completing an assignment before or on its due day grants the configured reward XP once.
- [ ] Completing an assignment shows clear dialogue with the assignment title and reward.
- [ ] Completed assignments cannot be rewarded again.
- [ ] Sleeping into the next day checks deadlines and marks newly missed assignments as overdue.
- [ ] Missing an assignment deadline applies a configured stress increase once and shows clear dialogue or summary messaging.
- [ ] The system does not add grade standing, exams, class attendance changes, or time-of-day simulation in this ticket.
- [ ] Keyboard and mobile action paths have the same assignment completion behavior.
- [ ] Focused tests cover assignment creation, HUD/summary, completion reward, duplicate blocking, deadline rollover, missed-deadline stress, and mobile parity.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 004
- Ticket 005
- Ticket 020
- Ticket 019 is an implementation dependency for missed-deadline stress consequences.
- Ticket 021 is available and may be used as context, but assignments should not require attending a class unless explicitly approved.

## Non-Goals

- No grade standing stat or grade penalties; Ticket 024 owns grade standing.
- No exams, boss fights, or exam scheduling; Ticket 023 owns exams.
- No time-of-day clock, minute-level due times, or assignment calendar UI.
- No complex multi-step homework minigame.
- No broad rebalance of study/class XP.

## Open Questions / Proposed Decisions

- Proposed first assignment source: create a small deterministic starter assignment set tied to existing skills and current schedule/course labels.
- Proposed completion interaction: add a distinct assignment desk/marker in the Library, separate from existing Library study stations and class markers.
- Proposed deadline model: due dates use `current_day`, with a starter assignment due after a small number of days.
- Proposed reward: completion grants configured skill XP to the assignment's related skill.
- Proposed missed-deadline consequence: when sleeping advances past a due day, each newly missed incomplete assignment increases stress by a configured amount once.
- Proposed summary: show the next due active assignment or "No active assignments" in a compact HUD line tested for overlap.

## Risks

- The HUD already includes schedule, energy, stress, XP, money, inventory, and mobile controls; assignment summary must remain compact and tested for overlap.
- Sleep already resets several daily systems; deadline processing must preserve existing sleep behavior and dialogue.
- If assignments are later linked to classes, the data model should already support that without requiring a migration.
