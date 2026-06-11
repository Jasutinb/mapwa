import pytest

from src.skill_xp import SkillXPManager


def test_grants_xp_to_independent_skills():
    manager = SkillXPManager()

    assert manager.grant_xp("academics", 10) == 10
    assert manager.grant_xp("fitness", 5) == 5
    assert manager.grant_xp("academics", 3) == 13

    assert manager.get_xp("academics") == 13
    assert manager.get_xp("fitness") == 5
    assert manager.get_xp("untrained") == 0
    assert manager.total_xp == 18


@pytest.mark.parametrize(
    ("skill", "amount"),
    [
        ("", 10),
        ("academics", 0),
        ("academics", -1),
        ("academics", 1.5),
    ],
)
def test_rejects_invalid_grants(skill, amount):
    manager = SkillXPManager()

    with pytest.raises(ValueError):
        manager.grant_xp(skill, amount)
