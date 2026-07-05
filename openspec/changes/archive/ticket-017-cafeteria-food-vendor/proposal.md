# Ticket 017: Add Cafeteria and Food Vendor

## Summary

Add a Cafeteria area where the player can buy food from a vendor to restore energy. Since the current code only has money and a placeholder food item, this ticket should introduce a small energy stat, display it in the HUD, and make the vendor purchase flow spend money and restore capped energy.

## Acceptance Criteria

- [ ] The Cafeteria is registered as a room with a visible location name.
- [ ] The School map has a clear door/path to the Cafeteria without breaking access to School Entrance, Programming Lab, Electronics Lab, or Library.
- [ ] Entering or exiting the Cafeteria spawns the player on clear floor without colliding with walls, doors, vendor, furniture, bus, desks, or benches.
- [ ] The player has an energy stat with a maximum value and a visible HUD readout.
- [ ] The Cafeteria has a food vendor NPC or station with an interaction hint.
- [ ] Pressing `E` near the vendor buys food when the player has enough money and is not already at full energy.
- [ ] Buying food subtracts the configured meal price, restores the configured energy amount, caps energy at the maximum, and shows a confirmation dialogue.
- [ ] Trying to buy food without enough money leaves money and energy unchanged and shows an insufficient-funds dialogue.
- [ ] Trying to buy food at full energy leaves money unchanged and shows an already-full dialogue.
- [ ] The mobile action button triggers the same vendor interaction as the keyboard action.
- [ ] Focused tests cover room access, clear pathing, successful purchase, capped restore, insufficient funds, full-energy blocking, mobile action parity, and location display.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Dependencies

- Ticket 002
- Ticket 008

## Non-Goals

- No hunger, fatigue drain, time-of-day meal schedules, buffs, penalties, or multi-item shop menu.
- No food inventory purchase flow unless needed by the existing inventory architecture.
- No changes to allowance, bus fare, gate access, or existing lab/library interactions.

## Risks

- School already uses its cardinal room links for School Entrance, Programming Lab, Electronics Lab, and Library. The Cafeteria should use an explicit School door target or another clear map connection without disturbing those existing routes.
- Energy is a new player stat, so tests should cover initialization, capping, and no-op purchase cases to avoid money loss bugs.
- HUD space is already shared by money, XP, inventory, and mobile controls; the energy readout must not overlap existing UI or the mobile action button.
