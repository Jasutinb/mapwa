SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

STATE_PLAY = "play"
STATE_DIALOGUE = "dialogue"
STATE_MENU = "menu"
STATE_SLEEP_CONFIRM = "sleep_confirm"

ROOM_MAIN = "main"
ROOM_BEDROOM = "bedroom"
ROOM_OUTSIDE = "outside"
ROOM_INTRAMUROS = "intramuros"
ROOM_SCHOOL_ENTRANCE = "school_entrance"
ROOM_ADMIN_OFFICE = "admin_office"
ROOM_SCHOOL = "school"
ROOM_PROGRAMMING_LAB = "programming_lab"
ROOM_ELECTRONICS_LAB = "electronics_lab"
ROOM_LIBRARY = "library"
ROOM_CAFETERIA = "cafeteria"

ALLOWANCE_AMOUNT = 250
MAX_ENERGY = 100
MIN_STRESS = 0
MAX_STRESS = 100
STARTING_STRESS = 0
MIN_GRADE_STANDING = 0
MAX_GRADE_STANDING = 100
STARTING_GRADE_STANDING = 75
GRADE_STANDING_EXAM_PASS_INCREASE = 5
GRADE_STANDING_EXAM_FAIL_DECREASE = 8
GRADE_STANDING_ASSIGNMENT_MISSED_DECREASE = 5
SLEEP_STRESS_RECOVERY = 20
LOW_ENERGY_STRESS_INCREASE = 5
MEAL_PRICE = 50
MEAL_ENERGY = 25
SCHOOL_STUDY_ENERGY_COST = 10
PROGRAMMING_PRACTICE_ENERGY_COST = 15
ELECTRONICS_PRACTICE_ENERGY_COST = 15
LIBRARY_STUDY_ENERGY_COST = 10
SKILL_ACADEMICS = "academics"
SKILL_MATH = "math"
SKILL_DISCIPLINE = "discipline"
SKILL_PROGRAMMING = "programming"
SKILL_ELECTRONICS = "electronics"
SKILL_SOCIAL = "social"
SKILL_FINANCE = "finance"
TRACKED_SKILLS = (
    SKILL_ACADEMICS,
    SKILL_MATH,
    SKILL_DISCIPLINE,
    SKILL_PROGRAMMING,
    SKILL_ELECTRONICS,
    SKILL_SOCIAL,
    SKILL_FINANCE,
)
STUDY_XP = 10
STUDY_DURATION_FRAMES = 60
ADMIN_OFFICE_CHECK_IN_XP = 5
PROGRAMMING_LAB_XP = 10
ELECTRONICS_LAB_XP = 10
CLASSMATE_SOCIAL_XP = 10
CAFETERIA_FINANCE_XP = 5
LIBRARY_STUDY_XP = 10
CLASS_ATTENDANCE_XP = 15
ASSIGNMENT_REWARD_XP = 20
ASSIGNMENT_MISSED_STRESS = 10
EXAM_REWARD_XP = 30
EXAM_ENERGY_COST = 20
EXAM_STRESS_PENALTY = 12

FIRST_MOM_DIALOGUE = [
    "Hi sweetie!",
    "Are you ready for your first day at school?",
    "Don't forget your backpack!",
    "Here's your allowance for today.",
]

DAILY_ALLOWANCE_MOM_DIALOGUE = [
    "Hi sweetie!",
    "Spend it wisely.",
    "Here's your allowance for today.",
]

REPEAT_MOM_DIALOGUE = [
    "Hi sweetie!",
    "Make sure to study hard!",
    "I'll see you later.",
]

SCHOOL_GATE_NO_ID_DIALOGUE = [
    'The guard blocks the gate. "Please present your Student ID first."',
]

SCHOOL_GUARD_NO_ID_DIALOGUE = [
    "Please present your Student ID at the gate.",
    "No ID, no campus entry.",
]

SCHOOL_GUARD_NO_ID_REDIRECT_DIALOGUE = [
    "You forgot your Student ID. Please report to the Admin Office for a temporary campus pass.",
]

