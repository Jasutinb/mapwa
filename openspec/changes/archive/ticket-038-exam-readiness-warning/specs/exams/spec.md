# Exam Readiness Warning Spec

## ADDED Requirements

### Requirement: Readiness Warning

The game MUST show the exam title, relevant skill, recommended XP, and current XP before an exam attempt is committed.

#### Scenario: Risky attempt warning

- GIVEN the player has less than the recommended readiness for an exam
- WHEN the player attempts the exam
- THEN the game shows current and recommended XP
- AND warns that the attempt is risky
- AND requires the player to select “Take Exam” before mechanics are applied

#### Scenario: Ready attempt clarity

- GIVEN the player meets or exceeds recommended readiness
- WHEN the player attempts the exam
- THEN the game shows current and recommended XP
- AND communicates that the recommendation is met
- AND waits for “Take Exam” or “Cancel” selection

### Requirement: Confirmation Is Binding

The player MUST be able to confirm or cancel a risky exam attempt without hidden penalties.

#### Scenario: Cancel risky attempt

- GIVEN the readiness warning is open
- WHEN the player cancels
- THEN no Energy is spent, Stress does not increase, Grade Standing does not change, and no exam result is recorded
- AND the pending exam is cleared
- AND play resumes

#### Scenario: Confirm risky attempt

- GIVEN the readiness warning is open
- WHEN the player confirms
- THEN the existing exam attempt mechanics run exactly once
- AND the pending exam is cleared

#### Scenario: Mobile parity

- GIVEN the readiness warning is open on mobile
- WHEN the player uses the mobile joystick and action button
- THEN the same confirm/cancel behavior applies

## Notes

- Source: https://app.notion.com/p/396c34b0c9018131a9a7fb3a1c922548
- Dependencies: Ticket 018, Ticket 019, Ticket 023, Ticket 024
