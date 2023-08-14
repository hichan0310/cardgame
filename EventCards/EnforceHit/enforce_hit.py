import random

import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos
from eventCard import EventCard
from characters import *
from summons import Summons

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from gameMap import GameMap


class EnforceHitBuff(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, 3, game_board, "강화 타격", "./EventCards/EnforceHit/enforce_hit.png")
        game_board.register_turnover(self)

    def atk_buff(self, caster, target, damage: int, atk_type):
        print(damage)
        return (damage*3)//2

    def turnover_event(self, game_board):
        self.used(1)

class EnforceHit(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_EnforceHit],
                         game_board, group, EnforceHit)

    def execute_range_one(self):
        result = []
        for i in range(1, 6):
            for j in range(1, 6):
                if self.game_board.gameBoard[i][j].team == FLAG_PLAYER_TEAM:
                    result.append((i, j))
        return result

    def execute_one(self, pos, target):
        self.game_board.cost.minus(self.cost)
        EnforceHitBuff(target, self.game_board)