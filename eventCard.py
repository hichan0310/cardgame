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
    from gameMap import GameMap


class EventCard(pygame.sprite.Sprite):
    def __init__(self, pos_center, info, game_board: "gameMap", group, class_name):
        super().__init__(group)
        self.group = group
        self.class_name = class_name
        self.name, self.cost, self.img_path, self.explaination, self.execute_type = info
        self.pos_center = pos_center
        self.game_board = game_board
        self.image = pygame.transform.scale(pygame.image.load(self.img_path), CARD_SIZE)
        self.rect = self.image.get_rect(center=pos_center)
        self.mask = pygame.mask.from_surface(self.image)

    def update_location(self, pos_center):
        self.pos_center = pos_center
        self.rect = self.image.get_rect(center=pos_center)
        self.mask = pygame.mask.from_surface(self.image)

    def execute_range_one(self):
        return []

    def execute_range_two(self):
        return [], []

    def execute_zero(self):
        pass

    def execute_one(self, pos, target):
        pass

    def execute_two(self, pos1, pos2, target1, target2):
        pass
