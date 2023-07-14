from typing import Callable
import pygame


# 프레임 단위의 그래픽을 그려주는 클래스
class GraphicManager:
    def __init__(self):
        self.__graphics: list[list[Callable[[pygame.Surface], None]]] = []

    def add_motion(self, drawer, after_frame):
        l = len(self.__graphics)
        while l >= after_frame:
            self.__graphics.append([])
            l += 1
        self.__graphics[after_frame].append(drawer)

    def draw(self, screen):
        if len(self.__graphics) == 0:
            return
        for motion in self.__graphics.pop(0):
            motion(screen)

    def motion_playing(self):
        return len(self.__graphics)!=0


motion_draw = GraphicManager()