SCHOOL_GUARD_HAS_ID_DIALOGUE = [
    "ID verified. You may proceed through the gate.",
    "Stay safe on campus.",
]

SCHOOL_GUARD_TEMP_PASS_DIALOGUE = [
    "Temporary campus pass verified. You may use the gate today.",
]

ADMIN_OFFICE_NO_ID_DIALOGUE = [
    "Admin issued you a temporary campus pass for today.",
    "Bring your Student ID tomorrow to avoid another admin stop.",
]

ADMIN_OFFICE_TEMP_PASS_ACTIVE_DIALOGUE = [
    "Your temporary campus pass is already active for today.",
    "You can enter campus through the gate now.",
]

ADMIN_OFFICE_CHECK_IN_DIALOGUE = [
    "Student ID verified. Your enrollment record is now active.",
    "You receive 5 academics XP for learning how admin check-in works.",
]

ADMIN_OFFICE_CHECKED_IN_DIALOGUE = [
    "Your enrollment record is already active.",
    "Check the school office if you need help with documents later.",
]

CAFETERIA_VENDOR_DIALOGUE = [
    "One hot meal coming up!",
]

CAFETERIA_NOT_ENOUGH_MONEY_DIALOGUE = [
    "You don't have enough money for a meal.",
]

CAFETERIA_FULL_ENERGY_DIALOGUE = [
    "You're already full of energy.",
]

CLASSMATE_HINT_TEXT = "Press E to talk"

CLASSMATE_INTRO_DIALOGUE = [
    "Hey, I'm Alex from your block. Want to compare notes after class?",
    "Social skill unlocked! You gained {xp} social XP. Total: {total}.",
]

CLASSMATE_REPEAT_DIALOGUE = [
    "Let's compare notes again after the next class.",
    "Good luck with your requirements today.",
]

LOST_CALCULATOR_START_DIALOGUE = [
    "Actually, can you help me? I lost my calculator before Math.",
    "I think I left it in the Library. Could you bring it back?",
]

LOST_CALCULATOR_SEARCH_DIALOGUE = [
    "I still can't find my calculator. I last had it in the Library.",
]

LOST_CALCULATOR_RETURN_DIALOGUE = (
    "You returned Alex's calculator and gained {xp} social XP! Total: {total}."
)

LOST_CALCULATOR_DONE_DIALOGUE = [
    "Thanks again for finding my calculator. I owe you one.",
]

INSUFFICIENT_ENERGY_DIALOGUE = [
    "You're too tired for that. Eat something or sleep first.",
]

LOW_ENERGY_STRESS_DIALOGUE = "Stress increased by {amount}."

CLASS_ATTENDED_DIALOGUE = (
    "You attended {course_name} and gained {xp} {skill} XP! Total: {total}."
)
CLASS_ALREADY_ATTENDED_DIALOGUE = "You already attended {course_name} today."
CLASS_NO_CLASSES_TODAY_DIALOGUE = "There are no classes today."
CLASS_NO_CLASS_HERE_DIALOGUE = "No class is scheduled here today."

ASSIGNMENT_COMPLETED_DIALOGUE = (
    "You completed {title} and gained {xp} {skill} XP! Total: {total}."
)
ASSIGNMENT_NONE_AVAILABLE_DIALOGUE = "No assignments are ready to submit right now."
ASSIGNMENT_MISSED_DIALOGUE = (
    "You missed {count} assignment deadline(s). Stress increased by {stress}. "
    "Grade Standing decreased by {grade}."
)
EXAM_COMPLETED_DIALOGUE = "You already passed {title}."
EXAM_NONE_AVAILABLE_DIALOGUE = "No exams are available here right now."
EXAM_PASSED_DIALOGUE = (
    "You passed {title} and gained {xp} {skill} XP! Total: {total}. "
    "Grade Standing increased by {grade}."
)
EXAM_FAILED_DIALOGUE = (
    "You failed {title}. Recommended {required} {skill} XP; you have {current}. "
    "Stress increased by {stress}. Grade Standing decreased by {grade}."
)

ITEM_ID = "student_id"
LOST_CALCULATOR_ITEM_ID = "calculator"
