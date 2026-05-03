import pygame
from typing import List, Tuple


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.bg = (28, 28, 38)
        self.grid_color = (85, 90, 120)
        self.line_color = (130, 220, 255)
        self.text_color = (238, 238, 238)
        self.flash = 0
        # 某些 Windows + Store Python 环境下 SysFont 会被系统字体注册表异常数据触发崩溃
        # 使用 pygame 内置默认字体，稳定跨平台~
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, 28)

    def draw_grid(self, origin: Tuple[int, int], cell: int, size: int) -> None:
        for i in range(size):
            pygame.draw.line(self.screen, self.grid_color, (origin[0], origin[1] + i * cell), (origin[0] + (size - 1) * cell, origin[1] + i * cell), 1)
            pygame.draw.line(self.screen, self.grid_color, (origin[0] + i * cell, origin[1]), (origin[0] + i * cell, origin[1] + (size - 1) * cell), 1)

    def draw_path(self, points: List[Tuple[int, int]], growth: float = 1.0) -> None:
        if len(points) < 2:
            return
        max_i = max(2, int(len(points) * growth))
        pygame.draw.lines(self.screen, self.line_color, False, points[:max_i], 4)
        for p in points[:max_i]:
            pygame.draw.circle(self.screen, (255, 200, 180), p, 5)

    def draw_ui(self, result: str, grade: str, hint_count: int) -> None:
        texts = [f"Result: {result}", f"Grade: {grade}", f"Hints: {hint_count}", "Z=Undo, H=Hint, E=Editor"]
        for i, t in enumerate(texts):
            surf = self.font.render(t, True, self.text_color)
            self.screen.blit(surf, (20, 20 + i * 28))

    def draw_popup(self, msg: str) -> None:
        panel = pygame.Surface((460, 80), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 200))
        self.screen.blit(panel, (170, 500))
        self.screen.blit(self.font.render(msg, True, (255, 255, 120)), (190, 528))
