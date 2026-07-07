# Commuting Skill Spec

## ADDED Requirements

### Requirement: Commuting Skill State

The game MUST track Commuting as a named skill through the existing skill XP system.

#### Scenario: Commuting is initialized

- GIVEN a new game state
- WHEN skill XP is inspected
- THEN Commuting exists with the same default behavior as other tracked skills

### Requirement: Travel Grants Commuting XP

Successful travel MUST be able to grant Commuting XP.

#### Scenario: Successful bus ride grants XP

- GIVEN the player has enough money for the bus
- WHEN the bus ride completes
- THEN money is spent and Commuting XP increases

#### Scenario: Failed bus ride grants no XP

- GIVEN the player does not have enough money for the bus
- WHEN the player attempts to ride
- THEN room, money, and Commuting XP remain unchanged

## Notes

- Source: https://app.notion.com/p/36ec34b0c901813c9445dfae8ceb2763
- Dependencies: Ticket 003, Ticket 005