# Split Game Responsibilities Spec

## ADDED Requirements

### Requirement: Focused Systems

The codebase MUST reduce Game class responsibilities by extracting cohesive systems while preserving player-facing behavior.

#### Scenario: Academic logic extracted

- GIVEN class attendance, assignments, exams, and Grade Standing behavior exists
- WHEN AcademicSystem or equivalent boundaries are introduced
- THEN those behaviors remain available through a focused API and existing gameplay still works

#### Scenario: HUD rendering extracted

- GIVEN HUD drawing currently lives in Game
- WHEN HUDRenderer or equivalent boundaries are introduced
- THEN HUD layout/rendering can be tested or reasoned about independently from the main loop

#### Scenario: Interaction and room setup boundaries

- GIVEN Game currently handles interactions and room creation
- WHEN InteractionSystem and RoomFactory or data-driven room definitions are introduced
- THEN existing room transitions, prompts, NPCs, and interactables keep working

### Requirement: Behavior Preservation

The refactor MUST avoid unrelated gameplay changes.

#### Scenario: Regression behavior

- GIVEN existing movement, rooms, NPC interaction, transport, academic actions, inventory, and mobile controls
- WHEN the refactor is complete
- THEN those behaviors remain equivalent unless a linked ticket explicitly changes them

#### Scenario: WASM loop preserved

- GIVEN the game runs in pygbag/WebAssembly
- WHEN the async loop is refactored or touched
- THEN browser-friendly yielding and startup behavior are preserved

## Notes

- Source: https://app.notion.com/p/396c34b0c90181369f46d2b92b422a34
- Dependencies: Ticket 018, Ticket 019, Ticket 020, Ticket 021, Ticket 022, Ticket 023, Ticket 024, Ticket 031, Ticket 032, Ticket 036