# Grade Standing Rewards Spec

## ADDED Requirements

### Requirement: Positive Academic Outcomes

The game MUST increase Grade Standing for meaningful positive academic behavior.

#### Scenario: Attend class on time

- GIVEN the player successfully attends an eligible class on time
- WHEN the class attendance reward is applied
- THEN Grade Standing increases by the configured class-attendance amount

#### Scenario: Submit assignment

- GIVEN the player submits an active assignment
- WHEN assignment rewards are applied
- THEN Grade Standing increases by the configured submission amount

#### Scenario: Early submission bonus

- GIVEN the assignment system can determine the submission is before the due date
- WHEN the assignment is submitted early
- THEN Grade Standing receives the configured early bonus once

### Requirement: Balanced Penalties

The game MUST keep meaningful penalties for failed exams and missed assignments without double-applying outcomes.

#### Scenario: Exam failure penalty

- GIVEN the player fails an exam attempt
- WHEN the result is applied
- THEN Grade Standing decreases by the configured failure amount once for that result

#### Scenario: Missed assignment penalty

- GIVEN an assignment becomes missed
- WHEN missed-assignment processing runs
- THEN Grade Standing decreases by the configured missed amount once

## Notes

- Source: https://app.notion.com/p/396c34b0c90181689079c862bb954953
- Suggested values: class +1, submitted assignment +3, early bonus +1, passed exam +5, failed exam -6 or -8, missed assignment -5.
- Dependencies: Ticket 021, Ticket 022, Ticket 023, Ticket 024