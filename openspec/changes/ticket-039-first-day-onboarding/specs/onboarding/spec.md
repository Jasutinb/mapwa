# First-Day Academic Onboarding Spec

## ADDED Requirements

### Requirement: Contextual Tutorial Beats

The game MUST teach major academic systems through short first-day tutorial beats tied to play context.

#### Scenario: Stat explanations

- GIVEN the school-study objective is current
- WHEN the player starts studying at the school desk
- THEN the game briefly explains Energy use and recovery
- AND briefly explains Stress causes and recovery

#### Scenario: Grade Standing explanation

- GIVEN the campus-entry objective is current
- WHEN the player successfully enters campus
- THEN the game explains that academic outcomes change Grade Standing

#### Scenario: Academic deadline explanations

- GIVEN the bus objective is current
- WHEN the player first arrives in Intramuros
- THEN the game explains that the Student Planner tracks schedules, assignments, exams, and deadlines
- AND names both `P` and the mobile Planner button

#### Scenario: Tutorial beat does not repeat

- GIVEN a first-day objective has already advanced
- WHEN the player repeats the associated action
- THEN the matching tutorial dialogue is not shown again

### Requirement: Existing Quest Flow Preserved

The onboarding additions MUST preserve the existing first-day quest flow.

#### Scenario: First-day quest still completes

- GIVEN a new player follows the first-day quest
- WHEN onboarding beats are shown
- THEN quest objectives still advance and complete as before
- AND the existing quest reward is granted once

#### Scenario: Planner handoff

- GIVEN the Student Planner is available
- WHEN schedule or deadline information is introduced
- THEN the player is directed to the planner instead of relying on persistent HUD clutter

## Notes

- Source: https://app.notion.com/p/396c34b0c90181e8a5e1ca9d210e22bb
- Dependencies: Ticket 018, Ticket 019, Ticket 020, Ticket 021, Ticket 022, Ticket 023, Ticket 024, Ticket 036
