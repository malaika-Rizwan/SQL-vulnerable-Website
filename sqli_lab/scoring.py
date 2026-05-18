"""Server-side scoring rules — unit tested."""

STREAK_BONUS_PER_DAY = 5
MAX_STREAK_BONUS = 25


def calculate_awarded_points(base_points: int, already_completed: bool) -> int:
    if already_completed:
        return 0
    return base_points


def streak_bonus(streak: int) -> int:
    if streak <= 1:
        return 0
    return min((streak - 1) * STREAK_BONUS_PER_DAY, MAX_STREAK_BONUS)


def total_with_streak(base_points: int, streak: int, already_completed: bool) -> int:
    awarded = calculate_awarded_points(base_points, already_completed)
    if awarded == 0:
        return 0
    return awarded + streak_bonus(streak)


def parse_badges(badges_csv: str) -> list[str]:
    if not badges_csv:
        return []
    return [b.strip() for b in badges_csv.split(",") if b.strip()]


def add_badge(badges_csv: str, badge: str) -> str:
    badges = parse_badges(badges_csv)
    if badge not in badges:
        badges.append(badge)
    return ",".join(badges)
