# Classes Spec

## Requirements

### Requirement: Attend Scheduled Classes

The game MUST allow the player to attend classes that are scheduled for the current day and current room.

#### Scenario: Attend scheduled class in matching room

- GIVEN the current day has a scheduled class for the player's current room
- AND the player is near the class attendance interaction spot
- AND the class has not been attended today
- WHEN the player presses the keyboard interaction key
- THEN the class is marked attended for the current day
- AND the class skill receives the configured attendance XP
- AND dialogue confirms the class attended and XP gained

#### Scenario: Attend class through mobile action

- GIVEN the current day has a scheduled class for the player's current room
- AND the player is near the class attendance interaction spot
- AND the class has not been attended today
- WHEN the player presses the mobile action button
- THEN the same attendance and XP behavior occurs as the keyboard interaction

### Requirement: Attendance Rewards Are Once Per Class Per Day

The game MUST prevent duplicate attendance rewards for the same scheduled class on the same day.

#### Scenario: Duplicate attendance is blocked

- GIVEN the player already attended a scheduled class today
- AND the player is near the same class attendance interaction spot
- WHEN the player attempts to attend again
- THEN XP is unchanged
- AND the attended class tracking is unchanged
- AND dialogue explains that the class was already attended today

#### Scenario: Sleeping opens the next day's attendance

- GIVEN the player attended a class today
- WHEN the player sleeps into the next day
- THEN the new day has no attended classes yet
- AND the player can attend a scheduled class for the new day

### Requirement: Wrong Room Or Free Day Blocks Attendance

The game MUST not grant attendance when no scheduled class is available for the current room and day.

#### Scenario: No class scheduled in this room today

- GIVEN the current day has no scheduled class for the player's current room
- AND the player is near a class attendance interaction spot
- WHEN the player attempts to attend class
- THEN XP is unchanged
- AND no class is marked attended
- AND dialogue explains that no class is scheduled here today

#### Scenario: Free day has no attendance

- GIVEN the current day has no scheduled classes
- AND the player is near a class attendance interaction spot
- WHEN the player attempts to attend class
- THEN XP is unchanged
- AND no class is marked attended
- AND dialogue explains that there are no classes today

### Requirement: Existing Study And Practice Interactions Remain Intact

The game MUST preserve existing learning interactions while adding class attendance.

#### Scenario: Existing study station still studies

- GIVEN the player is near an existing study or practice station
- WHEN the player presses the keyboard interaction key
- THEN the existing study or practice behavior still occurs
- AND class attendance does not trigger unless the player is near the class attendance spot

## Notes

- Ticket 020 owns schedule data and weekday lookup. This ticket should consume those helpers and avoid duplicating weekly schedule definitions.
- No time-of-day simulation exists yet, so attendance is limited to scheduled class/day/room validation.
- Future grade standing, assignment, and exam tickets may depend on the attendance tracking added here.
