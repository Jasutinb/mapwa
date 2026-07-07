# Debug Classmate Code Side Hustle Spec

## ADDED Requirements

### Requirement: Side Hustle Offer

The game MUST allow the classmate to offer a debug-code side hustle when prerequisites are available.

#### Scenario: Offer appears

- GIVEN the classmate exists and side hustle prerequisites are satisfied
- WHEN the player talks to the classmate
- THEN the player can accept or complete the debug-code activity

### Requirement: Rewards and Limits

The side hustle MUST grant intended rewards exactly once per allowed completion window.

#### Scenario: Completion rewards player

- GIVEN the player completes the debug-code activity
- WHEN rewards are applied
- THEN money and appropriate skill XP increase with clear feedback

#### Scenario: Repeat guard

- GIVEN the player has already completed the activity for the current allowed window
- WHEN the player tries again
- THEN duplicate rewards are not granted

#### Scenario: Mobile parity

- GIVEN the player uses mobile controls
- WHEN interacting with the classmate side hustle
- THEN the same reward and repeat-guard behavior applies

## Notes

- Source: https://app.notion.com/p/36ec34b0c901818cbc0af65084bb2e83
- Dependencies: Ticket 005, Ticket 025, Ticket 027