# Grade Standing Rewards Spec

## ADDED Requirements

### Requirement: Positive Academic Outcomes

The game MUST increase Grade Standing for meaningful positive academic behavior.

#### Scenario: Attend class on time

- GIVEN the player successfully attends an eligible class on time
- WHEN the class attendance reward is applied
- THEN Grade Standing increases by 1 exactly once
- AND feedback reports the actual applied increase

#### Scenario: Submit assignment

- GIVEN the player submits an active assignment
- WHEN assignment rewards are applied
- THEN Grade Standing increases by 3 exactly once
- AND feedback reports the actual applied increase

#### Scenario: Early submission bonus

- GIVEN an active assignment is submitted before its due day
- WHEN the assignment is submitted early
- THEN Grade Standing receives an additional 1-point bonus exactly once

#### Scenario: Submission on due day

- GIVEN an active assignment is submitted on its due day
- WHEN assignment rewards are applied
- THEN Grade Standing increases by 3
- AND no early-submission bonus is applied

### Requirement: Grade Standing Bounds

The game MUST keep Grade Standing between 0 and 100 and report actual applied changes.

#### Scenario: Positive reward reaches maximum

- GIVEN a positive academic reward would raise Grade Standing above 100
- WHEN the reward is applied
- THEN Grade Standing is clamped to 100
- AND feedback reports only the points actually applied

### Requirement: Balanced Penalties

The game MUST keep meaningful penalties for failed exams and missed assignments without double-applying outcomes.

#### Scenario: Exam failure penalty

- GIVEN the player fails an exam attempt
- WHEN the result is applied
- THEN Grade Standing decreases by 6 once for that result

#### Scenario: Missed assignment penalty

- GIVEN an assignment becomes missed
- WHEN missed-assignment processing runs
- THEN Grade Standing decreases by 5 once

## Notes

- Source: https://app.notion.com/p/396c34b0c90181689079c862bb954953
- Approved values: class +1, submitted assignment +3, early bonus +1, passed exam +5, failed exam -6, missed assignment -5.
- Dependencies: Ticket 021, Ticket 022, Ticket 023, Ticket 024
