import random

import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos
from EnemyCards.Knight_beginner.knight_beginner import Shield

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard



class Push(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board)
        self.name = "밀기"
        self.explaination = [
            "바로 앞의 적에게 1의 피해를 입힌다. ",
            "자신의 몸에 2번의 피격까지 유지되는 기사의 보호막을 두른다. "
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/fast_growth.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def execute(self, caster:"PlayerCard", targets:"list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        for target in targets:
            caster.attack(2, target, "normal attack")
        Shield(caster, 2, caster.game_board)

#반격