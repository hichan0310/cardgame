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


class WarpGate(EventCard):
    def __init__(self, pos_center, game_board: "GameMap", group):
        super().__init__(pos_center, event_card_info[EVENT_WarpGate],
                         game_board, group, WarpGate)

    def execute_range_two(self):
        return [(i, j) for i in range(1, 6) for j in range(1, 6)], [(i, j) for i in range(1, 6) for j in range(1, 6)]

    def execute_two(self, pos1, pos2, target1, target2):
        self.game_board.cost.minus(self.cost)
        self.game_board.gameBoard[pos1[0]][pos1[1]], self.game_board.gameBoard[pos2[0]][pos2[1]] = (
            self.game_board.gameBoard[pos2[0]][pos2[1]],
            self.game_board.gameBoard[pos1[0]][pos1[1]]
        )
        self.game_board.gameBoard[pos1[0]][pos1[1]].pos_center, self.game_board.gameBoard[pos2[0]][
            pos2[1]].pos_center = (
            self.game_board.gameBoard[pos2[0]][pos2[1]].pos_center,
            self.game_board.gameBoard[pos1[0]][pos1[1]].pos_center
        )
        self.game_board.gameBoard[pos1[0]][pos1[1]].pos_gameboard, self.game_board.gameBoard[pos2[0]][
            pos2[1]].pos_gameboard = (
            self.game_board.gameBoard[pos2[0]][pos2[1]].pos_gameboard,
            self.game_board.gameBoard[pos1[0]][pos1[1]].pos_gameboard
        )
        self.game_board.gameBoard[pos1[0]][pos1[1]].update_location()
        self.game_board.gameBoard[pos2[0]][pos2[1]].update_location()
