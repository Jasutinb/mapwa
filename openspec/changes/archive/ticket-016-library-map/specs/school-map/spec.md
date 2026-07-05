# School Map Spec

## Requirements

### Requirement: Library Room Access

The game MUST provide a Library room reachable from the School map without removing the existing School Entrance, Programming Lab, or Electronics Lab routes.

#### Scenario: Enter the Library from School

- GIVEN the player is in the School room
- WHEN the player uses the Library door
- THEN the current room becomes the Library
- AND the player spawns on clear Library floor without colliding with obstacles

#### Scenario: Exit the Library to School

- GIVEN the player is in the Library room
- WHEN the player uses the School exit
- THEN the current room becomes the School room
- AND the player spawns on clear School floor without colliding with obstacles, benches, desks, bus sprites, or walls

### Requirement: Library Skill Stations

The Library MUST include separate interaction stations for Academics, Math, and Discipline training.

#### Scenario: Train Academics

- GIVEN the player is in the Library near the Academics station
- WHEN the player presses the keyboard interaction key
- THEN the player gains Academics XP
- AND a confirmation dialogue names the Academics reward and total

#### Scenario: Train Math

- GIVEN the player is in the Library near the Math station
- WHEN the player presses the keyboard interaction key
- THEN the player gains Math XP
- AND a confirmation dialogue names the Math reward and total

#### Scenario: Train Discipline

- GIVEN the player is in the Library near the Discipline station
- WHEN the player presses the keyboard interaction key
- THEN the player gains Discipline XP
- AND a confirmation dialogue names the Discipline reward and total

#### Scenario: Mobile parity

- GIVEN the player is near any Library skill station
- WHEN the player presses the mobile action button
- THEN the same skill XP and dialogue behavior occurs as the keyboard interaction

### Requirement: Library Location Display

The game MUST show `Library` as the location display text when the Library map is created.

#### Scenario: Library location name

- GIVEN the current room is Library
- WHEN the map is created
- THEN the location display text is `Library`

## Notes

- This change introduces Math and Discipline as tracked skill IDs because they do not exist yet in the current codebase.
- The Library should reuse existing map primitives and visual style instead of adding new art dependencies.
- Station placement should avoid overlapping proximity zones where one action could ambiguously choose multiple rewards.
