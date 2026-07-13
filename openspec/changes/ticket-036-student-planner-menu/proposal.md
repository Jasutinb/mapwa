# Ticket 036: Add Student Planner Menu

## Summary

Add a dedicated, phone-style Student Planner state that presents non-urgent academic information without returning it to the always-visible HUD.

## Notion Ticket

- Ticket: [Ticket 036 - Add Student Planner Menu](https://app.notion.com/p/396c34b0c90181919dfdd4edbb0bc843)
- Status at planning time: Not started
- Type: Feature
- Epic: UI/UX
- Priority: P1
- Dependencies: Ticket 020, Ticket 022, Ticket 023, Ticket 024, Ticket 031

## Current System Assessment

- The default HUD already limits itself to urgent money, objective, energy, and stress information.
- Schedule, assignment, exam, grade, and quest data are available through `GameState` and existing helper methods.
- The state machine currently supports play, dialogue, sleep confirmation, and pause menu states.
- Desktop `Esc` and a mobile Menu button already share event-routing patterns that can be extended for planner parity.

## Approved Implementation Plan

1. Add a `STATE_PLANNER` constant and a `PlannerState` registered with the existing state machine.
2. Add `P` as the desktop planner toggle; allow `P` or `Esc` to close the planner while preventing it from opening over dialogue, sleep confirmation, or the pause menu.
3. Add a non-overlapping mobile Planner button with one-shot press consumption and synthesize the same planner key event used by desktop.
4. Build planner sections from live state:
   - today's class schedule;
   - currently assigned active assignments;
   - pending upcoming exams;
   - current Grade Standing;
   - the active quest objective.
5. Render a readable phone/menu-style overlay with explicit empty-state copy for schedule, assignments, exams, and objectives.
6. Hide the default HUD and inventory while the planner is open, while retaining the mobile Planner close affordance.
7. Update the README controls table and add focused tests for desktop/mobile toggles, content, empty states, and layout boundaries.
8. Run focused tests, Ruff, the full parallel pytest suite, headless render smoke, strict OpenSpec validation, and the pygbag archive build.

## Acceptance Criteria

- [ ] `P` opens and closes the Student Planner from normal desktop play.
- [ ] `Esc` closes the planner without opening a nested pause menu.
- [ ] A dedicated mobile Planner button opens and closes the same state.
- [ ] The mobile Planner button does not overlap the Menu, Action, dialogue, inventory, or urgent HUD areas.
- [ ] Planner schedule, assignments, exams, Grade Standing, and objective sections use live game state.
- [ ] Sections without data display clean player-facing empty states.
- [ ] The default play HUD remains focused on urgent state and planner-owned details remain absent from it.
- [ ] HUD and inventory do not draw over the open planner.
- [ ] README controls remain accurate.
- [ ] Focused desktop and mobile planner tests pass.
- [ ] `uv run ruff check .` and `uv run pytest -n auto` pass.
- [ ] Headless render smoke, strict OpenSpec validation, and pygbag archive build pass.
- [ ] PR and post-merge main CI/CD are green.
- [ ] The canonical Notion ticket is updated and this change is archived after merge.

## Approval Status

Approved by the user on 2026-07-13 with the instruction to proceed.

## Non-Goals

- Changing schedule, assignment, exam, quest, grade, reward, or consequence rules.
- Adding planner editing, reminders, calendar navigation, or new academic data.
- Refactoring unrelated `Game` responsibilities tracked by Ticket 040.
- Reintroducing academic detail panels to the default play HUD.

## Risks and Mitigations

- **Planner competes with HUD/mobile controls:** use a dedicated state, suppress play HUD/inventory while open, and reserve a clear close affordance.
- **Desktop/mobile behavior diverges:** route both through one planner key event and cover both paths in tests.
- **Long labels overflow cards:** wrap and truncate section lines within fixed layout bounds.
- **Pygbag font differences:** use the project's system-font fallback pattern and verify a web archive build.
