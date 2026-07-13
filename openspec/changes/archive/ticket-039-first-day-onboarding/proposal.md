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

- [ ] First bus arrival introduces the Student Planner and states that it tracks schedules, assignments, exams, and deadlines.
- [ ] First campus entry explains that Grade Standing changes with class, assignment, and exam outcomes.
- [ ] First school study explains Energy usage/recovery and Stress causes/recovery.
- [ ] Each beat is at most two short dialogue lines and appears only when its matching first-day objective advances.
- [ ] Planner guidance names both desktop `P` and the mobile Planner button.
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

- Add three dialogue constants for Planner/deadlines, Grade Standing, and Energy/Stress.
- Before advancing the bus, campus-entry, or study objective, determine whether it is the current first-day objective.
- Show the matching tutorial only after that objective successfully advances: Planner on first bus arrival, Grade Standing on first campus entry, and Energy/Stress after the first school study begins.
- Use existing quest objective progress as the one-time guard, avoiding new tutorial flags or save-schema changes.
- Preserve existing objective order, rewards, action methods, and keyboard/mobile controls.
- Add tests for exact contextual copy, one-time behavior, quest completion, planner directions, and save/load preservation through existing quest progress.

## Approval Status

Approved by the user through the instruction to proceed on 2026-07-13 after the ticket plan was reconciled with Notion and the existing first-day quest flow.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.
