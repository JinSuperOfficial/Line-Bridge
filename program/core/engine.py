import re
import sys
import time
from pathlib import Path

import pygame

from .achievement import AchievementSystem
from .audio import AudioSystem
from .editor import LevelEditor
from .input import InputHandler
from .language import LanguageManager
from .level_manager import LevelManager
from .renderer import Renderer
from .save_system import SaveSystem


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 620))
        pygame.display.set_caption("Line-Bridge / 线之枢纽 / 線の橋")
        self.clock = pygame.time.Clock()

        self.base = Path(__file__).resolve().parents[1]
        self.lang = LanguageManager()
        self.save_system = SaveSystem()
        self.save = self.save_system.load()
        self.level_manager = LevelManager(self.base)
        self.editor = LevelEditor(self.level_manager)
        self.achievement = AchievementSystem()
        self.audio = AudioSystem()
        self.audio.init()
        self.renderer = Renderer(self.screen)

        self.current_level_idx = 0
        self.hint_used = 0
        self.popup_msg = ""
        self.popup_until = 0.0
        self.growth = 1.0
        self.username = self._ask_username(self.save.get("username", ""))
        self.save["username"] = self.username
        self.expression_input = ""
        self.submitted = False
        self.result = "pending"
        self.grade = "-"

    def _ask_username(self, default: str) -> str:
        name = default or "Player"
        return name[:8]

    def name_easter_egg(self, name: str) -> str:
        n = name.strip()
        low = n.lower()
        if n in ("QianYu", "God"):
            return "forbidden"
        if n == "JinSuper": return "创世神大人你好"
        elif n == "Chara": return "这里不是Undertale"
        elif low in ("math", "maths"): return "你是数学大人"
        elif low in ("chinese", "english"): return "进阶之路开启"
        elif low in ("spirit", "character"): return "你似乎命名了"
        elif low == "dream": return "逐梦者，终圆梦"
        elif low == "hello": return "你好"
        elif re.fullmatch(r"67+", n): return "？"
        elif re.fullmatch(r"([A-Za-z0-9])\1{6,}", n) or re.fullmatch(r"[A-Za-z0-9]", n): return "不是很有创意？"
        elif n == "Esc": sys.exit(0)
        elif low in ("moon", "star", "stars"): return "夜色真美"
        elif low in ("sun", "shine"): return "光"
        elif low in ("oxygen", "o2", "air", "dirt"): return "世界充满了你"
        elif low in ("money", "doller"): return "请你尊重我"
        elif low in ("dad", "mum", "father", "mother"): return "？！"
        return ""

    def evaluate(self, level, points):
        target = level["target"]
        ttype = level["type"]
        l = InputHandler.length(points)
        if ttype == "length":
            val = l
        elif ttype == "perimeter":
            val = l + (((points[0][0]-points[-1][0])**2 + (points[0][1]-points[-1][1])**2) ** 0.5 if len(points) > 2 else 0)
        elif ttype == "area":
            val = InputHandler.area(points + [points[0]]) if len(points) > 2 else 0
        else:
            target_expr = str(target).replace(" ", "").lower().replace("**", "^")
            input_expr = self.expression_input.replace(" ", "").lower().replace("**", "^")
            return ("success", "A", 0.0) if target_expr == input_expr else ("fail", "B", 100.0)

        err = abs(val - float(target)) / float(target) * 100 if target else 0
        if err <= 1 and self.hint_used == 0:
            return "success", "S", err
        if err <= 3:
            return "success", "A", err
        if err <= 5:
            return "close", "B", err
        return "fail", "B", err

    def _reset_for_next_level(self, new_grid: int, origin, cell):
        self.hint_used = 0
        self.expression_input = ""
        self.submitted = False
        self.result = "pending"
        self.grade = "-"
        self.growth = 0.0
        self.ih = InputHandler(origin, cell, new_grid)

    def run(self) -> None:
        running = True
        self.ih = None
        while running:
            level = self.level_manager.levels[self.current_level_idx % len(self.level_manager.levels)]
            grid = level["grid"]
            origin, cell = (180, 120), int(360 / max(1, grid - 1))
            if self.ih is None or self.ih.grid_size != grid:
                self._reset_for_next_level(grid, origin, cell)
            ih = self.ih

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    if e.key == pygame.K_z:
                        ih.undo()
                    if e.key == pygame.K_h:
                        self.hint_used += 1
                        self.save["hints"] += 1
                        self.popup_msg = level["hint_1"] if self.hint_used == 1 else level["hint_2"]
                        self.popup_until = time.time() + 2
                    if e.key == pygame.K_e:
                        self.editor.create_level("length", 10, 5)
                        self.save["created_level"] = True
                        self.popup_msg, self.popup_until = "已创建自定义关卡", time.time() + 2
                    if e.key == pygame.K_RETURN and not self.submitted:
                        self.result, self.grade, err = self.evaluate(level, ih.points)
                        self.submitted = True
                        self.save["recent_grades"] = self.save.get("recent_grades", [])[-4:] + [self.grade]
                        if self.result == "success":
                            self.save["level"] += 1
                            self.save["rewards"] += 1 + (2 if err <= 1 else 0) + (1 if self.grade == "S" else 0)
                            self.current_level_idx += 1
                            self.popup_msg, self.popup_until = f"通关! 评级: {self.grade}", time.time() + 2
                        elif self.result == "fail":
                            self.save["fail_count"] += 1
                            self.popup_msg, self.popup_until = "再试一次吧~", time.time() + 1.5
                        new_ach = self.achievement.evaluate(self.save)
                        if new_ach:
                            self.popup_msg, self.popup_until = f"成就解锁: {new_ach[0]}", time.time() + 2
                    if level["type"] == "expression":
                        if e.key == pygame.K_BACKSPACE:
                            self.expression_input = self.expression_input[:-1]
                        elif e.unicode and len(self.expression_input) < 16 and e.unicode in "0123456789xyXY+-^*() ":
                            self.expression_input += e.unicode
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    ih.add_point(e.pos)
                elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
                    ih.add_point(e.pos)

            self.screen.fill((28, 28, 38))
            self.renderer.draw_grid(origin, cell, grid)
            wp = ih.world_points()
            self.growth = min(1.0, self.growth + 0.08)
            self.renderer.draw_path(wp, self.growth)
            self.renderer.draw_ui(self.result, self.grade, self.hint_used)
            if level["type"] == "expression":
                self.renderer.draw_popup(f"Expr: {self.expression_input or '(input)'}")
            if time.time() < self.popup_until:
                self.renderer.draw_popup(self.popup_msg)
            pygame.display.flip()
            self.clock.tick(60)

        self.save_system.save(self.save)
        pygame.quit()
