# Social NPC Spec

## Requirements

### Requirement: Social Skill Introduction

The system MUST introduce a Social skill through a classmate NPC interaction.

#### Scenario: First classmate conversation grants Social XP

- GIVEN the player is near the classmate NPC
- WHEN the player interacts with the classmate for the first time
- THEN classmate intro dialogue is shown
- AND the player gains the configured Social XP reward
- AND the game records that the classmate introduction has happened

#### Scenario: Repeat classmate conversation does not reward twice

- GIVEN the player has already completed the classmate introduction
- WHEN the player interacts with the classmate again
- THEN repeat dialogue is shown
- AND Social XP does not increase

### Requirement: Classmate NPC Placement

The system MUST place a classmate NPC in an existing school area without blocking required movement or interactions.

#### Scenario: Classmate appears in school

- GIVEN the School room is built
- WHEN sprites are inspected
- THEN exactly one classmate NPC is present in the visible sprite set and classmate sprite group

#### Scenario: Classmate does not block core school interactions

- GIVEN the School room is built
- WHEN the classmate position is inspected
- THEN the classmate does not overlap doors, the school desk, the class marker, the exam marker, or clear transition paths

### Requirement: PC and Mobile Interaction Parity

The system MUST expose the classmate interaction through both PC and mobile action paths.

#### Scenario: PC interaction talks to classmate

- GIVEN the player is near the classmate NPC
- WHEN the player presses `E`
- THEN the classmate interaction runs

#### Scenario: Mobile action talks to classmate

- GIVEN the player is near the classmate NPC
- WHEN the player taps the mobile action button
- THEN the same classmate interaction runs

### Requirement: Existing Interactions Remain Stable

The system MUST preserve existing player-facing interactions after adding the classmate NPC.

#### Scenario: Existing school interactions still work

- GIVEN the player is near an existing school interactable such as the school desk, class marker, exam marker, or a room door
- WHEN the player uses the existing interaction or transition
- THEN the existing behavior still occurs

#### Scenario: Existing NPC interactions still work

- GIVEN the player is near an existing NPC such as Mom, the guard, the admin attendant, or the food vendor
- WHEN the player uses the existing interaction
- THEN the existing dialogue or action still occurs

## Notes

- This first version introduces the Social skill but does not add a broader social progression system.
- The classmate should use existing NPC art conventions and avoid unrelated placeholder styling.
- No new controls are expected; mobile parity should come through the existing action button mapping.
