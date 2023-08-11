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


class Bomb(Summons):
    def __init__(self, pos, game_board, group):
        super().__init__(1, transform_pos(pos), game_board, group, None,
                         "./EventCards/BombThrowing/bomb_throwing.png", pos)

    def die(self):
        print(self.pos_center, self.pos_gameboard)
        super().die()
        x, y = self.pos_gameboard
        for target_pos in list(filter(lambda pos: 0 < pos[0] < 6 and 0 < pos[1] < 6,
                               [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                                (x, y - 1), (x, y + 1),
                                (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)])):
            target=self.game_board.gameBoard[target_pos[0]][target_pos[1]]
            target.hit(4, self, [TAG_SUMMON, TAG_PYRO])


class BombThrowing(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_BombThrowing],
                         game_board, group)
        self.group=group

    def execute_range_one(self):
        result = []
        for i in range(1, 6):
            for j in range(1, 6):
                if self.game_board.gameBoard[i][j].team == FLAG_EMPTY:
                    result.append((i, j))
        return result

    def execute_one(self, pos, target):
        self.game_board.cost.minus(self.cost)
        self.game_board.add_summons(pos, Bomb(pos, self.game_board, self.group))
