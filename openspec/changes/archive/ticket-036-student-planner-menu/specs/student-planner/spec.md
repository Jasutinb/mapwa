# Student Planner Menu Spec

## ADDED Requirements

### Requirement: Planner Access Parity

The game MUST provide equivalent desktop and mobile controls for opening and closing the Student Planner from normal play.

#### Scenario: Desktop planner toggle

- GIVEN the player is in normal play
- WHEN the player presses `P`
- THEN the Student Planner opens
- AND pressing `P` again returns to play

#### Scenario: Desktop planner escape

- GIVEN the Student Planner is open
- WHEN the player presses `Esc`
- THEN the planner closes and normal play resumes
- AND a pause menu is not opened over the planner

#### Scenario: Mobile planner toggle

- GIVEN the player is in normal play on a touch device
- WHEN the player taps the Planner button
- THEN the Student Planner opens
- AND tapping the Planner button again returns to play

#### Scenario: Planner cannot interrupt modal states

- GIVEN dialogue, sleep confirmation, or the pause menu is active
- WHEN a planner input is received
- THEN the current modal state remains active

### Requirement: Planner Academic Content

The planner MUST show live non-urgent academic and objective data without changing the underlying systems.

#### Scenario: Populated planner

- GIVEN schedule, active assignment, pending exam, Grade Standing, and active objective data exists
- WHEN the planner opens
- THEN today's classes display in schedule order
- AND assigned active assignments display in due-date order
- AND pending exams display in scheduled-date order
- AND Grade Standing and the current objective display from live state

#### Scenario: Planner empty states

- GIVEN no classes are scheduled today and assignment, exam, or objective data is absent
- WHEN the planner opens
- THEN each empty section shows concise player-facing copy
- AND no section exposes debug representations or placeholder object data

### Requirement: Planner Layout Isolation

The planner MUST remain readable at the configured 800x600 game resolution and keep default HUD elements from competing with it.

#### Scenario: Planner is open

- GIVEN the planner state is active
- WHEN the frame is drawn
- THEN all planner cards remain inside the screen and planner panel
- AND the default urgent HUD and inventory are not drawn over the planner
- AND the mobile Planner close button remains visible without overlapping other mobile controls

#### Scenario: Planner is closed

- GIVEN normal play is active
- WHEN the frame is drawn
- THEN the default HUD still shows urgent player state
- AND schedule, assignment, exam, and grade HUD rectangles remain empty

## Notes

- Canonical source: https://app.notion.com/p/396c34b0c90181919dfdd4edbb0bc843
- Dependencies: Ticket 020, Ticket 022, Ticket 023, Ticket 024, Ticket 031
