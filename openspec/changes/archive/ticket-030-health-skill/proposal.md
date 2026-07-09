# Ticket 030: Add Health Skill

## Summary

Add Health as a skill connected to eating, sleeping, resting, and stress management.

## Notion Ticket

- Ticket: [Ticket 030 - Add Health Skill](https://app.notion.com/p/36ec34b0c901817495dbe7d57c2e7250)
- Status at planning time: Not started
- Type: Feature
- Epic: Skills & Progression
- Dependencies:
- Ticket 017
- Ticket 018
- Ticket 019

## Acceptance Criteria

- [ ] Health exists as a named skill in the skill progression model.
- [ ] Eating, sleeping, resting, or stress-management actions can grant Health XP where appropriate.
- [ ] Existing Energy and Stress behavior is preserved unless explicitly changed.
- [ ] Skill rewards are deterministic and not granted repeatedly by accident.
- [ ] Tests cover at least one Health XP source and no unintended Energy or Stress regression.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add Health as a skill identifier using the existing skill XP manager.
- Choose one or more existing recovery actions, such as sleeping or eating, as deterministic Health XP sources.
- Preserve Energy and Stress effects unless the implementation plan explicitly adjusts them.
- Test Health XP gain and guard against duplicate or failed-action XP.

## Approval Status

Approved by the user on July 9, 2026. Implementation is scoped to adding Health as a tracked skill and awarding deterministic Health XP on successful existing wellness actions, starting with eating and sleeping, while preserving current Energy and Stress behavior.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.
