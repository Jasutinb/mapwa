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

ALLOWANCE_AMOUNT = 250
SKILL_ACADEMICS = "academics"
STUDY_XP = 10
STUDY_DURATION_FRAMES = 60
ADMIN_OFFICE_CHECK_IN_XP = 5

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

SCHOOL_GUARD_HAS_ID_DIALOGUE = [
    "ID verified. You may proceed through the gate.",
    "Stay safe on campus.",
]

ADMIN_OFFICE_NO_ID_DIALOGUE = [
    "Please bring your Student ID before we can process your enrollment record.",
]

ADMIN_OFFICE_CHECK_IN_DIALOGUE = [
    "Student ID verified. Your enrollment record is now active.",
    "You receive 5 academics XP for learning how admin check-in works.",
]

ADMIN_OFFICE_CHECKED_IN_DIALOGUE = [
    "Your enrollment record is already active.",
    "Check the school office if you need help with documents later.",
]

ITEM_ID = "student_id"
