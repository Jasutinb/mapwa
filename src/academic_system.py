from src.assignments import (
    ASSIGNMENT_STATUS_COMPLETED,
    ASSIGNMENT_STATUS_MISSED,
    assignment_summary,
    available_assignments,
)
from src.exams import EXAM_STATUS_PASSED, available_exams, exam_summary
from src.schedule import classes_for_day, schedule_summary_for_day, weekday_for_day
from src.config import (
    ASSIGNMENT_COMPLETED_DIALOGUE,
    ASSIGNMENT_MISSED_DIALOGUE,
    ASSIGNMENT_MISSED_STRESS,
    ASSIGNMENT_NONE_AVAILABLE_DIALOGUE,
    CLASS_ALREADY_ATTENDED_DIALOGUE,
    CLASS_ATTENDED_DIALOGUE,
    CLASS_ATTENDANCE_XP,
    CLASS_NO_CLASS_HERE_DIALOGUE,
    CLASS_NO_CLASSES_TODAY_DIALOGUE,
    EXAM_COMPLETED_DIALOGUE,
    EXAM_FAILED_DIALOGUE,
    EXAM_NONE_AVAILABLE_DIALOGUE,
    EXAM_PASSED_DIALOGUE,
    GRADE_STANDING_ASSIGNMENT_EARLY_BONUS,
    GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE,
    GRADE_STANDING_ASSIGNMENT_SUBMISSION_INCREASE,
    GRADE_STANDING_CLASS_ATTENDANCE_INCREASE,
    GRADE_STANDING_EXAM_FAIL_DECREASE,
    GRADE_STANDING_EXAM_PASS_INCREASE,
    MAX_GRADE_STANDING,
    MIN_GRADE_STANDING,
    STATE_EXAM_CONFIRM,
    STATE_PLAY,
)


