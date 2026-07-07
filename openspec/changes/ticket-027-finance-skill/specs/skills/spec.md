# Finance Skill Spec

## ADDED Requirements

### Requirement: Finance Skill State

The game MUST track Finance as a named skill through the existing skill XP system.

#### Scenario: Finance is initialized

- GIVEN a new game state
- WHEN skill XP is inspected
- THEN Finance exists with the same default behavior as other tracked skills

### Requirement: Finance XP Source

At least one money-management activity MUST grant Finance XP only after a successful action.

#### Scenario: Successful activity grants XP

- GIVEN the player completes the chosen Finance activity
- WHEN rewards are applied
- THEN Finance XP increases by the configured amount

#### Scenario: Failed activity grants no XP

- GIVEN the Finance activity cannot complete because requirements are not met
- WHEN the player attempts it
- THEN Finance XP does not change

## Notes

- Source: https://app.notion.com/p/36ec34b0c90181ba9ed4ca229c382cb5
- Dependencies: Ticket 002, Ticket 017