# Ticket 028: Add Side Hustle: Debug Classmate Code

## Summary

Add a money-making side activity where the player helps debug a classmate's code.

## Notion Ticket

- Ticket: [Ticket 028 - Add Side Hustle: Debug Classmate Code](https://app.notion.com/p/36ec34b0c901818cbc0af65084bb2e83)
- Status at planning time: Not started
- Type: Feature
- Epic: Economy & Side Activities
- Dependencies:
- Ticket 005
- Ticket 025
- Ticket 027

## Acceptance Criteria

- [ ] The classmate can offer a debug-code side hustle when dependencies are available.
- [ ] Completing the activity grants money and appropriate skill progression.
- [ ] The activity has clear success feedback and cannot be spammed for unintended rewards.
- [ ] Energy, stress, or time costs are applied only if explicitly designed in the implementation plan.
- [ ] Tests cover reward application and repeat-use guards.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add a classmate-offered side hustle interaction gated by the needed NPC and skill/economy dependencies.
- Model the activity as a deterministic reward flow, reusing existing money and skill XP helpers.
- Add a repeat-use guard, cooldown, or day-based limit so the side hustle cannot be spammed unexpectedly.
- Surface reward feedback through dialogue and tests.

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