# Grade Standing Labels and Consequences Spec

## ADDED Requirements

### Requirement: Standing Labels

The game MUST translate numeric Grade Standing into readable academic standing labels.

#### Scenario: Label thresholds

- GIVEN Grade Standing is 90-100, 80-89, 70-79, 60-69, or below 60
- WHEN the label is requested
- THEN the game returns Excellent Standing, Good Standing, Stable, At Risk, or Probation respectively

#### Scenario: Display label with number

- GIVEN Grade Standing is displayed in the planner or another appropriate surface
- WHEN the value is shown
- THEN the player sees both the numeric value and readable label

#### Scenario: Planner uses the live label

- GIVEN the Grade Standing value changes after an academic action
- WHEN the player opens the Student Planner
- THEN the Grade Standing card shows the updated `number/100 — label` value

### Requirement: Meaningful Consequence or Reward

The game MUST connect at least one Grade Standing band to a reward, consequence, eligibility gate, or grounded dialogue response.

#### Scenario: Band effect applies

- GIVEN the player reaches the configured Grade Standing band
- WHEN the related opportunity, reward, consequence, or dialogue is evaluated
- THEN the band-specific effect is applied clearly and deterministically

#### Scenario: Excellent Standing recognition allowance

- GIVEN the player has Grade Standing from 90 through 100 and has not received today's allowance
- WHEN they complete Mom's allowance dialogue
- THEN they receive the normal ₱250 allowance plus a ₱50 academic-recognition bonus exactly once for that day

#### Scenario: Non-Excellent allowance remains unchanged

- GIVEN the player has Grade Standing below 90
- WHEN they complete Mom's allowance dialogue
- THEN they receive only the normal ₱250 allowance

#### Scenario: Threshold tests

- GIVEN Grade Standing is at or near each threshold
- WHEN labels and band effects are evaluated
- THEN boundary behavior is correct and stable

## Notes

- Source: https://app.notion.com/p/396c34b0c9018116be44cbb41e329462
- Dependencies: Ticket 024, Ticket 036, Ticket 037
