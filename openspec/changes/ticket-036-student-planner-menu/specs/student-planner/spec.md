# Student Planner Menu Spec

## ADDED Requirements

### Requirement: Planner Access

The game MUST provide a Student Planner screen or overlay that can be opened and closed on both desktop and mobile.

#### Scenario: Desktop planner toggle

- GIVEN the player is in normal play
- WHEN the player uses the planner desktop control
- THEN the Student Planner opens, and the same control or a clear close action returns to play

#### Scenario: Mobile planner toggle

- GIVEN the player is using mobile controls
- WHEN the player uses the planner mobile control
- THEN the Student Planner opens and closes with equivalent behavior

### Requirement: Planner Content

The planner MUST show non-urgent academic information that no longer belongs in the default HUD.

#### Scenario: Academic details shown

- GIVEN schedule, assignments, exams, Grade Standing, or objective data exists
- WHEN the planner is open
- THEN the planner displays the available data in a readable layout

#### Scenario: Empty state

- GIVEN a planner section has no data
- WHEN the planner is open
- THEN that section shows a clean empty state rather than debug-looking text

## Notes

- Source: https://app.notion.com/p/396c34b0c90181919dfdd4edbb0bc843
- Dependencies: Ticket 020, Ticket 022, Ticket 023, Ticket 024, Ticket 031