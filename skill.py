import pygame
from settings import *


class Skill:
    def __init__(self, cost):
        self.cost = cost
        self.name = "empty skill"
        self.explaination = "no explaination"
        self.skill_image_path = "./Chloe/skill_image/sprout_of_blue.png"

    def execute_one(self, caster, target):
        pass

    def execute(self, caster, targets):
        for target in targets:
            self.execute_one(caster, target)

    def execute_range(self, pos):
        return [(i + 1, 1) for i in range(5)] + \
               [(i + 1, 2) for i in range(5)] + \
               [(i + 1, 3) for i in range(5)] + \
               [(i + 1, 4) for i in range(5)] + \
               [(i + 1, 5) for i in range(5)]

    def atk_range(self, caster_pos, pos):
        return [pos]