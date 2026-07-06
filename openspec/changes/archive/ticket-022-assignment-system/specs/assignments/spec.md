# Assignments Spec

## Requirements

### Requirement: Assignment Records

The game MUST model assignments with deadlines and rewards.

#### Scenario: Starter assignments exist

- GIVEN a new game starts
- WHEN assignments are initialized
- THEN at least one active assignment exists
- AND each assignment has a stable ID, title, skill/category, assigned day, due day, reward XP, and status

#### Scenario: Assignment summary is available

- GIVEN active assignments exist
- WHEN the assignment summary is requested
- THEN the game returns a concise next-due assignment summary
- AND completed or missed assignments are not presented as active work

### Requirement: Complete Assignments For Rewards

The game MUST let the player complete available assignments and receive rewards once.

#### Scenario: Complete assignment before deadline

- GIVEN the player has an active assignment that is not overdue
- AND the player is near the assignment interaction marker
- WHEN the player presses the keyboard interaction key
- THEN the assignment is marked completed
- AND the assignment skill receives the configured reward XP
- AND dialogue confirms the assignment title and reward

#### Scenario: Mobile action completes assignment

- GIVEN the player has an active assignment that is not overdue
- AND the player is near the assignment interaction marker
- WHEN the player presses the mobile action button
- THEN the same completion and reward behavior occurs as the keyboard interaction

#### Scenario: Completed assignment does not reward twice

- GIVEN the player already completed an assignment
- WHEN the player attempts to complete it again
- THEN XP is unchanged
- AND dialogue explains that there are no available assignments to complete

### Requirement: Deadlines Are Processed On Day Advance

The game MUST process assignment deadlines when the player sleeps into the next day.

#### Scenario: Assignment becomes overdue after due day

- GIVEN an assignment is incomplete
- AND the assignment due day is before the new current day
- WHEN the player sleeps into the next day
- THEN the assignment is marked overdue
- AND it is not available for completion rewards

#### Scenario: Missed deadline increases stress once

- GIVEN an assignment becomes overdue during sleep
- WHEN deadline processing runs
- THEN stress increases by the configured missed-deadline amount
- AND the same overdue assignment does not increase stress again on later sleeps

### Requirement: Assignment UI Does Not Break Existing Systems

The game MUST surface assignments without interfering with existing interactions.

#### Scenario: Assignment readout avoids existing UI

- GIVEN the HUD is drawn
- WHEN the assignment summary is visible
- THEN it does not overlap money, XP, schedule, energy, stress, inventory, or mobile controls

#### Scenario: Existing Library study remains intact

- GIVEN the player is near an existing Library study station
- WHEN the player presses the keyboard interaction key
- THEN the existing Library study behavior still occurs
- AND assignment completion does not trigger unless the player is near the assignment marker

## Notes

- Deadlines use `current_day`; no time-of-day clock exists yet.
- Grade standing is intentionally deferred to Ticket 024.
- Assignment data should be structured so future class, grade, and exam systems can reference assignments by stable ID.
