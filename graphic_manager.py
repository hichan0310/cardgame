from typing import Callable, Any
import pygame


# 프레임 단위의 그래픽을 그려주는 클래스
class GraphicManager:
    def __init__(self):
        self.__graphics: list[list[Callable[[pygame.Surface, *Any], None]]] = []
        self.__graphic_params: list[list[tuple[Any]]] = []

    def add_motion(self, drawer, after_frame, params):
        while len(self.__graphics) <= after_frame:
            self.__graphics.append([])
        while len(self.__graphic_params) <= after_frame:
            self.__graphic_params.append([])
        self.__graphics[after_frame].append(drawer)
        self.__graphic_params[after_frame].append(params)

    def draw(self, screen):
        if len(self.__graphics) == 0:
            return
        for motion, params in zip(self.__graphics.pop(0), self.__graphic_params.pop(0)):
            motion(screen, *params)

    def motion_playing(self):
        return len(self.__graphics) != 0

    def motion_length(self):
        return len(self.__graphics)


motion_draw = GraphicManager()
