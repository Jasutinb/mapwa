from dataclasses import dataclass, field


@dataclass
class SkillXPManager:
    xp_by_skill: dict[str, int] = field(default_factory=dict)

    def grant_xp(self, skill: str, amount: int) -> int:
        self._validate_skill(skill)
        self._validate_xp(amount)

        self.xp_by_skill[skill] = self.get_xp(skill) + amount
        return self.xp_by_skill[skill]

    def get_xp(self, skill: str) -> int:
        self._validate_skill(skill)
        return self.xp_by_skill.get(skill, 0)

    @property
    def total_xp(self) -> int:
        return sum(self.xp_by_skill.values())

    @staticmethod
    def _validate_skill(skill: str) -> None:
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError("Skill name must be a non-empty string")

    @staticmethod
    def _validate_xp(amount: int) -> None:
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ValueError("XP amount must be a positive integer")
