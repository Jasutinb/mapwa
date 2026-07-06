# Exams Spec

## Requirements

### Requirement: Exam Definitions

The system MUST define deterministic exams with stable IDs, subject labels, skill keys, scheduled day, room, recommended XP, reward XP, energy cost, stress consequence, attempt count, and status.

#### Scenario: Initial exams exist

- GIVEN a new game state
- WHEN exam state is inspected
- THEN at least one exam exists with a stable ID, skill, scheduled day, room, recommended XP, reward XP, and active status

#### Scenario: Exam state survives room transitions

- GIVEN an exam has an attempt count or completed status
- WHEN the player changes rooms
- THEN the exam state remains unchanged

### Requirement: Exam Availability

The system MUST make exams available only when the player is in the exam's scheduled room on or after its scheduled day and the exam is not already completed.

#### Scenario: Scheduled exam available in matching room

- GIVEN today is an exam's scheduled day or later
- AND the player is in the exam's room
- WHEN the player approaches the exam marker
- THEN the player can start that exam

#### Scenario: Exam unavailable before scheduled day

- GIVEN today is before an exam's scheduled day
- WHEN the player approaches an exam marker
- THEN the exam cannot be started and clear feedback is shown

#### Scenario: Exam unavailable in wrong room

- GIVEN an active exam exists for another room
- WHEN the player interacts away from that room
- THEN the exam does not start

### Requirement: Exam Interaction

The system MUST start exams through the same interaction path used by other in-world actions.

#### Scenario: Keyboard starts exam

- GIVEN the player is near an available exam marker
- WHEN the player presses `E`
- THEN the exam resolves and displays pass or fail feedback

#### Scenario: Mobile parity

- GIVEN the player is near an available exam marker
- WHEN the player presses the mobile action button
- THEN the same exam resolution path is used

### Requirement: Exam Resolution

The system MUST resolve exams deterministically from current skill XP, energy, and stress.

#### Scenario: Passing exam

- GIVEN the player has enough energy
- AND the relevant skill XP meets the exam's recommended XP
- WHEN the player starts the exam
- THEN the exam is marked passed
- AND reward XP is granted once
- AND pass feedback is shown

#### Scenario: Failing exam

- GIVEN the player has enough energy
- AND the relevant skill XP is below the exam's recommended XP
- WHEN the player starts the exam
- THEN the exam attempt count increases
- AND stress increases by the configured exam stress consequence
- AND fail feedback is shown
- AND the player is not blocked from continuing normal play

#### Scenario: Insufficient energy

- GIVEN the player's energy is below the exam energy cost
- WHEN the player attempts to start an available exam
- THEN the exam does not resolve
- AND existing insufficient-energy feedback is shown

#### Scenario: Completed exam does not reward again

- GIVEN an exam has already been passed
- WHEN the player attempts to interact with its marker again
- THEN no additional reward XP is granted
- AND clear already-completed feedback is shown

### Requirement: Exam HUD

The system MUST show a concise exam summary without overlapping existing UI.

#### Scenario: Exam summary shown

- GIVEN the game is drawn
- WHEN active exams exist
- THEN a concise exam summary appears near the existing schedule/assignment HUD stack

#### Scenario: HUD avoids existing UI

- GIVEN the game is drawn on the default viewport
- WHEN the exam HUD rectangle is measured
- THEN it does not overlap schedule, assignment, energy, stress, inventory, or mobile action controls

### Requirement: Sleep Persistence

The system MUST preserve exam state across sleeping and day advancement.

#### Scenario: Sleeping advances exam availability

- GIVEN an exam is scheduled for the next day
- WHEN the player sleeps
- THEN the current day advances
- AND the exam can become available if the player goes to the matching room

#### Scenario: Sleeping preserves completed exam

- GIVEN an exam is already passed
- WHEN the player sleeps
- THEN the exam remains passed
- AND its reward cannot be collected again

## Notes

- Ticket 024 owns grade standing; this ticket should only record exam pass/fail state and immediate rewards/consequences.
- Keep the first version deterministic for testability and WASM stability.
- Place markers so they do not block map paths or take priority over nearby study/class/assignment interactions.
