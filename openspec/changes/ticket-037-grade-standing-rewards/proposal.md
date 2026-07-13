# Ticket 037: Rebalance Grade Standing Rewards

## Summary

Make Grade Standing reward good student behavior instead of mostly acting as a punishment meter.

## Notion Ticket

- Ticket: [Ticket 037 - Rebalance Grade Standing Rewards](https://app.notion.com/p/396c34b0c90181689079c862bb954953)
- Status at planning time: Not started
- Type: Feature
- Epic: Academic Systems
- Dependencies:
- Ticket 021
- Ticket 022
- Ticket 023
- Ticket 024

## Acceptance Criteria

- [ ] A successful class attendance increases Grade Standing by 1 exactly once.
- [ ] Assignment submission increases Grade Standing by 3 exactly once.
- [ ] Submitting before the due day grants an additional 1-point early bonus exactly once; submitting on the due day does not.
- [ ] Passing an exam increases Grade Standing by 5, failing decreases it by 6, and missing an assignment decreases it by 5.
- [ ] Grade Standing remains clamped between 0 and 100, and player feedback reports the actual applied change.
- [ ] Tests cover positive and negative Grade Standing changes.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add explicit balance constants: class `+1`, assignment `+3`, early submission `+1`, exam pass `+5`, exam fail `-6`, and missed assignment `-5`.
- Apply class rewards only after a new attendance ID is recorded and assignment rewards only after an active assignment becomes completed.
- Determine an early submission with `current_day < due_day`; the existing assignment status prevents repeat rewards.
- Extend the existing class and assignment result dialogue with the actual clamped Grade Standing increase.
- Preserve the existing exam and missed-deadline paths, changing only the exam failure balance from 8 to 6.
- Cover keyboard and mobile success paths, normal/early submissions, one-time guards, penalties, and bounds in focused tests.

## Approval Status

Approved by the user through the instruction to proceed on 2026-07-13 after the ticket plan was reconciled with Notion.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.
