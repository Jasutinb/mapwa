# Ticket 035: Create README Roadmap Section

## Summary

Update README with a clear overview of the game and current roadmap.

## Notion Ticket

- Ticket: [Ticket 035 - Create README Roadmap Section](https://app.notion.com/p/36ec34b0c901813bbaa2e5415a6116cb)
- Status at planning time: Not started
- Type: Documentation
- Epic: Developer Experience
- Dependencies:
- None

## Acceptance Criteria

- [ ] README explains the current game concept and student RPG loop.
- [ ] README lists implemented and planned roadmap areas at a high level.
- [ ] Setup, run, test, and web build commands stay accurate.
- [ ] Documentation does not conflict with AGENTS.md or OpenSpec workflow.
- [ ] Markdown renders cleanly.
- [ ] Focused tests cover the ticket behavior where applicable.
- [ ] PC controls and mobile controls have parity when player-facing input changes.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] PR includes manual and command verification steps.
- [ ] Post-merge main CI/CD is green.
- [ ] Notion ticket is updated.

## Proposed Implementation

- Update README with the current Mapwa premise, core gameplay loop, and project status.
- Add a concise roadmap section that distinguishes implemented systems from planned tickets.
- Verify setup, run, test, hot refresh, and web build commands against the current repo files.
- Keep AGENTS.md and OpenSpec workflow details authoritative; the README should summarize and link/point rather than duplicate every rule.

## Approval Status

This OpenSpec proposal captures the current ticket plan before coding. Confirm the implementation plan with the user before creating the ticket branch and changing game code.

## Non-Goals

- Do not bundle unrelated roadmap tickets into this work.
- Do not refactor broad Game behavior unless the ticket explicitly calls for it.
- Do not add PC-only player-facing controls.

## Risks

- Player-facing changes may need mobile parity updates in src/mobile_controls.py.
- UI changes can overlap dialogue, inventory, location text, or mobile controls if layout is not measured.
- Gameplay/system changes can regress existing room transitions, academic state, or pygbag compatibility.