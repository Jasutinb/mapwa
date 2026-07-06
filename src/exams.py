from dataclasses import dataclass

from src.config import (
    EXAM_ENERGY_COST,
    EXAM_REWARD_XP,
    EXAM_STRESS_PENALTY,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SKILL_ACADEMICS,
    SKILL_PROGRAMMING,
)


EXAM_STATUS_PENDING = "pending"
EXAM_STATUS_PASSED = "passed"


@dataclass
class Exam:
    exam_id: str
    title: str
    skill: str
    room_key: str
    scheduled_day: int
    recommended_xp: int
    reward_xp: int
    energy_cost: int
    stress_penalty: int
    status: str = EXAM_STATUS_PENDING
    attempts: int = 0

    @property
    def is_pending(self):
        return self.status == EXAM_STATUS_PENDING

    @property
    def is_passed(self):
        return self.status == EXAM_STATUS_PASSED

    def is_available(self, day, room_key):
        return self.is_pending and self.scheduled_day <= day and self.room_key == room_key

    def summary_label(self):
        return f"Day {self.scheduled_day} {self.title}"


def create_initial_exams():
    return [
        Exam(
            "academics-midterm",
            "Academics Midterm",
            SKILL_ACADEMICS,
            ROOM_SCHOOL,
            scheduled_day=5,
            recommended_xp=30,
            reward_xp=EXAM_REWARD_XP,
            energy_cost=EXAM_ENERGY_COST,
            stress_penalty=EXAM_STRESS_PENALTY,
        ),
        Exam(
            "programming-practical",
            "Programming Practical",
            SKILL_PROGRAMMING,
            ROOM_PROGRAMMING_LAB,
            scheduled_day=6,
            recommended_xp=35,
            reward_xp=EXAM_REWARD_XP,
            energy_cost=EXAM_ENERGY_COST,
            stress_penalty=EXAM_STRESS_PENALTY,
        ),
    ]


def available_exams(exams, day, room_key):
    return sorted(
        (exam for exam in exams if exam.is_available(day, room_key)),
        key=lambda exam: (exam.scheduled_day, exam.title),
    )


def next_exam(exams):
    pending_exams = [exam for exam in exams if exam.is_pending]
    if not pending_exams:
        return None
    return min(pending_exams, key=lambda exam: (exam.scheduled_day, exam.title))


def exam_summary(exams):
    upcoming_exam = next_exam(exams)
    if upcoming_exam is None:
        return "Exams: All cleared"
    return f"Exams: {upcoming_exam.summary_label()}"
