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
        super().__init__(0, game_board, [TAG_NORMAL_ATTACK])
        self.name = "밀기"
        self.explaination = [
            "바로 앞의 넓은 영역에 1의 광역 피해를 입힌다. ",
            "자신의 몸에 2번의 피격까지 유지되는 기사의 보호막을 두른다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/fast_growth.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def atk_range(self, caster_pos, pos):
        if caster_pos[0] < pos[0]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1] + 1),
                 (pos[0], pos[1]), (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
            ))
        if caster_pos[0] > pos[0]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1] + 1),
                 (pos[0], pos[1]), (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
            ))
        if caster_pos[1] < pos[1]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0], pos[1]), (pos[0] - 1, pos[1]),
                 (pos[0] + 1, pos[1] + 1), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1] + 1)]
            ))
        if caster_pos[1] > pos[1]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0], pos[1]), (pos[0] - 1, pos[1]),
                 (pos[0] + 1, pos[1] - 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1] - 1)]
            ))

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        for target in targets:
            caster.attack(2, target, self.atk_type)
        Shield(caster, 2, caster.game_board)


class CounterAttackBuff(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "반격", "./PlayerCards/Tania/burn.png")
        character.register_hit(self)

    def hit_event(self, caster: "PlayerCard", target: "PlayerCard", game_board, atk_type):
        if TAG_PENETRATE in atk_type:return
        p = target.pos_gameboard
        for x, y in list(filter(lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                                [(p[0] - 1, p[1] - 1), (p[0] - 1, p[1]), (p[0] - 1, p[1] + 1),
                                 (p[0], p[1] - 1), (p[0], p[1] + 1),
                                 (p[0] + 1, p[1] - 1), (p[0] + 1, p[1]), (p[0] + 1, p[1] + 1)])):
            t=game_board.gameBoard[x][y]
            target.attack(2, t, [TAG_BUFF])


