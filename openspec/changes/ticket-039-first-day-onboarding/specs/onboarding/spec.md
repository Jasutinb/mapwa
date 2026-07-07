# First-Day Academic Onboarding Spec

## ADDED Requirements

### Requirement: Contextual Tutorial Beats

The game MUST teach major academic systems through short first-day tutorial beats tied to play context.

#### Scenario: Stat explanations

- GIVEN the player first encounters Energy, Stress, or Grade Standing relevance
- WHEN the tutorial beat triggers
- THEN the game briefly explains the stat without blocking normal play longer than necessary

#### Scenario: Academic deadline explanations

- GIVEN assignments, exams, or deadlines become relevant
- WHEN the player reaches that first-day moment
- THEN the game explains the concept and how to check related information

### Requirement: Existing Quest Flow Preserved

The onboarding additions MUST preserve the existing first-day quest flow.

#### Scenario: First-day quest still completes

- GIVEN a new player follows the first-day quest
- WHEN onboarding beats are shown
- THEN quest objectives still advance and complete as before

#### Scenario: Planner handoff

- GIVEN the Student Planner is available
- WHEN schedule or deadline information is introduced
- THEN the player is directed to the planner instead of relying on persistent HUD clutter

## Notes

- Source: https://app.notion.com/p/396c34b0c90181e8a5e1ca9d210e22bb
- Dependencies: Ticket 018, Ticket 019, Ticket 020, Ticket 021, Ticket 022, Ticket 023, Ticket 024, Ticket 036