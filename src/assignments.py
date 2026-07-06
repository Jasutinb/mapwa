from dataclasses import dataclass

from src.config import (
    ASSIGNMENT_REWARD_XP,
    SKILL_ACADEMICS,
    SKILL_MATH,
    SKILL_PROGRAMMING,
)


ASSIGNMENT_STATUS_ACTIVE = "active"
ASSIGNMENT_STATUS_COMPLETED = "completed"
ASSIGNMENT_STATUS_MISSED = "missed"


@dataclass
class Assignment:
    assignment_id: str
    title: str
    skill: str
    assigned_day: int
    due_day: int
    reward_xp: int
    status: str = ASSIGNMENT_STATUS_ACTIVE
    missed_stress_applied: bool = False

    @property
    def is_active(self):
        return self.status == ASSIGNMENT_STATUS_ACTIVE

    def is_available(self, day):
        return self.is_active and self.assigned_day <= day <= self.due_day

    def is_overdue_on(self, day):
        return self.is_active and self.due_day < day

    def summary_label(self):
        return f"{self.title} due Day {self.due_day}"


def create_initial_assignments():
    return [
        Assignment(
            "academics-reflection",
            "Academics Reflection",
            SKILL_ACADEMICS,
            assigned_day=1,
            due_day=2,
            reward_xp=ASSIGNMENT_REWARD_XP,
        ),
        Assignment(
            "programming-practice-sheet",
            "Programming Practice Sheet",
            SKILL_PROGRAMMING,
            assigned_day=2,
            due_day=4,
            reward_xp=ASSIGNMENT_REWARD_XP,
        ),
        Assignment(
            "math-problem-set",
            "Math Problem Set",
            SKILL_MATH,
            assigned_day=3,
            due_day=5,
            reward_xp=ASSIGNMENT_REWARD_XP,
        ),
    ]


def available_assignments(assignments, day):
    return sorted(
        (assignment for assignment in assignments if assignment.is_available(day)),
        key=lambda assignment: (assignment.due_day, assignment.assigned_day),
    )


def next_due_assignment(assignments, day):
    active_assignments = [
        assignment
        for assignment in assignments
        if assignment.is_active and assignment.assigned_day <= day
    ]
    if not active_assignments:
        return None
    return min(active_assignments, key=lambda assignment: assignment.due_day)


def assignment_summary(assignments, day):
    assignment = next_due_assignment(assignments, day)
    if assignment is None:
        return "Assignments: None active"
    return f"Assignments: {assignment.summary_label()}"