class AcademicSystem:
    """Own academic schedules, work, exams, attendance, and grade effects."""

    def __init__(self, game):
        self.game = game

    @property
    def current_weekday(self):
        return weekday_for_day(self.game.current_day)

    def get_today_classes(self):
        return classes_for_day(self.game.current_day)

    def get_schedule_summary(self):
        return schedule_summary_for_day(self.game.current_day)

    def get_schedule_hud_lines(self):
        return [
            f"Day {self.game.current_day} - {self.current_weekday}",
            self.get_schedule_summary(),
        ]

    def get_attended_class_ids(self):
        game = self.game
        if game.state.attended_class_day != game.current_day:
            game.state.attended_class_day = game.current_day
            game.state.attended_class_ids.clear()
        return game.state.attended_class_ids

    def get_today_classes_for_room(self, room_name=None):
        target_room = room_name or self.game.current_room
        return [entry for entry in self.get_today_classes() if entry.room_key == target_room]

    def get_available_assignments(self):
        game = self.game
        return available_assignments(game.state.assignments, game.current_day)

    def get_assignment_summary(self):
        game = self.game
        return assignment_summary(game.state.assignments, game.current_day)

    def get_available_exams(self, room_name=None):
        game = self.game
        return available_exams(
            game.state.exams,
            game.current_day,
            room_name or game.current_room,
        )

    def get_exam_summary(self):
        return exam_summary(self.game.state.exams)

    def get_grade_summary(self):
        return f"Grade Standing: {self.game.grade_standing}/{MAX_GRADE_STANDING}"

    def adjust_grade_standing(self, amount):
        game = self.game
        previous = game.grade_standing
        game.grade_standing = max(
            MIN_GRADE_STANDING,
            min(MAX_GRADE_STANDING, previous + amount),
        )
        return game.grade_standing - previous

    def complete_assignment(self):
        game = self.game
        assignments = self.get_available_assignments()
        if not assignments:
            game.show_dialogue([ASSIGNMENT_NONE_AVAILABLE_DIALOGUE])
            return False

        assignment = assignments[0]
        assignment.status = ASSIGNMENT_STATUS_COMPLETED
        skill_xp = game.grant_skill_xp(assignment.skill, assignment.reward_xp)
        grade_increased = self.adjust_grade_standing(
            GRADE_STANDING_ASSIGNMENT_SUBMISSION_INCREASE
        )
        early_bonus = 0
        if game.current_day < assignment.due_day:
            early_bonus = self.adjust_grade_standing(
                GRADE_STANDING_ASSIGNMENT_EARLY_BONUS
            )
        grade_increased += early_bonus
        early_bonus_text = (
            f" Includes a +{early_bonus} early submission bonus."
            if early_bonus
            else ""
        )
        game.show_dialogue(
            [
                ASSIGNMENT_COMPLETED_DIALOGUE.format(
                    title=assignment.title,
                    xp=assignment.reward_xp,
                    skill=assignment.skill,
                    total=skill_xp,
                    grade=grade_increased,
                    early_bonus_text=early_bonus_text,
                )
            ]
        )
        return True

    def take_exam(self):
        game = self.game
        exams = self.get_available_exams()
        if not exams:
            passed_exam = next(
                (
                    exam
                    for exam in game.state.exams
                    if exam.room_key == game.current_room and exam.is_passed
                ),
                None,
            )
            if passed_exam is not None:
                game.show_dialogue(
                    [EXAM_COMPLETED_DIALOGUE.format(title=passed_exam.title)]
                )
            else:
                game.show_dialogue([EXAM_NONE_AVAILABLE_DIALOGUE])
            return False

        game.pending_exam_id = exams[0].exam_id
        game.state_machine.change_state(STATE_EXAM_CONFIRM)
        return True

    def get_pending_exam(self):
        game = self.game
        return next(
            (exam for exam in game.state.exams if exam.exam_id == game.pending_exam_id),
            None,
        )

    def get_exam_readiness(self, exam):
        current_xp = self.game.get_skill_xp(exam.skill)
        return {
            "current_xp": current_xp,
            "recommended_xp": exam.recommended_xp,
            "is_risky": current_xp < exam.recommended_xp,
        }

    def cancel_exam_confirmation(self):
        game = self.game
        game.pending_exam_id = None
        game.state_machine.change_state(STATE_PLAY)
        return True

    def confirm_exam_attempt(self):
        game = self.game
        exam = self.get_pending_exam()
        game.pending_exam_id = None
        if exam is None or exam not in self.get_available_exams():
            game.state_machine.change_state(STATE_PLAY)
            return False
        return self.resolve_exam_attempt(exam)

    def resolve_exam_attempt(self, exam):
        game = self.game
        if not game.spend_energy(exam.energy_cost):
            return False

        exam.attempts += 1
        current_skill_xp = game.get_skill_xp(exam.skill)
        if current_skill_xp >= exam.recommended_xp:
            exam.status = EXAM_STATUS_PASSED
            total = game.grant_skill_xp(exam.skill, exam.reward_xp)
            grade_increased = self.adjust_grade_standing(
                GRADE_STANDING_EXAM_PASS_INCREASE
            )
            game.show_dialogue(
                [
                    EXAM_PASSED_DIALOGUE.format(
                        title=exam.title,
                        xp=exam.reward_xp,
                        skill=exam.skill,
                        total=total,
                        grade=grade_increased,
                    )
                ]
            )
            return True

        stress_increased = game.increase_stress(exam.stress_penalty)
        grade_decreased = abs(
            self.adjust_grade_standing(-GRADE_STANDING_EXAM_FAIL_DECREASE)
        )
        game.show_dialogue(
            [
                EXAM_FAILED_DIALOGUE.format(
                    title=exam.title,
                    required=exam.recommended_xp,
                    skill=exam.skill,
                    current=current_skill_xp,
                    stress=stress_increased,
                    grade=grade_decreased,
                )
            ]
        )
        return False

    def attend_class(self):
        game = self.game
        classes_today = self.get_today_classes()
        if not classes_today:
            game.show_dialogue([CLASS_NO_CLASSES_TODAY_DIALOGUE])
            return False

        room_classes = self.get_today_classes_for_room()
        if not room_classes:
            game.show_dialogue([CLASS_NO_CLASS_HERE_DIALOGUE])
            return False

        attended_ids = self.get_attended_class_ids()
        class_entry = next(
            (entry for entry in room_classes if entry.identifier not in attended_ids),
            room_classes[0],
        )
        if class_entry.identifier in attended_ids:
            game.show_dialogue(
                [
                    CLASS_ALREADY_ATTENDED_DIALOGUE.format(
                        course_name=class_entry.course_name
                    )
                ]
            )
            return False

        attended_ids.add(class_entry.identifier)
        skill_xp = game.grant_skill_xp(class_entry.skill, CLASS_ATTENDANCE_XP)
        grade_increased = self.adjust_grade_standing(
            GRADE_STANDING_CLASS_ATTENDANCE_INCREASE
        )
        game.show_dialogue(
            [
                CLASS_ATTENDED_DIALOGUE.format(
                    course_name=class_entry.course_name,
                    xp=CLASS_ATTENDANCE_XP,
                    skill=class_entry.skill,
                    total=skill_xp,
                    grade=grade_increased,
                )
            ]
        )
        return True

    def process_assignment_deadlines(self):
        game = self.game
        missed_count = 0
        stress_increased = 0
        grade_decreased = 0
        for assignment in game.state.assignments:
            if not assignment.is_overdue_on(game.current_day):
                continue
            assignment.status = ASSIGNMENT_STATUS_MISSED
            if assignment.missed_stress_applied:
                continue
            assignment.missed_stress_applied = True
            missed_count += 1
            stress_increased += game.increase_stress(ASSIGNMENT_MISSED_STRESS)
            grade_decreased += abs(
                self.adjust_grade_standing(
                    -GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE
                )
            )

        if not missed_count:
            return []
        return [
            ASSIGNMENT_MISSED_DIALOGUE.format(
                count=missed_count,
                stress=stress_increased,
                grade=grade_decreased,
            )
        ]
