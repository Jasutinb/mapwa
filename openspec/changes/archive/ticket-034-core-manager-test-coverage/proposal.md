# Ticket 034: Add Basic Test Coverage for Core Managers

## Summary

Add focused, deterministic unit coverage for the core manager and state contracts that exist today, while consolidating dummy SDL configuration so pygame tests remain safe in headless CI.

## Notion Ticket

- Ticket: [Ticket 034 - Add Basic Test Coverage for Core Managers](https://app.notion.com/p/36ec34b0c90181c698a8d29137479940)
- Status at planning time: Not started
- Type: Chore
- Epic: Developer Experience
- Priority: P2
- Dependencies: Ticket 001, Ticket 002, Ticket 005, Ticket 009
- Duplicate note: an older Draft copy exists in another database; the linked page above is the canonical ticket in the current Mapwa data source.

## Current Coverage Assessment

- Inventory, skill XP, quests, and state transitions have basic happy-path coverage.
- `GameState` helper behavior is mostly exercised indirectly through `Game` integration tests.
- State-machine lifecycle, delegation, same-state no-op, and empty-machine behavior are not directly specified.
- Validation and boundary contracts for inventory, quests, and skill XP have gaps.
- Dummy SDL environment setup is repeated and, in some modules, occurs after importing pygame.

## Approved Implementation Plan

1. Add `tests/conftest.py` to set dummy SDL video and audio drivers before test-module imports.
2. Add focused `GameState` tests for independent defaults, dialogue progression, aggregate experience, and inventory/picked-item bookkeeping.
3. Expand `StateMachine` tests for enter/exit lifecycle, event/update/draw delegation, same-state no-op, and safe operation before a state is selected.
4. Expand manager edge-case coverage:
   - Inventory slot bounds, empty removal/use behavior, definition lookup, and non-unique consumables.
   - Quest validation, capped objective progress, ordered objective advancement, and one-time rewards.
   - Skill XP whitespace/boolean validation and aggregate totals.
5. Avoid production changes unless a focused test demonstrates a real defect; document and keep any approved testability seam minimal.
6. Run focused tests, Ruff, the full parallel pytest suite, and strict OpenSpec validation before publishing the PR.

## Acceptance Criteria

- [ ] Core inventory, skill XP, quest, state-machine, and `GameState` contracts have focused tests for expected behavior and relevant edge cases.
- [ ] Dummy SDL drivers are configured centrally before pygame test modules import pygame.
- [ ] Tests are deterministic and do not open a visible game window.
- [ ] State-machine lifecycle and delegation behavior are directly verified.
- [ ] `GameState` dialogue, experience, and item bookkeeping helpers are directly verified.
- [ ] No gameplay behavior, maps, controls, quests, or systems are changed by this coverage-only ticket.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] Strict OpenSpec validation passes.
- [ ] The PR includes manual and command verification evidence.
- [ ] PR and post-merge main CI/CD are green.
- [ ] The canonical Notion ticket is updated and this change is archived after merge.

## Approval Status

Approved by the user on 2026-07-13 with the instruction to proceed.

## Non-Goals

- Refactoring core managers solely for style or architecture.
- Adding new gameplay behavior, player controls, maps, quests, or systems.
- Duplicating integration scenarios already covered by feature-specific tests.
- Updating the older duplicate Draft ticket in the legacy Notion database.

## Risks and Mitigations

- **Existing tests initialize pygame inconsistently:** central dummy-driver setup runs before test collection without forcing a broad fixture rewrite.
- **Coverage-only work can become a refactor:** production files remain unchanged unless a failing contract test identifies a defect and the fix is explicitly approved.
- **Overlapping tests can slow the suite:** prefer small manager objects and lightweight fakes over additional full `Game` fixtures.
