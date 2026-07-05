# Economy and Survival Spec

## Requirements

### Requirement: Cafeteria Room Access

The game MUST provide a Cafeteria room reachable from the School map without removing existing School Entrance, Programming Lab, Electronics Lab, or Library access.

#### Scenario: Enter the Cafeteria from School

- GIVEN the player is in the School room
- WHEN the player uses the Cafeteria door
- THEN the current room becomes the Cafeteria
- AND the player spawns on clear Cafeteria floor without colliding with obstacles

#### Scenario: Exit the Cafeteria to School

- GIVEN the player is in the Cafeteria room
- WHEN the player uses the School exit
- THEN the current room becomes the School room
- AND the player spawns on clear School floor without colliding with obstacles, bus sprites, desks, benches, walls, or doors

### Requirement: Energy Stat

The game MUST track player energy as a capped stat and make the current value visible to the player.

#### Scenario: Energy initializes

- GIVEN a new game starts
- WHEN game state is initialized
- THEN energy has a current value
- AND energy does not exceed the configured maximum

#### Scenario: Restore energy with cap

- GIVEN the player's energy is below maximum
- WHEN energy is restored by a food purchase
- THEN energy increases by the configured meal amount
- AND energy does not exceed the configured maximum

#### Scenario: Energy HUD

- GIVEN the game is drawn
- WHEN the HUD renders
- THEN the current energy value is visible
- AND the energy HUD does not overlap the money HUD, XP HUD, inventory bar, or mobile controls

### Requirement: Food Vendor Purchase

The Cafeteria MUST include a food vendor interaction that spends money to restore energy.

#### Scenario: Buy food successfully

- GIVEN the player is near the Cafeteria vendor
- AND the player has at least the configured meal price
- AND the player's energy is below maximum
- WHEN the player presses the keyboard interaction key
- THEN money decreases by the meal price
- AND energy increases by the meal energy amount up to the maximum
- AND a confirmation dialogue states the purchase and energy total

#### Scenario: Not enough money

- GIVEN the player is near the Cafeteria vendor
- AND the player has less than the configured meal price
- WHEN the player presses the keyboard interaction key
- THEN money is unchanged
- AND energy is unchanged
- AND an insufficient-funds dialogue is shown

#### Scenario: Energy already full

- GIVEN the player is near the Cafeteria vendor
- AND the player's energy is already at maximum
- WHEN the player presses the keyboard interaction key
- THEN money is unchanged
- AND energy remains at maximum
- AND an already-full dialogue is shown

#### Scenario: Mobile parity

- GIVEN the player is near the Cafeteria vendor
- WHEN the player presses the mobile action button
- THEN the same purchase, blocking, money, energy, and dialogue behavior occurs as the keyboard interaction

## Notes

- The current inventory has a placeholder consumable food item, but it does not restore energy. This ticket should prefer the direct vendor purchase flow unless implementation reveals a low-risk way to connect the placeholder item without expanding scope.
- Use existing map primitives and NPC styling for the vendor; no new art dependency is required.
