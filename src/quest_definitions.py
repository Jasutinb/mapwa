from src.config import ITEM_ID, ROOM_INTRAMUROS, SKILL_ACADEMICS, SKILL_PROGRAMMING
from src.quests import Quest, QuestManager, QuestObjective, QuestReward


FIRST_DAY_QUEST_ID = "first_day_at_mapua"
FIRST_DAY_PICK_UP_ID = "pick_up_id"
FIRST_DAY_TALK_TO_MOM = "talk_to_mom"
FIRST_DAY_RIDE_BUS = "ride_bus"
FIRST_DAY_ENTER_CAMPUS = "enter_campus"
FIRST_DAY_STUDY = "study"
HELLO_WORLD_QUEST_ID = "hello_world"
HELLO_WORLD_ENTER_LAB = "enter_programming_lab"
HELLO_WORLD_PRACTICE_PROGRAMMING = "practice_programming"
HELLO_WORLD_REWARD_XP = 5


def create_first_day_quest():
    return Quest(
        FIRST_DAY_QUEST_ID,
        "First Day at Mapua",
        [
            QuestObjective("Pick up your Student ID.", FIRST_DAY_PICK_UP_ID),
            QuestObjective("Talk to Mom for your allowance.", FIRST_DAY_TALK_TO_MOM),
            QuestObjective("Ride the bus to Intramuros.", FIRST_DAY_RIDE_BUS),
            QuestObjective("Use your Student ID to enter campus.", FIRST_DAY_ENTER_CAMPUS),
            QuestObjective("Study at the school desk.", FIRST_DAY_STUDY),
        ],
        QuestReward(skill_xp={SKILL_ACADEMICS: 5}),
    )


def create_hello_world_quest():
    return Quest(
        HELLO_WORLD_QUEST_ID,
        "Hello World",
        [
            QuestObjective("Find the Programming Lab.", HELLO_WORLD_ENTER_LAB),
            QuestObjective("Practice programming at the workstation.", HELLO_WORLD_PRACTICE_PROGRAMMING),
        ],
        QuestReward(skill_xp={SKILL_PROGRAMMING: HELLO_WORLD_REWARD_XP}),
    )


def create_initial_quest_manager():
    manager = QuestManager()
    manager.add_quest(create_first_day_quest())
    manager.add_quest(create_hello_world_quest())
    manager.start_quest(FIRST_DAY_QUEST_ID)
    manager.start_quest(HELLO_WORLD_QUEST_ID)
    return manager


def is_first_day_bus_destination(destination):
    return destination == ROOM_INTRAMUROS


def is_first_day_item(item_id):
    return item_id == ITEM_ID
