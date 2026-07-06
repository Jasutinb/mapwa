# Ticket 023: Add Exams as Boss Fights

## Summary

Implement exams as major progression checks that feel like lightweight RPG boss fights. Exams should use existing progression systems from earlier tickets: class schedule, energy, stress, and skill XP. The first version should be deterministic, small, testable, and playable from an in-world exam marker rather than adding a full combat engine.

## Acceptance Criteria

- [ ] Exam records exist with stable IDs, subject/skill, scheduled day, room, minimum recommended skill XP, energy cost, stress consequence, and completion result.
- [ ] The player can start an available exam from an in-world marker using `E`.
- [ ] Mobile action triggers the same exam-start path as keyboard interaction.
- [ ] Exams resolve deterministically from current skill XP, energy, and stress.
- [ ] Passing an exam grants a clear reward once and records the exam as passed.
- [ ] Failing an exam records an attempt, increases stress, and gives clear feedback without blocking future play.
- [ ] Completed exams cannot be farmed for repeated rewards.
- [ ] Exam availability respects scheduled day/room and survives room transitions.
- [ ] Exam HUD/summary avoids overlapping existing schedule, assignment, energy, stress, inventory, and mobile UI.
- [ ] Sleeping advances day without breaking exam availability or completed exam state.
- [ ] PC controls and mobile controls have parity.
- [ ] Existing map entrances/exits continue to spawn the player on clear floor.
- [ ] Focused tests cover creation, availability, pass/fail resolution, duplicate blocking, stress/energy effects, HUD layout, sleep behavior, and mobile parity.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 005
- Ticket 018
- Ticket 019
- Ticket 020

## Proposed Implementation

- Add a small `src/exams.py` model with deterministic starter exams.
- Store exam state on `GameState` so results survive room changes and sleep.
- Add a distinct non-blocking `ExamMarker` sprite in the scheduled exam rooms, likely near class markers but far enough not to conflict with study/class interactions.
- Add `Game` helpers for exam availability, summary text, marker proximity, and deterministic resolution.
- Use current skill XP as the main success input, energy as the participation cost, and stress as a penalty/risk factor.
- Start with a deterministic pass threshold, for example `skill_xp >= recommended_xp` and enough energy, with stress increasing after failed attempts.
- Draw a concise exam HUD line below the existing schedule/assignment HUD stack.
- Route player input through the existing `E` and mobile action button path.

## Non-Goals

- No grade standing stat or GPA calculation; that belongs to Ticket 024.
- No full combat/battle engine, animations, timed minigame, or random exam questions.
- No exam retake calendar beyond deterministic retry availability in this ticket.
- No changes to itch deploy pipeline.

## Risks

- Exam markers could conflict with class markers or study stations if placed too close.
- HUD stacking could overlap the growing schedule/assignment/stat UI.
- Exam pass/fail rules could accidentally depend on random behavior or become hard to test.
- Stress and energy effects must not regress existing sleep, study, cafeteria, assignment, or class attendance behavior.
