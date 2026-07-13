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

- [ ] Every available exam interaction shows the exam title, relevant skill, current XP, and recommended XP before commitment.
- [ ] The prompt clearly labels an underprepared attempt as risky and requires “Take Exam” confirmation.
- [ ] Canceling an exam attempt spends no Energy, adds no Stress, and does not change Grade Standing.
- [ ] Canceling records no attempt or exam result and returns to play.
- [ ] Confirming uses the existing energy, pass/fail, Stress, Grade Standing, and reward mechanics exactly once.
- [ ] Keyboard and mobile action/selection paths can both confirm and cancel.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Add a transient `STATE_EXAM_CONFIRM` and `ExamConfirmState`, following the existing sleep-confirmation interaction pattern without changing save data.
- Change `take_exam()` to resolve availability and open a prompt containing the exam title, relevant skill, current XP, and recommended XP.
- Label `current XP < recommended XP` as risky; ready attempts still show the same readiness information before commitment.
- Keep the existing exam resolution mechanics behind `confirm_exam_attempt()` so Energy, attempts, rewards, Stress, and Grade Standing change only after confirmation.
- Make cancellation clear the pending exam and return to play with no gameplay mutation.
- Use existing keyboard arrows/WASD plus E/Enter/Space and the mapped mobile joystick/action button for selection and activation.
- Add focused tests for ready confirmation, risky confirmation, keyboard cancel, mobile confirm/cancel, one-time resolution, and unchanged low-energy behavior after confirmation.

## Approval Status

Approved by the user through the instruction to proceed on 2026-07-13 after the ticket plan was reconciled with Notion and the existing state architecture.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.
