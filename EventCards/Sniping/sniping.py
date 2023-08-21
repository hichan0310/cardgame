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

class Sniping(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_Sniping],
                         game_board, group, Sniping)

    def execute_range_one(self):
        result = []
        for i in range(1, 6):
            for j in range(1, 6):
                if self.game_board.gameBoard[i][j].team != FLAG_EMPTY:
                    result.append((i, j))
        return result

    def execute_one(self, pos, target):
        self.game_board.cost.minus(self.cost)
        try:
            if target.hp<=7:
                target.hit(target.hp-1, None, [TAG_BUFF, TAG_PENETRATE])
            else:
                target.hit(7, None, [TAG_BUFF, TAG_PENETRATE])
        except:
            target.hit(7, None, [TAG_BUFF, TAG_PENETRATE])
