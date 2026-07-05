# Ticket 018: Add Energy Stat

## Summary

Extend the energy stat so it meaningfully limits how much the player can do in one day. Ticket 017 already introduced capped energy, the energy HUD, and food restoration, so this ticket should add daily activity costs, insufficient-energy blocking, and sleep reset behavior.

## Acceptance Criteria

- [ ] Energy remains a capped player stat with a visible HUD readout.
- [ ] Energy is restored to the configured maximum when the player sleeps into the next day.
- [ ] Studying at School costs energy when it starts.
- [ ] Practicing in the Programming Lab costs energy before awarding XP or advancing the Hello World quest.
- [ ] Practicing in the Electronics Lab costs energy before awarding XP.
- [ ] Library Academics, Math, and Discipline study stations cost energy before awarding XP.
- [ ] If the player does not have enough energy for an activity, the activity is blocked, energy is unchanged, XP/rewards/quest progress are not granted, and an insufficient-energy dialogue is shown.
- [ ] Food purchases from the Cafeteria still restore energy up to the cap and remain covered by regression tests.
- [ ] Keyboard and mobile action paths have the same energy-cost and insufficient-energy behavior.
- [ ] Focused tests cover energy reset on sleep, each activity cost path, insufficient-energy blocking, quest non-advancement where relevant, mobile parity, and food restore regression.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 004
- Ticket 017 is now also an implementation dependency because it introduced the baseline energy stat, HUD, and cafeteria restoration.

## Non-Goals

- No time-of-day clock, fatigue animations, health penalties, or automatic energy drain while walking.
- No balancing pass across all future activities beyond the current study/practice interactions.
- No new food items, shop menu, or inventory changes.

## Risks

- Energy costs touch several existing interactions and quests; tests must verify blocked actions do not grant XP or advance objectives.
- The School study action currently uses a delayed study animation and dialogue; the energy cost should happen once at start, not repeatedly during the animation.
- Existing mobile action parity is implemented by converting mobile action into `E`; tests should cover at least one mobile insufficient-energy path so parity stays intact.
