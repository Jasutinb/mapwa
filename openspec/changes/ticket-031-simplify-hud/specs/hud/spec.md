# Simplified HUD Spec

## ADDED Requirements

### Requirement: Urgent HUD Only

The default play HUD MUST show only urgent moment-to-moment state: Energy, Stress, current objective, and money.

#### Scenario: Default HUD renders urgent state

- GIVEN the game is in the default play view
- WHEN the HUD is drawn
- THEN Energy, Stress, current objective, and money are visible in a compact layout

#### Scenario: Planner-owned details are not persistent

- GIVEN schedule, assignments, exams, and Grade Standing exist
- WHEN the default play HUD is drawn
- THEN those non-urgent academic details are not permanently rendered in the play view

### Requirement: Layout Safety

The simplified HUD MUST avoid overlapping player controls and feedback surfaces.

#### Scenario: HUD avoids other UI

- GIVEN the game is drawn on the default viewport
- WHEN HUD, dialogue, inventory, location text, and mobile controls are measured or visually inspected
- THEN the urgent HUD does not overlap those UI elements incoherently

## Notes

- Source: https://app.notion.com/p/36ec34b0c9018198b168f0d0a3cab854
- Dependencies: Ticket 018, Ticket 019, Ticket 024