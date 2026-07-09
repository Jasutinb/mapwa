# Health Skill Spec

## ADDED Requirements

### Requirement: Health Skill State

The game MUST track Health as a named skill through the existing skill XP system.

#### Scenario: Health is initialized

- GIVEN a new game state
- WHEN skill XP is inspected
- THEN Health exists with the same default behavior as other tracked skills

### Requirement: Wellness Actions Grant Health XP

At least one successful wellness action MUST grant Health XP.

#### Scenario: Successful wellness action grants XP

- GIVEN the player completes an eligible wellness action such as eating, sleeping, resting, or stress management
- WHEN the action succeeds
- THEN Health XP increases and existing Energy or Stress effects still apply correctly

#### Scenario: Failed or unavailable action grants no XP

- GIVEN the wellness action cannot complete
- WHEN the player attempts it
- THEN Health XP does not change

## Notes

- Source: https://app.notion.com/p/36ec34b0c901817495dbe7d57c2e7250
- Dependencies: Ticket 017, Ticket 018, Ticket 019