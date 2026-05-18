from sqli_lab.scoring import (
    calculate_awarded_points,
    streak_bonus,
    total_with_streak,
    add_badge,
    parse_badges,
)


def test_no_points_when_already_completed():
    assert calculate_awarded_points(100, True) == 0
    assert calculate_awarded_points(100, False) == 100


def test_streak_bonus_capped():
    assert streak_bonus(1) == 0
    assert streak_bonus(3) == 10
    assert streak_bonus(99) == 25


def test_total_with_streak_skips_if_done():
    assert total_with_streak(100, 5, True) == 0
    assert total_with_streak(100, 3, False) == 110


def test_badges():
    assert parse_badges("") == []
    merged = add_badge("a", "b")
    assert "a" in parse_badges(merged) and "b" in parse_badges(merged)
