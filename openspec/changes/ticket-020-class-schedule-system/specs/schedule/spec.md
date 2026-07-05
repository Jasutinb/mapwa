# Schedule Spec

## Requirements

### Requirement: Weekly Class Schedule Data

The game MUST define a simple weekly class schedule that can be queried by day.

#### Scenario: Class entries have required display fields

- GIVEN the weekly schedule is loaded
- WHEN class entries are inspected
- THEN each entry includes a course name
- AND each entry includes a weekday
- AND each entry includes start and end labels
- AND each entry includes a room or location label
- AND each entry includes a skill or category

#### Scenario: School days return classes in order

- GIVEN the current day maps to a school weekday with scheduled classes
- WHEN today's classes are requested
- THEN the game returns the class entries for that weekday
- AND the entries are returned in display order

#### Scenario: Free days return no classes

- GIVEN the current day maps to a configured free day
- WHEN today's classes are requested
- THEN the game returns an empty list
- AND the schedule summary says there are no classes today

### Requirement: Weekday Derives From Current Day

The game MUST derive the weekday from the existing day counter.

#### Scenario: Day one starts on Monday

- GIVEN the game starts on day 1
- WHEN the weekday is requested
- THEN the weekday is Monday

#### Scenario: Sleeping advances the schedule day

- GIVEN the game is on day 1
- WHEN the player sleeps into the next day
- THEN the game is on day 2
- AND the schedule weekday is Tuesday
- AND existing sleep side effects still occur

#### Scenario: Weekday cycles after Sunday

- GIVEN the game advances past Sunday
- WHEN the weekday is requested
- THEN the weekday cycles back to Monday

### Requirement: Schedule Summary Is Visible

The game MUST show a compact schedule readout without interfering with existing UI.

#### Scenario: School day readout

- GIVEN the current day has scheduled classes
- WHEN the HUD is drawn
- THEN the readout shows the current day or weekday
- AND it shows a concise class summary
- AND it does not overlap money, XP, energy, stress, inventory, or mobile controls

#### Scenario: Free day readout

- GIVEN the current day has no scheduled classes
- WHEN the HUD is drawn
- THEN the readout shows the current day or weekday
- AND it shows that there are no classes today

## Notes

- This ticket creates the schedule foundation only. Ticket 021 owns the attend-class interaction and any rewards, penalties, or validation based on being in the correct room.
- Because there is no time-of-day clock yet, class times are labels for display and future logic, not a simulated clock.
- The schedule should be deterministic and covered by tests so later progression systems can depend on it.
