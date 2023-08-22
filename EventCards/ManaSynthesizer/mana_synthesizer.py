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


class ManaSynthesizerBuff(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, 0, game_board, "마나 합성", "./EventCards/ManaSynthesizer/mana_synthesizer_buff.png")
        game_board.register_turnstart(self)
        character.register_hit(self)

    def hit_event(self, caster, target, game_board, atk_type, damage):
        self.use_num=min(3, self.use_num+1)

    def turnstart_event(self, game_board):
        if self.use_num>=3:
            self.game_board.cost.plus(3)
            self.remove()

class ManaSynthesizer(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_ManaSynthesizer],
                         game_board, group, ManaSynthesizer)

    def execute_range_one(self):
        result = []
        for i in range(1, 6):
            for j in range(1, 6):
                if self.game_board.gameBoard[i][j].team == FLAG_PLAYER_TEAM:
                    result.append((i, j))
        return result

    def execute_one(self, pos, target):
        self.game_board.cost.minus(self.cost)
        ManaSynthesizerBuff(target, self.game_board)