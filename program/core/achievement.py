from typing import Dict, List


class AchievementSystem:
    def __init__(self) -> None:
        self.rules = {
            "初入数学": lambda s: s.get("level", 0) >= 1,
            "完美主义者": lambda s: "S" in s.get("recent_grades", []),
            "连续胜利": lambda s: s.get("streak_success", 0) >= 3,
            "创造者": lambda s: s.get("created_level", False),
            "数学大师": lambda s: s.get("level", 0) >= 4,
            "一次过关": lambda s: s.get("first_try_win", False),
            "提示达人": lambda s: s.get("hints", 0) >= 10,
            "节约大师": lambda s: s.get("no_hint_wins", 0) >= 5,
            "探索者": lambda s: len(s.get("shape_set", [])) >= 10,
            "精准计算": lambda s: s.get("last_error", 100) <= 1,
            "坚持不懈": lambda s: s.get("fail_count", 0) >= 10 and s.get("last_win", False),
            "夜行者": lambda s: s.get("night_wins", 0) >= 3,
            "速度之星": lambda s: s.get("fast_win", False),
            "全能玩家": lambda s: all(v >= 3 for v in s.get("difficulty_done", {"beginner": 0, "normal": 0, "hard": 0}).values()),
            "彩蛋猎人": lambda s: len(s.get("easter_eggs", [])) >= 5,
        }

    def evaluate(self, save_data: Dict) -> List[str]:
        unlocked = set(save_data.get("achievements", []))
        new_unlocks = []
        for name, fn in self.rules.items():
            if name not in unlocked and fn(save_data):
                unlocked.add(name)
                new_unlocks.append(name)
        save_data["achievements"] = sorted(unlocked)
        return new_unlocks
