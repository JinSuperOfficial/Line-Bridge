import math
from typing import List, Tuple


class InputHandler:
    def __init__(self, origin: Tuple[int, int], cell: int, grid_size: int) -> None:
        self.origin = origin
        self.cell = cell
        self.grid_size = grid_size
        self.points: List[Tuple[int, int]] = []

    def snap(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x = round((pos[0] - self.origin[0]) / self.cell)
        y = round((pos[1] - self.origin[1]) / self.cell)
        x = max(0, min(self.grid_size - 1, x))
        y = max(0, min(self.grid_size - 1, y))
        return x, y

    def add_point(self, pos: Tuple[int, int]) -> None:
        p = self.snap(pos)
        if not self.points or self.points[-1] != p:
            self.points.append(p)

    def undo(self) -> None:
        if self.points:
            self.points.pop()

    def world_points(self) -> List[Tuple[int, int]]:
        return [(self.origin[0] + x * self.cell, self.origin[1] + y * self.cell) for x, y in self.points]

    @staticmethod
    def length(points: List[Tuple[int, int]]) -> float:
        total = 0.0
        for i in range(1, len(points)):
            dx = points[i][0] - points[i - 1][0]
            dy = points[i][1] - points[i - 1][1]
            total += math.hypot(dx, dy)
        return total

    @staticmethod
    def area(points: List[Tuple[int, int]]) -> float:
        if len(points) < 3 or points[0] != points[-1]:
            return 0.0
        s = 0.0
        for i in range(len(points) - 1):
            s += points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
        return abs(s) / 2.0
