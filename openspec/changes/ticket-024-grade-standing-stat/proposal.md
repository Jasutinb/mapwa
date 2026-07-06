# Ticket 024: Add Grade Standing Stat

## Summary

Add a Grade Standing stat that represents the student's academic performance across class attendance, assignments, and exams. The first version should be deterministic, readable, and easy to verify, using already-shipped progression systems rather than inventing a separate grading minigame.

## Notion Ticket

- Ticket: [Ticket 024 - Add Grade Standing Stat](https://app.notion.com/p/36ec34b0c901816fa89bc75265f02b03)
- Status at planning time: Not started
- Dependencies: Ticket 021, Ticket 022, and Ticket 023 are Done in Notion.

## Acceptance Criteria

- [ ] Grade standing is stored in player state and survives room transitions and sleeping.
- [ ] Grade standing has a bounded numeric scale with a clear default starting value.
- [ ] Passing exams can improve grade standing.
- [ ] Missing assignments or failing exams can reduce grade standing.
- [ ] Grade standing updates deterministically from existing academic systems rather than random rolls.
- [ ] Grade standing changes are reflected in clear player feedback when the stat changes.
- [ ] Grade standing appears in the HUD without overlapping schedule, assignment, exam, energy, stress, inventory, or mobile UI.
- [ ] Existing keyboard and mobile controls remain unchanged unless a new interaction is added.
- [ ] Existing class attendance, assignment, exam, sleep, study, energy, stress, cafeteria, quest, and map transition behavior still works.
- [ ] Focused tests cover initialization, clamping, positive and negative grade changes, persistence across sleep/room changes, and HUD layout.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 021
- Ticket 022
- Ticket 023

## Proposed Implementation

- Add grade-standing constants in `src/config.py`:
  - min/max bounds: `0` to `100`
  - starting value: `75`
  - passed exam change: `+5`
  - failed exam change: `-8`
  - missed assignment change: `-5` per missed assignment
- Store grade standing on `GameState` with a `Game.grade_standing` property and clamped helper method that returns the actual changed amount.
- Apply grade-standing updates from existing high-signal academic outcomes:
  - passed exams increase grade standing when the exam is first marked passed
  - failed exam attempts decrease grade standing when the failed attempt is applied
  - missed assignments decrease grade standing once, reusing the existing missed-deadline one-time guard
- Draw grade standing as a compact HUD line below the exam summary, tracking its own rectangle for layout tests.
- Reuse the existing dialogue system to append meaningful grade-standing feedback to exam and missed-assignment messages.

## Non-Goals

- No transcript, GPA breakdown, letter-grade transcript export, or semester history.
- No new input surface unless we later decide the player needs a dedicated grade view.
- No rebalancing of class attendance, assignment, or exam rewards beyond what grade standing needs.

## Risks

- Grade standing could become noisy if too many small events change it every day.
- HUD crowding is a growing risk now that schedule, assignments, exams, energy, and stress are all visible.
- The stat should not accidentally double-apply when revisiting completed content or sleeping multiple times.
