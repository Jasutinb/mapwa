from dataclasses import dataclass

from src.config import (
    ROOM_ELECTRONICS_LAB,
    ROOM_LIBRARY,
    ROOM_PROGRAMMING_LAB,
    ROOM_SCHOOL,
    SKILL_ACADEMICS,
    SKILL_DISCIPLINE,
    SKILL_ELECTRONICS,
    SKILL_MATH,
    SKILL_PROGRAMMING,
)


WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


@dataclass(frozen=True)
class ClassScheduleEntry:
    course_name: str
    weekday: str
    start_label: str
    end_label: str
    room_label: str
    room_key: str
    skill: str

    @property
    def time_label(self):
        return f"{self.start_label}-{self.end_label}"

    def summary_label(self):
        return f"{self.start_label} {self.course_name} ({self.room_label})"


WEEKLY_CLASS_SCHEDULE = (
    ClassScheduleEntry(
        "Academics",
        "Monday",
        "08:00",
        "09:30",
        "School",
        ROOM_SCHOOL,
        SKILL_ACADEMICS,
    ),
    ClassScheduleEntry(
        "Programming",
        "Monday",
        "10:00",
        "11:30",
        "Programming Lab",
        ROOM_PROGRAMMING_LAB,
        SKILL_PROGRAMMING,
    ),
    ClassScheduleEntry(
        "Math",
        "Tuesday",
        "08:00",
        "09:30",
        "Library",
        ROOM_LIBRARY,
        SKILL_MATH,
    ),
    ClassScheduleEntry(
        "Electronics",
        "Wednesday",
        "10:00",
        "11:30",
        "Electronics Lab",
        ROOM_ELECTRONICS_LAB,
        SKILL_ELECTRONICS,
    ),
    ClassScheduleEntry(
        "Discipline",
        "Thursday",
        "13:00",
        "14:00",
        "Library",
        ROOM_LIBRARY,
        SKILL_DISCIPLINE,
    ),
    ClassScheduleEntry(
        "Academics",
        "Friday",
        "09:00",
        "10:30",
        "School",
        ROOM_SCHOOL,
        SKILL_ACADEMICS,
    ),
)


def weekday_for_day(day):
    return WEEKDAYS[(day - 1) % len(WEEKDAYS)]


def classes_for_weekday(weekday):
    return [entry for entry in WEEKLY_CLASS_SCHEDULE if entry.weekday == weekday]


def classes_for_day(day):
    return classes_for_weekday(weekday_for_day(day))


def schedule_summary_for_day(day):
    weekday = weekday_for_day(day)
    classes = classes_for_weekday(weekday)
    if not classes:
        return f"{weekday}: No classes today."
    return f"{weekday}: Next {classes[0].summary_label()}"
