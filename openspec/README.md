# OpenSpec Workflow

OpenSpec is used here as the lightweight planning record for Mapwa tickets.
Notion remains the source of ticket status, and GitHub remains the source of PR
review, CI/CD, and merge history.

## Folder Layout

```text
openspec/
  config.yaml
  changes/
    ticket-000-short-name/
      proposal.md
      tasks.md
      specs/
        feature-area/
          spec.md
    archive/
  specs/
  templates/
    proposal.md
    tasks.md
    spec.md
```

## Ticket Flow

1. Fetch the Notion ticket and summarize it.
2. Create a change folder under `openspec/changes/ticket-000-short-name/`.
3. Copy the templates from `openspec/templates/`.
4. Fill in the proposal and wait for approval before coding.
5. Implement the ticket on a dedicated branch/worktree.
6. Run focused tests, `uv run ruff check .`, and `uv run pytest -n auto`.
7. Open one PR for the ticket and add manual plus command verification steps.
8. Merge after PR CI/CD is green.
9. Confirm post-merge main CI/CD is green.
10. Update Notion and move the change folder to `openspec/changes/archive/`.

## Naming

Use the ticket number and a short kebab-case title:

```text
openspec/changes/ticket-015-electronics-lab/
```

Use matching Git branch names:

```text
codex/ticket-015-electronics-lab
```
