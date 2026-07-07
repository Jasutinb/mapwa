# Ticket 038: Add Exam Readiness Warning

## Summary

Warn the player before risky exam attempts so failure feels like an informed choice instead of a trap.

## Notion Ticket

- Ticket: [Ticket 038 - Add Exam Readiness Warning](https://app.notion.com/p/396c34b0c9018131a9a7fb3a1c922548)
- Status at planning time: Not started
- Type: Feature
- Epic: Academic Systems
- Dependencies:
- Ticket 018
- Ticket 019
- Ticket 023
- Ticket 024

## Acceptance Criteria

- [ ] Exam attempts show recommended readiness and current readiness before commitment.
- [ ] Risky attempts require explicit confirmation.
- [ ] Canceling an exam attempt spends no Energy, adds no Stress, and does not change Grade Standing.
- [ ] Confirming still uses the existing exam mechanics.
- [ ] Tests cover confirm and cancel flows, including the mobile path.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Calculate current readiness and recommended readiness before exam commitment.
- Show a warning/confirmation prompt for risky attempts, including clear current-versus-recommended values.
- Make cancel a true no-op for Energy, Stress, Grade Standing, and exam result state.
- Add matching mobile confirmation/cancel paths and tests.

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