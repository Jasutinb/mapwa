# Core Manager Test Coverage Spec

## ADDED Requirements

### Requirement: Focused Core Contract Coverage

The project MUST directly test important contracts for the core managers and state containers that exist in the current codebase.

#### Scenario: GameState helpers are isolated and predictable

- GIVEN two newly created `GameState` instances
- WHEN dialogue, skill XP, quest, assignment, exam, or item state changes on one instance
- THEN mutable defaults remain isolated and helper methods produce deterministic state transitions

#### Scenario: State-machine lifecycle is preserved

- GIVEN registered states with observable lifecycle and delegation hooks
- WHEN the active state changes or receives events, updates, and draws
- THEN enter, exit, and delegated methods run exactly when expected
- AND selecting the current state again is a no-op
- AND an empty state machine safely ignores delegated operations

#### Scenario: Manager boundaries are enforced

- GIVEN inventory, quest, and skill XP manager inputs at valid and invalid boundaries
- WHEN add, remove, use, advance, lookup, or reward operations run
- THEN valid operations return deterministic results
- AND invalid operations fail using the manager's documented exception or no-op contract

### Requirement: Headless Pygame Test Safety

The test suite MUST configure dummy SDL video and audio drivers before pygame-based test modules are imported.

#### Scenario: Test suite runs without a visible window

- GIVEN pytest runs locally or in CI without a graphical or audio device
- WHEN pygame-based tests are collected and executed
- THEN dummy SDL drivers are already configured
- AND the suite does not require or open a visible game window

### Requirement: Coverage-Only Scope

Ticket 034 MUST preserve current gameplay behavior.

#### Scenario: Tests expose no production defect

- GIVEN the new focused tests pass against the current implementation
- WHEN the ticket is completed
- THEN no production source file is changed

#### Scenario: A test exposes a production defect

- GIVEN a focused contract test demonstrates an existing defect
- WHEN a production fix is considered
- THEN work pauses for explicit approval of the minimal fix before production code changes

## Notes

- Canonical source: https://app.notion.com/p/36ec34b0c90181c698a8d29137479940
- Dependencies: Ticket 001, Ticket 002, Ticket 005, Ticket 009
