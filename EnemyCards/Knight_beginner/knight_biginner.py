import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos

if TYPE_CHECKING:
    from playerCard import PlayerCard

class Sortie(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board)
        self.name="돌격"
        self.explaination = [
            "적을 만날 때까지 앞으로 가면서 타격한다. "
        ]
        self.skill_image_path = "./PlayerCards/Astin/astin_card.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: p != pos,
            [(pos[0], 1),
             (pos[0], 5),
             (1, pos[1]),
             (5, pos[1])]
        ))

    def atk_range(self, caster_pos, pos):
        result = []
        if pos[0] == 1 and caster_pos[0] != 1:
            while caster_pos[0] > 1:
                caster_pos = (caster_pos[0] - 1, caster_pos[1])
                result.append(caster_pos)
        elif pos[0] == 5 and caster_pos[0] != 5:
            while caster_pos[0] < 5:
                caster_pos = (caster_pos[0] + 1, caster_pos[1])
                result.append(caster_pos)
        elif pos[1] == 1 and caster_pos[1] != 1:
            while caster_pos[1] > 1:
                caster_pos = (caster_pos[0], caster_pos[1] - 1)
                result.append(caster_pos)
        elif pos[1] == 5 and caster_pos[1] != 5:
            while caster_pos[1] < 5:
                caster_pos = (caster_pos[0], caster_pos[1] + 1)
                result.append(caster_pos)
        return result

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target_pos in targets_pos:
            if self.game_board.gameBoard[target_pos[0]][target_pos[1]].team==FLAG_EMPTY:
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]], self.game_board.gameBoard[target_pos[0]][
                    target_pos[1]] = (
                    self.game_board.gameBoard[target_pos[0]][target_pos[1]],
                    self.game_board.gameBoard[caster_pos[0]][caster_pos[1]]
                )
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_center, \
                self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_center = (
                    self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_center,
                    self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_center
                )
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].update_location()
                self.game_board.gameBoard[target_pos[0]][target_pos[1]].update_location()
            else:
                caster.attack(1, self.game_board.gameBoard[target_pos[0]][target_pos[1]], "normal attack")
                for observer in caster.observers_attack[::-1]:
                    observer.attack_event(self, [self.game_board.gameBoard[target_pos[0]][target_pos[1]]], self.game_board, "normal attack")
                break

class Shield(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "기사의 보호막", "./PlayerCards/Tania/burn.png")
        game_board.register_turnover(self)

    def hit_buff(self, caster, target, damage: int, atk_type: str):
        if damage>0:
            damage-=1
            self.remove()
        return damage

class PrepareDefence(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board)
        self.name = "방어 준비"
        self.explaination = [
            "자신의 몸에 기사의 보호막을 두르고 다음 공격에서 받는 피해를 1 줄인다. "
        ]
        self.skill_image_path = "./PlayerCards/Astin/astin_card.png"
    def execute_range(self, pos):
        return [pos]
    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        Shield(caster, caster.game_board)
