# Browser Save and Load Spec

## ADDED Requirements

### Requirement: GameState Serialization

The game MUST serialize and deserialize the central GameState using a stable, versioned format.

#### Scenario: Round-trip state

- GIVEN a GameState with room, money, stats, quests, assignments, exams, and inventory data
- WHEN it is serialized and deserialized
- THEN the restored state matches the saved values for supported fields

### Requirement: Persistence Targets

The game MUST support persistence in desktop development runs and SHOULD persist across browser refreshes where pygbag/browser storage is available.

#### Scenario: Desktop save and load

- GIVEN the player saves during a desktop run
- WHEN the player loads that save
- THEN the saved GameState is restored without crashing

#### Scenario: Browser refresh survival

- GIVEN browser storage is available in the web build
- WHEN the player saves and refreshes the page
- THEN loading restores the saved progress

### Requirement: Safe Failure

Loading MUST fail gracefully for missing, corrupt, or incompatible saves.

#### Scenario: Missing or corrupt save

- GIVEN no valid save exists
- WHEN load is requested
- THEN the game continues with a safe new or current state and provides clear feedback if needed

### Requirement: Save and Load Controls

The game MUST expose save and load actions through the pause menu, and mobile players MUST be able to reach the same menu and actions.

#### Scenario: Desktop pause menu

- GIVEN the player is using desktop controls
- WHEN the player opens the pause menu
- THEN Save Game and Load Game actions are available

#### Scenario: Mobile pause menu

- GIVEN the player is using mobile controls
- WHEN the player taps the Menu control and navigates with the mobile controls
- THEN the same Save Game and Load Game actions are available

## Notes

- Source: https://app.notion.com/p/36ec34b0c901815799a3dc25fa008b52
- Dependencies: Ticket 001, Ticket 002, Ticket 004, Ticket 005, Ticket 009, Ticket 018, Ticket 019, Ticket 020, Ticket 022, Ticket 023, Ticket 024
