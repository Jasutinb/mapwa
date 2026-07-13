# README Roadmap Spec

## ADDED Requirements

### Requirement: README Project Orientation

The repository MUST provide a `README.md` that lets a new player or contributor understand Mapwa and begin development without first reading implementation code.

#### Scenario: Reader understands the game

- GIVEN a reader opens the repository landing page
- WHEN they read the overview and gameplay loop
- THEN they understand that Mapwa is a student-life RPG
- AND they can identify the major resources, activities, and day progression loop

#### Scenario: Reader understands controls

- GIVEN a player wants to use the desktop or mobile build
- WHEN they read the controls table
- THEN movement, interaction, inventory, and menu controls match the implemented input paths

### Requirement: Reproducible Development Commands

The README MUST document commands that match the current Python, uv, pytest, Ruff, and pygbag configuration.

#### Scenario: Contributor runs local checks

- GIVEN dependencies are synchronized with uv
- WHEN a contributor follows the run, test, and lint instructions
- THEN the commands invoke the same entry point and checks used by the repository

#### Scenario: Contributor builds for the browser

- GIVEN a Windows development environment with project dependencies installed
- WHEN a contributor follows the preview or archive instructions
- THEN pygbag serves the local build or creates `build/web.zip` through the repository script

### Requirement: Honest Roadmap Status

The README MUST distinguish shipped capabilities from planned roadmap areas without presenting unapproved scope as complete.

#### Scenario: Reader compares current and planned work

- GIVEN a reader opens the roadmap section
- WHEN they scan implemented and planned items
- THEN shipped systems are listed separately from Tickets 036–041 themes
- AND the README explains that ticket refinement and approval remain authoritative

### Requirement: Authoritative Workflow Link

The README MUST summarize the ticket delivery loop and point contributors to `AGENTS.md` for detailed project rules.

#### Scenario: Contributor starts ticket work

- GIVEN a contributor reads the contribution section
- WHEN they need detailed development or OpenSpec instructions
- THEN they are directed to `AGENTS.md`
- AND the summarized delivery loop does not conflict with that guide

## Notes

- Canonical source: https://app.notion.com/p/36ec34b0c901813bbaa2e5415a6116cb
- Dependencies: None
