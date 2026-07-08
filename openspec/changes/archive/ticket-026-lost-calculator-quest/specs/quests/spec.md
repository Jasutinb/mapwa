# Lost Calculator Quest Spec

## ADDED Requirements

### Requirement: Quest Start

The game MUST allow the classmate NPC to start a Lost Calculator side quest.

#### Scenario: Start quest from classmate

- GIVEN Ticket 025 classmate exists and the quest is not active or complete
- WHEN the player interacts with the classmate
- THEN the Lost Calculator quest is added to active quest state with a clear objective

### Requirement: Calculator Retrieval

The game MUST let the player find, pick up, and return the calculator.

#### Scenario: Calculator appears while quest is active

- GIVEN Lost Calculator is active
- WHEN the player enters the target location
- THEN the calculator item is available on clear floor or via a clear interaction point

#### Scenario: Return calculator

- GIVEN the player has picked up the calculator
- WHEN the player talks to the classmate
- THEN the quest completes, rewards apply once, and the calculator is removed or marked delivered

#### Scenario: Mobile parity

- GIVEN the player is on mobile
- WHEN the player uses mobile movement and action controls
- THEN the quest can be started, advanced, and completed through equivalent interactions

## Notes

- Source: https://app.notion.com/p/36ec34b0c901814f8f66f94248fc105f
- Dependencies: Ticket 009, Ticket 012, Ticket 025