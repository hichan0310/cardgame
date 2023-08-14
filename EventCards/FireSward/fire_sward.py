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


class Overheating(Buff):
    def __init__(self, character: "PlayerCard", game_board):
        super().__init__(character, -1, game_board, "과열", "./EventCards/FireSward/overheating.png")
        character.register_attack(self)
        self.overheat = 0

    def attack_event(self, caster, targets, game_board, atk_type):
        if TAG_SKILL in atk_type:
            self.overheat += 1
        while True:
            if self.overheat >= 3:
                self.target.specialSkill.gage_up(1)
                self.game_board.cost.plus(1)
                self.overheat -= 3
            else:
                return


class FireSward(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_FireSward],
                         game_board, group, FireSward)

    def execute_range_one(self):
        result = []
        for i in range(1, 6):
            for j in range(1, 6):
                if self.game_board.gameBoard[i][j].team == FLAG_PLAYER_TEAM and "과열" not in list(
                        map(lambda a: a.name, self.game_board.gameBoard[i][j].buff)):
                    result.append((i, j))
        return result

    def execute_one(self, pos, target):
        self.game_board.cost.minus(self.cost)
        Overheating(target, self.game_board)
