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

boom = pygame.image.load("./EventCards/BombThrowing/boom.png")


class Bomb(Summons):
    def __init__(self, pos, game_board, group):
        super().__init__(1, transform_pos(pos), game_board, group, None,
                         "./EventCards/BombThrowing/bomb_throwing.png", pos)

    def die(self):
        p = self.pos_gameboard
        size_change = [100, 130, 160, 200, 300, 440, 430, 400]
        for ii in range(8):
            motion_draw.add_motion(
                lambda screen, size: screen.blit(pygame.transform.scale(wizard_energy_ball_boom, (size, size)), (
                    self.pos_center[0] - size / 2, self.pos_center[1] - size / 2)), ii, (size_change[ii],))
        for t_pos in [(p[0] - 1, p[1] - 1), (p[0] - 1, p[1]), (p[0] - 1, p[1] + 1),
                      (p[0], p[1] - 1), (p[0], p[1]), (p[0], p[1] + 1),
                      (p[0] + 1, p[1] - 1), (p[0] + 1, p[1]), (p[0] + 1, p[1] + 1)]:
            motion_draw.add_motion(
                lambda screen, t_p: self.game_board.gameBoard[t_p[0]][t_p[1]].hit(3, self, [TAG_SUMMON, TAG_PYRO]),
                6, (t_pos,))
        super().die()


class BombThrowing(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_BombThrowing],
                         game_board, group, BombThrowing)

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
