# Ticket 019: Add Stress Stat

## Summary

Add stress as a capped player stat that tracks the consequence side of daily school life. Ticket 018 added energy costs and daily limits, so this ticket should introduce stress state, HUD visibility, helper APIs, and the first concrete stress sources that exist in the current game loop.

## Acceptance Criteria

- [ ] Stress is stored in game state as a capped stat with a configured minimum and maximum.
- [ ] New games start with the configured baseline stress.
- [ ] The HUD displays stress without overlapping the existing money, inventory, mobile controls, or energy HUD.
- [ ] Sleeping into the next day reduces stress by a configured recovery amount.
- [ ] Stress increases when the player attempts meaningful schoolwork while too tired, using the existing insufficient-energy path from Ticket 018.
- [ ] Stress helper methods clamp values and return the amount changed, matching the energy helper pattern.
- [ ] Stress changes show clear player-facing dialogue where the change happens.
- [ ] Keyboard and mobile action paths produce the same stress behavior for low-energy blocked activities.
- [ ] Focused tests cover initial stress, clamping, HUD placement, sleep recovery, insufficient-energy stress increase, mobile parity, and no stress change for unrelated blocked actions such as insufficient money.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 004
- Ticket 018, because stress should build on the energy-gated activity behavior introduced there.

## Non-Goals

- No exam calendar, deadline system, assignments, or time-of-day schedule in this ticket.
- No grade penalties, health penalties, random events, or passive stress ticking.
- No broad rebalance of study rewards or energy costs.
- No persistence/save-file migration unless the repo already has a save system to update.

## Open Questions / Proposed Decisions

- The ticket mentions missed deadlines and exams, but those mechanics do not exist yet. Proposed decision: add explicit stress helper APIs now and integrate those future sources when deadline/exam tickets are implemented.
- Proposed current stress source: when an energy-gated study/practice action is blocked because the player is too tired, stress increases by a small configured amount.
- Proposed current recovery: sleeping reduces stress by a configured amount, then restores energy as Ticket 018 already does.

## Risks

- The top-right HUD already contains energy, so stress needs careful layout tests to avoid stacked text overlap.
- If stress is added directly inside `spend_energy`, every future energy-gated action may gain stress behavior by default. The implementation should make that intentional and test the current call sites.
- Dialogue should remain wrapped inside the dialogue box after the recent dialogue-layout bugfix.
