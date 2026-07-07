# Ticket 039: Add First-Day Academic Onboarding Beats

## Summary

Teach Energy, Stress, Grade Standing, assignments, exams, and deadlines through short first-day tutorial beats.

## Notion Ticket

- Ticket: [Ticket 039 - Add First-Day Academic Onboarding Beats](https://app.notion.com/p/396c34b0c90181e8a5e1ca9d210e22bb)
- Status at planning time: Not started
- Type: Content
- Epic: Onboarding
- Dependencies:
- Ticket 018
- Ticket 019
- Ticket 020
- Ticket 021
- Ticket 022
- Ticket 023
- Ticket 024
- Ticket 036

## Acceptance Criteria

- [ ] New players encounter brief explanations for Energy, Stress, Grade Standing, assignments, exams, and deadlines during the first-day flow.
- [ ] Tutorial beats are contextual and do not block normal play longer than necessary.
- [ ] The player is directed to the Student Planner when schedule or deadline information matters.
- [ ] Existing first-day quest flow still works.
- [ ] Tests cover any new quest flags or state transitions.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add short tutorial beats to the existing first-day quest/state flow rather than building a separate tutorial mode.
- Introduce Energy, Stress, Grade Standing, assignments, exams, and deadlines at the moment each concept first matters.
- Reference the Student Planner once it exists so schedule/deadline guidance has a home.
- Track tutorial flags or quest state carefully to avoid repeating beats unnecessarily.

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