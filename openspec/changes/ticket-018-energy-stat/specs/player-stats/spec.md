# Player Stats Spec

## Requirements

### Requirement: Energy Limits Daily Activities

The game MUST spend energy when the player performs study or practice activities that represent meaningful daily effort.

#### Scenario: School study spends energy

- GIVEN the player is near the School study desk
- AND the player has at least the configured study energy cost
- WHEN the player starts studying
- THEN energy decreases by the study cost
- AND the study animation and XP reward proceed normally

#### Scenario: Programming practice spends energy

- GIVEN the player is near the Programming Lab station
- AND the player has at least the configured programming energy cost
- WHEN the player practices programming
- THEN energy decreases by the programming cost
- AND programming XP and related quest progress proceed normally

#### Scenario: Electronics practice spends energy

- GIVEN the player is near the Electronics Lab station
- AND the player has at least the configured electronics energy cost
- WHEN the player practices electronics
- THEN energy decreases by the electronics cost
- AND electronics XP is granted normally

#### Scenario: Library study spends energy

- GIVEN the player is near any Library study station
- AND the player has at least the configured library study cost
- WHEN the player studies at that station
- THEN energy decreases by the library cost
- AND the matching skill XP is granted normally

### Requirement: Insufficient Energy Blocks Activities

The game MUST block energy-gated activities when the player does not have enough energy.

#### Scenario: Block low-energy activity

- GIVEN the player is near an energy-gated activity
- AND the player's energy is below that activity's configured cost
- WHEN the player presses the keyboard interaction key
- THEN the activity does not start
- AND energy is unchanged
- AND XP, money, quest progress, and animation state are unchanged
- AND an insufficient-energy dialogue is shown

#### Scenario: Mobile parity

- GIVEN the player is near an energy-gated activity
- AND the player's energy is below that activity's configured cost
- WHEN the player presses the mobile action button
- THEN the same blocking behavior occurs as the keyboard interaction

### Requirement: Daily Energy Reset

The game MUST restore energy when the player sleeps into the next day.

#### Scenario: Sleep restores energy

- GIVEN the player's energy is below maximum
- WHEN the player confirms sleep and advances to the next day
- THEN energy is restored to the configured maximum
- AND existing daily reset behavior still occurs

### Requirement: Food Restoration Remains Compatible

The Cafeteria food vendor MUST continue restoring energy up to the maximum after energy costs are introduced.

#### Scenario: Food restores spent energy

- GIVEN the player has spent energy
- AND the player has enough money for a meal
- WHEN the player buys food from the Cafeteria vendor
- THEN money decreases by the meal price
- AND energy increases by the meal amount up to the maximum

## Notes

- Ticket 017 already introduced `MAX_ENERGY`, `MEAL_PRICE`, `MEAL_ENERGY`, the energy HUD, and cafeteria food restoration.
- Energy should be deducted once at the start of an activity, not every frame during animations.
- Do not add passive walking drain in this ticket.
