# Ticket 040: Split Game Responsibilities Into Systems

## Summary

Reduce the 1,889-line `Game` class by extracting focused systems while preserving all current player-facing behavior and the public `Game` API used by states and tests.

## Notion Ticket

- Ticket: [Ticket 040 — Split Game Responsibilities Into Systems](https://app.notion.com/p/396c34b0c90181369f46d2b92b422a34)
- Status at planning time: Not started
- Type: Chore
- Epic: Core Architecture
- Priority: P2
- Dependencies: Tickets 018, 019, 020, 021, 022, 023, 024, 031, 032, and 036

## Approved Implementation Plan

### Phase 1: Focused composition boundaries

- Add an `AcademicSystem` that owns schedule queries, assignment completion and deadlines, exam readiness/resolution, class attendance, and Grade Standing mutations.
- Add an `InteractionSystem` that owns proximity checks and resolves the shared PC/mobile action request in priority order.
- Add a `RoomFactory` that owns the room graph and current-room builder dispatch while retaining existing room-builder behavior.
- Keep the existing `SaveSystem` as the serialization/storage boundary; `Game.save_game()` and `Game.load_game()` remain compatibility-facing orchestration methods.

### Phase 2: HUD extraction

- Add a `HUDRenderer` that owns HUD text fitting, panel drawing, urgent/planner rectangle clearing, urgent-state rendering, location rendering, inventory/mobile-control rendering, and the display flip.
- Preserve the existing HUD rectangle attributes on `Game` because tests and other collaborators use them as observable layout state.

### Phase 3: Compatibility and verification

- Retain existing public methods on `Game` as thin delegates where states/tests already call them.
- Add focused unit tests proving each system boundary is instantiated and delegated behavior remains observable through `Game`.
- Run relevant academic, HUD, interaction, room, save, mobile-control, and state regression tests before the full suite.
- Run Ruff, the full test suite, headless startup, strict OpenSpec validation, and the pygbag web archive build.

## Acceptance Criteria

- [ ] `Game` delegates academic behavior to a focused `AcademicSystem`.
- [ ] `Game` delegates HUD layout and drawing details to a focused `HUDRenderer`.
- [ ] PC `E` and mobile action-button interaction resolution share one `InteractionSystem` path with unchanged priority.
- [ ] Room graph creation and room-builder selection are owned by `RoomFactory` without changing room contents or transitions.
- [ ] Existing `SaveSystem` behavior and serialized schema remain unchanged.
- [ ] Existing movement, rooms, NPC interaction, transport, academic actions, inventory, and mobile controls still work.
- [ ] Pygbag/WASM async yielding and startup behavior remain unchanged.
- [ ] No gameplay values, rewards, costs, schedules, map layouts, controls, or quest behavior change.
- [ ] Focused and full regression tests pass.
- [ ] `uv run ruff check .` passes.
- [ ] PR includes verification evidence and post-merge CI/CD is green.
- [ ] Notion is updated and this change is archived after merge.

## Clarifications and Assumptions

- “Extract” means composition with compatibility delegates, not a breaking public-API redesign. This keeps the refactor reviewable and avoids rewriting all states/tests in the same ticket.
- Room layout methods remain behavior-identical; this ticket moves room graph/dispatch responsibility rather than converting every map into a new data format.
- Save-system preparation is already satisfied by the dedicated `src/save_system.py` boundary from Ticket 032. No persistence-format migration is needed.
- No player-facing input changes are planned, so mobile parity requires regression verification rather than new controls.

## Non-Goals

- Gameplay balance, dialogue, quests, schedules, room layouts, and HUD redesign.
- Save-schema changes or migration logic.
- Removing every `Game` compatibility method in one large breaking refactor.
- Unrelated cleanup outside the extracted responsibilities.

## Risks and Mitigations

- **Circular dependencies:** systems receive the `Game` instance and avoid importing `Game` at runtime.
- **Interaction priority regressions:** preserve the current ordered action chain and test both keyboard and mobile paths.
- **HUD layout regressions:** preserve `Game` rectangle observables and run the existing overlap/layout suite.
- **Room regressions:** keep room-builder methods unchanged and test graph links, room creation, and transitions.
- **WASM regressions:** leave the async loop unchanged and verify a pygbag archive build.

## Approval Status

Approved by the user’s “proceed” instruction on 2026-07-14 after the canonical Notion ticket and proposed system boundaries were summarized.
