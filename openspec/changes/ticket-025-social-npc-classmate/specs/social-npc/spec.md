# Social NPC Classmate Spec

## ADDED Requirements

### Requirement: Classmate NPC

The game MUST add an interactable classmate NPC that matches the existing character style and can be found in an appropriate school area.

#### Scenario: Classmate appears in school

- GIVEN the player enters the relevant school area
- WHEN sprites are created for the room
- THEN exactly one classmate NPC is present in the visible sprite set and classmate sprite group

#### Scenario: Classmate does not block core interactions

- GIVEN the School room is built
- WHEN the classmate position is inspected
- THEN the classmate does not overlap doors, the school desk, the class marker, the exam marker, or clear transition paths

#### Scenario: Classmate interaction

- GIVEN the player is near the classmate
- WHEN the player presses the PC interaction key
- THEN classmate dialogue starts through the existing dialogue system

#### Scenario: Mobile parity

- GIVEN the player is near the classmate on mobile
- WHEN the player presses the mobile action button
- THEN the same classmate dialogue starts

### Requirement: Social Introduction

The classmate interaction MUST introduce the Social skill or social progression hook without depending on unfinished future quests.

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

- Source: https://app.notion.com/p/36ec34b0c9018138bc5bf6b2f99b256a
- Dependencies: Ticket 005, Ticket 008
- This first version introduces the Social skill but does not add a broader social progression system.
- No new controls are expected; mobile parity should come through the existing action button mapping.
