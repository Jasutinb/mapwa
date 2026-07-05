# Player Stats Spec

## Requirements

### Requirement: Stress Is A Capped Player Stat

The game MUST store stress as a player stat with configured bounds and a visible HUD readout.

#### Scenario: New game starts with baseline stress

- GIVEN a new game starts
- WHEN the game state is initialized
- THEN stress is set to the configured starting value
- AND the value is within the configured stress bounds

#### Scenario: Stress values are clamped

- GIVEN stress is assigned or changed
- WHEN the value would fall below the minimum or exceed the maximum
- THEN the stored stress value is clamped to the configured bounds

#### Scenario: Stress is visible in the HUD

- GIVEN the game is drawn
- WHEN the HUD is rendered
- THEN the player can see current stress and maximum stress
- AND the stress HUD does not overlap money, inventory, mobile controls, or the energy HUD

### Requirement: Sleep Recovers Stress

The game MUST reduce stress when the player sleeps into the next day.

#### Scenario: Sleep reduces stress

- GIVEN the player's stress is above the minimum
- WHEN the player sleeps into the next day
- THEN stress decreases by the configured sleep recovery amount
- AND stress does not fall below the configured minimum
- AND existing next-day behavior, including energy restoration, still occurs

### Requirement: Low Energy Schoolwork Adds Stress

The game MUST increase stress when the player is too tired to perform energy-gated schoolwork.

#### Scenario: Blocked schoolwork increases stress

- GIVEN the player is near an energy-gated study or practice activity
- AND the player's energy is below that activity's configured cost
- WHEN the player presses the keyboard interaction key
- THEN the activity remains blocked
- AND stress increases by the configured low-energy stress amount
- AND stress does not exceed the configured maximum
- AND energy, XP, quest progress, money, and animation state remain unchanged
- AND the player sees dialogue explaining that they are too tired

#### Scenario: Mobile parity

- GIVEN the player is near an energy-gated study or practice activity
- AND the player's energy is below that activity's configured cost
- WHEN the player presses the mobile action button
- THEN the same stress increase and blocking behavior occurs as the keyboard interaction

### Requirement: Unrelated Blocks Do Not Add Stress

The game MUST only add stress for the explicit stress sources in this ticket.

#### Scenario: Insufficient money does not add stress

- GIVEN the player does not have enough money for a cafeteria meal
- WHEN the player tries to buy food
- THEN the purchase remains blocked
- AND stress is unchanged
- AND the existing insufficient-money dialogue is shown

## Notes

- Ticket 018 already introduced energy-gated study and practice activities. This ticket should reuse those paths rather than duplicating per-room stress logic.
- Future deadline and exam systems should call the stress helper APIs introduced by this ticket when those mechanics are added.
- Stress should not passively increase every frame or while walking.
