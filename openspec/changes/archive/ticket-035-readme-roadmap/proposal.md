# Ticket 035: Create README Roadmap Section

## Summary

Create the repository's first `README.md` with an accurate contributor-facing overview of Mapwa, its gameplay loop, controls, development commands, browser build, project structure, roadmap, and ticket workflow.

## Notion Ticket

- Ticket: [Ticket 035 - Create README Roadmap Section](https://app.notion.com/p/36ec34b0c901813bbaa2e5415a6116cb)
- Status at planning time: Not started
- Type: Documentation
- Epic: Developer Experience
- Priority: P2
- Dependencies: None
- Duplicate note: an older Draft copy exists in another database; the linked page above is the canonical ticket in the current Mapwa data source.

## Current Documentation Assessment

- The repository has no `README.md`.
- `AGENTS.md` contains authoritative development and workflow rules but is too detailed to serve as the project landing page.
- `pyproject.toml`, repository scripts, and `.github/workflows/ci-cd.yml` define the current setup, test, build, and deployment commands.
- Active OpenSpec changes identify Tickets 036–041 as the next planned roadmap areas.

## Approved Implementation Plan

1. Add `README.md` with the current game premise and a concise student-life gameplay loop.
2. Document desktop and mobile controls using the parity implemented in the current codebase.
3. Document Python/uv setup, local run, hot refresh, lint, tests, pygbag preview, and Windows archive build commands verified against repository configuration.
4. Add a roadmap that clearly separates implemented systems from planned work represented by Tickets 036–041.
5. Summarize the project structure and ticket delivery loop while pointing to `AGENTS.md` as the authoritative development guide.
6. Manually inspect Markdown structure and links, then run Ruff, the full parallel pytest suite, and strict OpenSpec validation.

## Acceptance Criteria

- [ ] `README.md` explains the current Mapwa concept and student RPG loop.
- [ ] Desktop and mobile controls match the implemented input paths.
- [ ] Implemented and planned roadmap areas are clearly distinguished.
- [ ] Setup, run, hot-refresh, lint, test, web-preview, and archive-build commands match current repository tooling.
- [ ] Documentation does not conflict with `AGENTS.md` or the OpenSpec workflow.
- [ ] Markdown headings, tables, code blocks, and repository links render cleanly.
- [ ] No gameplay or production code changes are included.
- [ ] `uv run ruff check .` passes.
- [ ] `uv run pytest -n auto` passes.
- [ ] Strict OpenSpec validation passes.
- [ ] PR and post-merge main CI/CD are green.
- [ ] The canonical Notion ticket is updated and this change is archived after merge.

## Approval Status

Approved by the user on 2026-07-13 with the instruction to proceed.

## Non-Goals

- Duplicating every rule from `AGENTS.md`.
- Promising dates or features beyond the currently planned ticket set.
- Changing gameplay, controls, deployment configuration, or project tooling.
- Updating the older duplicate Draft ticket in the legacy Notion database.

## Risks and Mitigations

- **Commands drift from the codebase:** derive them from `pyproject.toml`, scripts, and CI rather than memory.
- **Roadmap becomes a promise:** describe planned areas at a high level and state that approved tickets remain authoritative.
- **README duplicates policy:** keep policy details in `AGENTS.md` and link to it.
