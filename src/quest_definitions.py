from src.config import ITEM_ID, ROOM_INTRAMUROS, SKILL_ACADEMICS
from src.quests import Quest, QuestManager, QuestObjective, QuestReward


FIRST_DAY_QUEST_ID = "first_day_at_mapua"
FIRST_DAY_PICK_UP_ID = "pick_up_id"
FIRST_DAY_TALK_TO_MOM = "talk_to_mom"
FIRST_DAY_RIDE_BUS = "ride_bus"
FIRST_DAY_ENTER_CAMPUS = "enter_campus"
FIRST_DAY_STUDY = "study"


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


def create_initial_quest_manager():
    manager = QuestManager()
    manager.add_quest(create_first_day_quest())
    manager.start_quest(FIRST_DAY_QUEST_ID)
    return manager


def is_first_day_bus_destination(destination):
    return destination == ROOM_INTRAMUROS


def is_first_day_item(item_id):
    return item_id == ITEM_ID
