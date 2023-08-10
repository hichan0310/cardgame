import random

import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos

if TYPE_CHECKING:
    from playerCard import PlayerCard


class EventCard(pygame.sprite.Sprite):
    def __init__(self, pos_center, img_path, execute_type, game_board, group):
        super().__init__(group)
        self.execute_type=execute_type
        self.pos_center = pos_center
        self.game_board = game_board
        self.image = pygame.transform.scale(pygame.image.load(img_path), CARD_SIZE)
        self.rect = self.image.get_rect(center=pos_center)
        self.mask = pygame.mask.from_surface(self.image)

    # 인자 없음
    def click_zero(self):
        pass

    # 인자 1개
    def click_one(self, pos1):
        pass

    #인자 2개
    def click_two(self, pos1, pos2):
        pass
