# Ticket 041: Add Grade Standing Labels and Consequences

## Summary

Make Grade Standing readable as academic reputation without expanding the persistent play HUD. The Student Planner will show a label with the existing numeric value, and Excellent Standing will earn a small, clearly explained daily academic-recognition allowance bonus.

## Notion Ticket

- Ticket: [Ticket 041 — Add Grade Standing Labels and Consequences](https://app.notion.com/p/396c34b0c9018116be44cbb41e329462)
- Status at planning time: Not started
- Type: Feature
- Epic: Academic Systems
- Priority: P2
- Dependencies: Tickets 024, 036, and 037

## Proposed Implementation Plan

1. Add a focused Grade Standing label helper in `AcademicSystem` with these inclusive bands:
   - 90–100: `Excellent Standing`
   - 80–89: `Good Standing`
   - 70–79: `Stable`
   - 60–69: `At Risk`
   - 0–59: `Probation`
2. Keep the default play HUD unchanged. Update the Student Planner’s existing Grade Standing card to show `number/100 — label`, using the helper so the label always reflects the live score.
3. Add one deterministic reward: when a player has Excellent Standing, Mom’s once-per-day allowance includes a ₱50 academic-recognition bonus and a matching dialogue line. The normal daily-allowance guard remains responsible for preventing duplicate rewards.
4. Keep all other grade bands mechanically neutral in this ticket; their label is the feedback, avoiding an unrecoverable low-grade gate or unrelated balance change.
5. Add focused boundary, Planner, allowance, and regression tests. No PC/mobile input changes or save-schema changes are required.

## Acceptance Criteria

- [ ] Grade Standing resolves to the approved label at every band boundary.
- [ ] The Planner displays both live numeric Grade Standing and its current label.
- [ ] Excellent Standing grants exactly one ₱50 recognition bonus per eligible daily allowance and explains it in Mom’s dialogue.
- [ ] Non-Excellent standing receives no recognition bonus, and the daily allowance cannot be collected twice.
- [ ] The default play HUD remains free of persistent Grade Standing details.
- [ ] Existing grade rewards, controls, rooms, quests, dialogue flow, and save schema remain compatible.
- [ ] Focused tests, Ruff, full tests, headless startup, strict OpenSpec validation, and pygbag build pass.
- [ ] PR includes verification evidence; post-merge CI/CD, Notion update, and OpenSpec archive are completed.

## Clarifications and Assumptions

- The Notion ticket lists several possible reward/consequence models but does not select one. This proposal chooses a daily allowance bonus because it is already grounded in Mom’s existing dialogue and has an existing once-per-day guard.
- “Where appropriate” means the Student Planner and grade-summary APIs; Grade Standing remains intentionally absent from the persistent HUD under Ticket 031.
- The bonus is derived solely from existing Grade Standing and the existing daily allowance guard, so no new saved state or migration is needed.

## Non-Goals

- Adding a new input, map, NPC, quest, or persistent HUD panel.
- Changing the existing Grade Standing gains/losses, course schedules, exams, or assignment rules.
- Adding a low-standing gameplay lockout that could block recovery.
- Changing the save format.

## Risks and Mitigation

- **Boundary mistakes:** table-driven threshold tests cover every transition point.
- **Duplicate allowance bonus:** reuse the existing daily-allowance guard and test repeated collection.
- **Planner layout collision:** retain the existing Grade Standing card size and verify planner layout tests.
- **Balance spillover:** only the explicit ₱50 Excellent Standing reward changes economy behavior.

## Approval Status

Approved by the user's “proceed” instruction on 2026-07-22. The implementation is limited to the explicit Excellent Standing daily-allowance bonus and the approved label presentation.
