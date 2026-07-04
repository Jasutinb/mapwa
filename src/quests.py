from dataclasses import dataclass, field


QUEST_NOT_STARTED = "not_started"
QUEST_ACTIVE = "active"
QUEST_DONE = "done"


@dataclass
class QuestObjective:
    description: str
    objective_id: str | None = None
    target: int = 1
    progress: int = 0

    def __post_init__(self):
        if not self.description.strip():
            raise ValueError("Objective description is required")
        if self.objective_id is not None and not self.objective_id.strip():
            raise ValueError("Objective id cannot be blank")
        if self.target <= 0:
            raise ValueError("Objective target must be positive")
        if self.progress < 0:
            raise ValueError("Objective progress cannot be negative")

    @property
    def complete(self):
        return self.progress >= self.target

    def advance(self, amount=1):
        if amount <= 0:
            raise ValueError("Objective progress amount must be positive")
        self.progress = min(self.target, self.progress + amount)
        return self.progress


@dataclass(frozen=True)
class QuestReward:
    money: int = 0
    skill_xp: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if self.money < 0:
            raise ValueError("Quest money reward cannot be negative")
        if any(amount <= 0 for amount in self.skill_xp.values()):
            raise ValueError("Quest skill XP rewards must be positive")


@dataclass
class Quest:
    quest_id: str
    title: str
    objectives: list[QuestObjective]
    reward: QuestReward = field(default_factory=QuestReward)
    status: str = QUEST_NOT_STARTED

    def __post_init__(self):
        if not self.quest_id.strip():
            raise ValueError("Quest id is required")
        if not self.title.strip():
            raise ValueError("Quest title is required")
        if not self.objectives:
            raise ValueError("Quest needs at least one objective")

    @property
    def current_objective(self):
        return next((objective for objective in self.objectives if not objective.complete), None)

    @property
    def complete(self):
        return all(objective.complete for objective in self.objectives)

    def start(self):
        if self.status == QUEST_NOT_STARTED:
            self.status = QUEST_ACTIVE
        return self

    def advance(self, amount=1, objective_index=None):
        if self.status == QUEST_DONE:
            return None

        self.start()
        objective = self._objective_at(objective_index)
        objective.advance(amount)

        if self.complete:
            self.status = QUEST_DONE
            return self.reward
        return None

    def advance_objective(self, objective_id, amount=1):
        objective = self.current_objective
        if objective is None or objective.objective_id != objective_id:
            return None
        return self.advance(amount, self.objectives.index(objective))

    def _objective_at(self, objective_index):
        if objective_index is None:
            objective = self.current_objective
            if objective is None:
                raise ValueError("Quest has no incomplete objectives")
            return objective
        return self.objectives[objective_index]


class QuestManager:
    def __init__(self):
        self.quests = {}

    def add_quest(self, quest):
        if quest.quest_id in self.quests:
            raise ValueError(f"Quest already exists: {quest.quest_id}")
        self.quests[quest.quest_id] = quest
        return quest

    def get_quest(self, quest_id):
        return self.quests[quest_id]

    def start_quest(self, quest_id):
        return self.get_quest(quest_id).start()

    def advance_quest(self, quest_id, amount=1, objective_index=None):
        return self.get_quest(quest_id).advance(amount, objective_index)

    def advance_objective(self, quest_id, objective_id, amount=1):
        return self.get_quest(quest_id).advance_objective(objective_id, amount)

    @property
    def active_quests(self):
        return [quest for quest in self.quests.values() if quest.status == QUEST_ACTIVE]

    @property
    def current_objective(self):
        for quest in self.active_quests:
            objective = quest.current_objective
            if objective is not None:
                return objective.description
        return ""
