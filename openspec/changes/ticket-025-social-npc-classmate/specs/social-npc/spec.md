# Social NPC Classmate Spec

## ADDED Requirements

### Requirement: Classmate NPC

The game MUST add an interactable classmate NPC that matches the existing character style and can be found in an appropriate school area.

#### Scenario: Classmate appears in school

- GIVEN the player enters the relevant school area
- WHEN sprites are created for the room
- THEN the classmate NPC is present on clear floor and does not block required paths

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

#### Scenario: Social skill introduced

- GIVEN the player talks to the classmate for the first time
- WHEN the dialogue completes
- THEN the player receives clear feedback about social progression or its future purpose

## Notes

- Source: https://app.notion.com/p/36ec34b0c9018138bc5bf6b2f99b256a
- Dependencies: Ticket 005, Ticket 008