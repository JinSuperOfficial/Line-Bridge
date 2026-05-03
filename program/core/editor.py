import time
from typing import Dict


class LevelEditor:
    def __init__(self, level_manager) -> None:
        self.level_manager = level_manager

    def create_level(self, target_type: str, target: float, grid: int = 5) -> Dict:
        level = {
            "id": int(time.time()),
            "name": f"Custom {target_type}",
            "grid": grid,
            "type": target_type,
            "target": target,
            "hint_1": "先规划轮廓再落笔~",
            "hint_2": "离答案不远啦~",
            "design_intent": "玩家自定义目标训练",
            "math_basis": "由玩家定义的数学目标",
        }
        self.level_manager.save_custom_level(level)
        return level
