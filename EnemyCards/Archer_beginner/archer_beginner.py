import random

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
import pygame
from math import atan, sin, cos, sqrt, pi
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard
    from gameMap import GameMap


class Arrow(Skill):
    def __init__(self, game_board: "GameMap"):
        super().__init__(0, game_board, [TAG_NORMAL_ATTACK])
        self.name = "정조준"
        self.explaination = [
            "적군 1명에게 2의 피해를 가한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = None

    def execute(self, caster: "EnemyCard", targets: "list[PlayerCard]", caster_pos: tuple[int, int],
                targets_pos: list[tuple[int, int]], execute_pos):
        for target in targets:
            if target.name != "empty cell":
                caster.attack(2, target, self.atk_type)
        for observer in caster.observers_attack[::-1]:
            observer.attack_event(self, targets, self.game_board, self.atk_type)


class AI_ArcherBiginner:
    def __init__(self, game_board, character: "EnemyCard"):
        self.game_board = game_board
        self.character = character

    def execute(self, pos):
        target=random.choice(self.game_board.players)
        target_pos=target.pos_center
        img_arrow=pygame.image.load("./EnemyCards/Archer_beginner/arrow.png")
        img_arrow=pygame.transform.scale(img_arrow, (100, 30))
        p1=transform_pos(pos)
        p2=target_pos
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = -atan(dy / (dx - 0.00001)) / pi * 180
        if dx > 0: angle += 180
        angle+=180
        img_arrow = pygame.transform.rotate(img_arrow, angle)
        size=img_arrow.get_size()
        i=0
        while (80*i)**2<dx**2+dy**2:
            def temp(screen, i):
                t = i * 80 / sqrt(dx ** 2 + dy ** 2)
                img_pos = (p1[0] + t * dx-size[0]/2, p1[1] + t * dy-size[1]/2)
                screen.blit(img_arrow, img_pos)
            motion_draw.add_motion(temp, 20+i, (i, ))
            i+=1
        motion_draw.add_motion(lambda *_:self.character.attack(2, target, [TAG_NORMAL_ATTACK]), i+20, ())
        img = pygame.image.load("./EnemyCards/Archer_beginner/preview/arrow.png")
        for i in range(15):
            motion_draw.add_motion(lambda screen, a: screen.blit(img, (1 - 1.4 ** a, 0)), 14 - i, (i,))
        for i in range(5):
            motion_draw.add_motion(lambda screen: screen.blit(img, (0, 0)), 15 + i, tuple())
