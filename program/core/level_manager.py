import json
from pathlib import Path
from typing import Dict, List, Any


class LevelManager:
    """关卡管理器：内置关卡 + 自定义关卡统一入口。"""

    REQUIRED_FIELDS = {
        "id", "name", "type", "target", "grid", "hint_1", "hint_2", "design_intent", "math_basis"
    }
    VALID_TYPES = {"length", "area", "perimeter", "expression"}
    VALID_GRIDS = {4, 5, 10}

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.level_dir = base_dir / "level"
        self.levels: List[Dict[str, Any]] = self._bootstrap_levels()

    def _builtin_levels(self) -> List[Dict[str, Any]]:
        return [
            # Beginner Guidance 1-5
            {"id": 1, "name": "一只普通的线", "type": "length", "target": 3, "grid": 4, "hint_1": "尝试连接两个点", "hint_2": "横向或纵向长度为3", "design_intent": "引导玩家理解最基本的点到点连接", "math_basis": "单位长度相加"},
            {"id": 2, "name": "走弯路の线", "type": "length", "target": 4, "grid": 4, "hint_1": "不一定要直线", "hint_2": "可以分成两段", "design_intent": "引导玩家理解路径可以分段", "math_basis": "分段长度求和"},
            {"id": 3, "name": "线连起来了！", "type": "perimeter", "target": 8, "grid": 4, "hint_1": "尝试围成图形", "hint_2": "一个边长为2的正方形", "design_intent": "引导闭合路径概念", "math_basis": "周长 = 边长之和"},
            {"id": 4, "name": "点与线", "type": "length", "target": 5, "grid": 4, "hint_1": "尝试斜线", "hint_2": "3和4组成的直角三角形", "design_intent": "引入对角线", "math_basis": "勾股定理 √(3²+4²)"},
            {"id": 5, "name": "Line-Bridge", "type": "area", "target": 4, "grid": 4, "hint_1": "围成区域", "hint_2": "2×2", "design_intent": "让玩家理解面积来自闭合图形", "math_basis": "面积 = 长×宽"},
            # Rational_Number 6-15
            {"id": 6, "name": "分数的长度", "type": "length", "target": 2.5, "grid": 5, "hint_1": "组合长度", "hint_2": "2+0.5", "design_intent": "引入非整数长度", "math_basis": "有理数加法"},
            {"id": 7, "name": "小数面积", "type": "area", "target": 6.25, "grid": 5, "hint_1": "面积也可以是小数", "hint_2": "2.5×2.5", "design_intent": "引导玩家接受非整数面积", "math_basis": "小数乘法"},
            {"id": 8, "name": "长方形", "type": "area", "target": 6, "grid": 5, "hint_1": "不是正方形", "hint_2": "2×3", "design_intent": "理解多解结构", "math_basis": "矩形面积公式"},
            {"id": 9, "name": "周长挑战", "type": "perimeter", "target": 10, "grid": 5, "hint_1": "边可以不同", "hint_2": "2+3+2+3", "design_intent": "理解周长变化", "math_basis": "边长累加"},
            {"id": 10, "name": "斜线大师", "type": "length", "target": 5, "grid": 5, "hint_1": "对角线", "hint_2": "√(3²+4²)", "design_intent": "强化勾股理解", "math_basis": "欧几里得距离"},
            {"id": 11, "name": "双倍面积", "type": "area", "target": 8, "grid": 5, "hint_1": "组合图形", "hint_2": "2个2×2", "design_intent": "拆分组合图形", "math_basis": "面积可加性"},
            {"id": 12, "name": "复杂路径", "type": "length", "target": 7, "grid": 5, "hint_1": "多段", "hint_2": "3+2+2", "design_intent": "路径规划", "math_basis": "线段加法"},
            {"id": 13, "name": "不规则图形", "type": "area", "target": 5, "grid": 5, "hint_1": "L形", "hint_2": "组合", "design_intent": "打破规则图形限制", "math_basis": "拆分法"},
            {"id": 14, "name": "周长变化", "type": "perimeter", "target": 12, "grid": 5, "hint_1": "多边", "hint_2": "3×4", "design_intent": "路径优化", "math_basis": "周长计算"},
            {"id": 15, "name": "表达式初体验", "type": "expression", "target": "2x+3", "grid": 5, "hint_1": "变量表示长度", "hint_2": "2段x+3段1", "design_intent": "引入代数思维", "math_basis": "代数表达式结构"},
            # Hard 16-25
            {"id": 16, "name": "精确长度", "type": "length", "target": 7.07, "grid": 10, "hint_1": "对角线", "hint_2": "√50", "design_intent": "引入误差容忍", "math_basis": "近似值"},
            {"id": 17, "name": "复杂面积", "type": "area", "target": 13, "grid": 10, "hint_1": "拆分", "hint_2": "9+4", "design_intent": "复杂图形拆解", "math_basis": "面积加法"},
            {"id": 18, "name": "多边形周长", "type": "perimeter", "target": 20, "grid": 10, "hint_1": "多边", "hint_2": "5×4", "design_intent": "路径设计", "math_basis": "周长累加"},
            {"id": 19, "name": "分割面积", "type": "area", "target": 7.5, "grid": 10, "hint_1": "三角形", "hint_2": "底×高÷2", "design_intent": "引入非矩形面积", "math_basis": "三角形面积"},
            {"id": 20, "name": "复杂路径", "type": "length", "target": 12, "grid": 10, "hint_1": "分段", "hint_2": "5+4+3", "design_intent": "路径规划强化", "math_basis": "分段求和"},
            {"id": 21, "name": "不规则挑战", "type": "area", "target": 11, "grid": 10, "hint_1": "拆分", "hint_2": "6+5", "design_intent": "非规则区域理解", "math_basis": "组合面积"},
            {"id": 22, "name": "周长优化", "type": "perimeter", "target": 18, "grid": 10, "hint_1": "紧凑", "hint_2": "矩形", "design_intent": "最优路径思维", "math_basis": "周长最小化"},
            {"id": 23, "name": "表达式进阶", "type": "expression", "target": "x^2", "grid": 10, "hint_1": "面积", "hint_2": "x乘x", "design_intent": "变量平方理解", "math_basis": "代数平方"},
            {"id": 24, "name": "面积与周长", "type": "area", "target": 16, "grid": 10, "hint_1": "正方形", "hint_2": "4×4", "design_intent": "回归规则图形", "math_basis": "平方关系"},
            {"id": 25, "name": "终极路径", "type": "length", "target": 15, "grid": 10, "hint_1": "组合", "hint_2": "分段", "design_intent": "综合能力测试", "math_basis": "路径累加"},
            # Goodbye 26-30
            {"id": 26, "name": "不普通的线", "type": "length", "target": 10, "grid": 10, "hint_1": "组合路径", "hint_2": "拆分", "design_intent": "强化路径策略", "math_basis": "长度叠加"},
            {"id": 27, "name": "弯弯绕绕", "type": "perimeter", "target": 22, "grid": 10, "hint_1": "复杂图形", "hint_2": "组合", "design_intent": "复杂路径理解", "math_basis": "周长计算"},
            {"id": 28, "name": "线动成面", "type": "area", "target": 20, "grid": 10, "hint_1": "大区域", "hint_2": "5×4", "design_intent": "视觉与数学统一", "math_basis": "面积公式"},
            {"id": 29, "name": "坐标艺术", "type": "expression", "target": "2x+2y", "grid": 10, "hint_1": "横纵", "hint_2": "组合", "design_intent": "二维表达式理解", "math_basis": "多变量表达式"},
            {"id": 30, "name": "Last Goodbye", "type": "area", "target": 25, "grid": 10, "hint_1": "最大正方形", "hint_2": "5×5", "design_intent": "收束与情绪结束", "math_basis": "平方面积"},
        ]

    def _validate_level(self, lv: Dict[str, Any]) -> None:
        missing = self.REQUIRED_FIELDS - set(lv.keys())
        if missing:
            raise ValueError(f"关卡字段缺失: {missing}, level={lv.get('id')}")
        if lv["type"] not in self.VALID_TYPES:
            raise ValueError(f"关卡类型错误: {lv['type']}")
        if lv["grid"] not in self.VALID_GRIDS:
            raise ValueError(f"网格规格错误: {lv['grid']}")

    def _bootstrap_levels(self) -> List[Dict[str, Any]]:
        self.level_dir.mkdir(parents=True, exist_ok=True)
        built_in = self._builtin_levels()
        for lv in built_in:
            self._validate_level(lv)
        custom_levels = self.load_custom_levels()
        return sorted(built_in + custom_levels, key=lambda x: x["id"])

    def load_custom_levels(self) -> List[Dict[str, Any]]:
        custom_dir = self.level_dir / "custom"
        custom_dir.mkdir(parents=True, exist_ok=True)
        levels: List[Dict[str, Any]] = []
        for fp in custom_dir.glob("*.json"):
            with fp.open("r", encoding="utf-8") as f:
                lv = json.load(f)
                self._validate_level(lv)
                levels.append(lv)
        return levels

    def save_custom_level(self, level_data: Dict[str, Any]) -> None:
        self._validate_level(level_data)
        custom_dir = self.level_dir / "custom"
        custom_dir.mkdir(parents=True, exist_ok=True)
        out = custom_dir / f"{level_data['id']}.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(level_data, f, ensure_ascii=False, indent=2)
        self.levels = sorted(self.levels + [level_data], key=lambda x: x["id"])
