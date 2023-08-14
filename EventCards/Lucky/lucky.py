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


class LuckyBuff(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, 1, game_board, "행운", "./EventCards/Lucky/lucky_buff.png")
        game_board.register_turnover(self)

    def hit_buff(self, caster, target, damage: int, atk_type):
        if random.randint(0, 1)==0:
            return damage
        a = random.random() * 2 - 1
        b = random.random() * 2 - 1
        def func_temp(scr):
            for _ in range(15):
                def temp_func(screen, pos, i):
                    damage_font = pygame.font.Font("./D2Coding.ttf", 20)
                    damage_text = damage_font.render("회피", True, "#FFFFFF", "#000000")
                    damage_text_rect = damage_text.get_rect(
                        center=(pos[0], pos[1] - 60 + 50 / i * 2))
                    screen.blit(damage_text, damage_text_rect)

                motion_draw.add_motion(temp_func, _, ((target.pos_center[0] + a * 10, target.pos_center[1] + b * 10), _ + 1))
        motion_draw.add_motion(func_temp, 0, ())
        return 0

    def turnover_event(self, game_board):
        self.used(1)

class Lucky(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_Lucky],
                         game_board, group, Lucky)

    def execute_range_one(self):
        result = []
        for i in range(1, 6):
            for j in range(1, 6):
                if self.game_board.gameBoard[i][j].team == FLAG_PLAYER_TEAM:
                    result.append((i, j))
        return result

    def execute_one(self, pos, target):
        self.game_board.cost.minus(self.cost)
        LuckyBuff(target, self.game_board)