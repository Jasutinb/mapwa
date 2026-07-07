# Core Manager Test Coverage Spec

## ADDED Requirements

### Requirement: Core Manager Regression Coverage

The project MUST add focused automated tests for important core manager and state contracts that are not already protected by gameplay tests.

#### Scenario: Manager behavior covered

- GIVEN a core manager or extracted system exists in the codebase
- WHEN behavior such as add, remove, update, transition, or reward application is important to gameplay
- THEN focused tests cover the expected behavior and at least one relevant edge case

#### Scenario: Headless pygame safety

- GIVEN a test imports or initializes pygame
- WHEN the test runs in CI or another headless environment
- THEN dummy SDL video and audio drivers are configured before pygame initialization

#### Scenario: No broad refactor required

- GIVEN the ticket is for coverage
- WHEN tests are added
- THEN production refactors are avoided unless a small approved testability seam is required

## Notes

- Source: https://app.notion.com/p/36ec34b0c90181c698a8d29137479940
- Dependencies: Ticket 001, Ticket 002, Ticket 005, Ticket 009