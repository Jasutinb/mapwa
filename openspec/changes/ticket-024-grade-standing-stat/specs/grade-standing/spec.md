# Grade Standing Spec

## Requirements

### Requirement: Grade Standing State

The system MUST store a bounded Grade Standing stat that represents current academic performance.

The stat MUST use a 0 to 100 numeric scale and start at 75.

#### Scenario: Initial grade standing

- GIVEN a new game state
- WHEN grade standing is inspected
- THEN it starts at the configured default value

#### Scenario: Grade standing is clamped

- GIVEN grade standing is near its minimum or maximum
- WHEN a change would move it beyond the allowed bounds
- THEN the stored value is clamped within the configured range

### Requirement: Academic Outcomes Affect Grade Standing

The system MUST update grade standing from important academic outcomes.

#### Scenario: Passed exam increases grade standing

- GIVEN the player passes an exam
- WHEN the exam result is applied
- THEN grade standing increases by 5

#### Scenario: Failed exam decreases grade standing

- GIVEN the player fails an exam
- WHEN the exam result is applied
- THEN grade standing decreases by 8

#### Scenario: Missed assignment decreases grade standing

- GIVEN an assignment becomes missed when the day advances
- WHEN the missed result is first applied
- THEN grade standing decreases by 5 for that assignment

#### Scenario: No double application

- GIVEN a passed exam or missed assignment has already changed grade standing
- WHEN the player retries the same interaction or sleeps again
- THEN grade standing does not change again from that same result

### Requirement: Persistence

The system MUST preserve grade standing across ordinary play state transitions.

#### Scenario: Room changes preserve grade standing

- GIVEN the player changes rooms
- WHEN the transition completes
- THEN the current grade standing value is unchanged

#### Scenario: Sleeping preserves grade standing

- GIVEN grade standing has changed
- WHEN the player sleeps and the day advances
- THEN the stored grade standing value persists apart from any newly triggered missed-assignment penalty

### Requirement: Grade Standing Feedback

The system MUST communicate meaningful grade-standing changes to the player.

#### Scenario: Positive feedback after improvement

- GIVEN grade standing increases
- WHEN the relevant result dialogue is shown
- THEN the player can understand that grade standing improved

#### Scenario: Negative feedback after decline

- GIVEN grade standing decreases
- WHEN the relevant result dialogue is shown
- THEN the player can understand that grade standing declined

### Requirement: Grade Standing HUD

The system MUST render grade standing without overlapping existing UI.

#### Scenario: HUD line is visible

- GIVEN the game is drawn
- WHEN the HUD is rendered
- THEN grade standing is shown below the exam summary in the visible player stat area

#### Scenario: HUD avoids existing UI

- GIVEN the game is drawn on the default viewport
- WHEN the grade-standing HUD rectangle is measured
- THEN it does not overlap schedule, assignment, exam, energy, stress, inventory, or mobile action controls

## Notes

- The first version should favor clarity and deterministic behavior over realism.
- Ticket 024 should build on assignments and exams, not replace their existing rewards or penalties.
