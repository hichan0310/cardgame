import random

import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard

prepare_defence_preview = pygame.image.load("./EnemyCards/Knight_beginner/preview/prepare_defence.png")
sortie_preview = pygame.image.load("./EnemyCards/Knight_beginner/preview/sortie.png")


class Sortie(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_NORMAL_ATTACK])
        self.name = "돌격"
        self.explaination = [
            "적을 만날 때까지 앞으로 가면서 타격한다. ",
            "적을 만나면 검을 휘둘러서 바로 옆 상대에게 피해를 준다. "
        ]
        self.skill_image_path = "./EnemyCards/Knight_beginner/sortie.png"

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
        for target_pos in targets_pos:
            if self.game_board.gameBoard[target_pos[0]][target_pos[1]].team == FLAG_PLAYER_TEAM:
                caster.attack(1, self.game_board.gameBoard[target_pos[0]][target_pos[1]], [TAG_NORMAL_ATTACK])
                for observer in caster.observers_attack[::-1]:
                    observer.attack_event(self, targets, self.game_board, [TAG_NORMAL_ATTACK])
                break
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
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_gameboard, \
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_gameboard = (
                self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_gameboard,
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_gameboard
            )
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].update_location()
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].update_location()
            caster_pos = target_pos


class Shield(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "기사의 보호막", "./EnemyCards/Knight_beginner/shield.png")
        game_board.register_turnover(self)

    def hit_buff(self, caster, target, damage: int, atk_type: str):
        if damage > 0:
            damage -= 1
            self.remove()
        return damage

    def turnover_event(self, game_board):
        self.used(1)


class PrepareDefence(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_SKILL, TAG_BUFF])
        self.name = "회피"
        self.explaination = [
            "빠르게 회피하며 한 칸 이동한다. 랜덤한 방향으로 이동한다. ",
            "자신의 몸에 보호막을 두르고 다음 공격에서 받는 피해를 1 줄인다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./EnemyCards/Knight_beginner/prepare_defence.png"

    def execute_range(self, pos):
        return [pos]

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        pos = random.choice(list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(caster_pos[0] + 1, caster_pos[1]),
             (caster_pos[0] - 1, caster_pos[1]),
             (caster_pos[0], caster_pos[1] + 1),
             (caster_pos[0], caster_pos[1] - 1)]
        )))
        self.game_board.move_card(caster_pos, pos)
        Shield(caster, 2, caster.game_board)


class AI_KnightBiginner:
    def __init__(self, game_board, character: "EnemyCard"):
        self.game_board = game_board
        self.character = character

    def execute(self, pos):
        temp = pos[0] + 1
        while temp < 6:
            if self.game_board.gameBoard[temp][pos[1]].team == FLAG_PLAYER_TEAM:
                targets = list(map(lambda a: self.game_board.gameBoard[a[0]][a[1]],
                                   self.character.skills[0].atk_range(pos, (5, pos[1]))))

                def temp(*_):
                    self.character.skills[0].execute(self.character, targets, pos,
                                                     self.character.skills[0].atk_range(pos, (5, pos[1])),
                                                     (5, pos[1]))

                motion_draw.add_motion(temp, 20, ())
                for i in range(15):
                    motion_draw.add_motion(lambda screen, a: screen.blit(sortie_preview, (1 - 1.4 ** a, 0)), 14 - i,
                                           (i,))
                for i in range(5):
                    motion_draw.add_motion(lambda screen: screen.blit(sortie_preview, (0, 0)), 15 + i, ())
                return
            if self.game_board.gameBoard[temp][pos[1]].team != FLAG_EMPTY:
                break
            temp += 1
        temp = pos[1] + 1
        while temp < 6:
            if self.game_board.gameBoard[pos[0]][temp].team == FLAG_PLAYER_TEAM:
                targets = list(map(lambda a: self.game_board.gameBoard[a[0]][a[1]],
                                   self.character.skills[0].atk_range(pos, (pos[0], 5))))

                def temp(*_):
                    self.character.skills[0].execute(self.character, targets, pos,
                                                     self.character.skills[0].atk_range(pos, (pos[0], 5)),
                                                     (5, pos[1]))

                motion_draw.add_motion(temp, 20, ())
                for i in range(15):
                    motion_draw.add_motion(lambda screen, a: screen.blit(sortie_preview, (1 - 1.4 ** a, 0)),
                                           14 - i, (i,))
                for i in range(5):
                    motion_draw.add_motion(lambda screen: screen.blit(sortie_preview, (0, 0)), 15 + i, ())
                return
            if self.game_board.gameBoard[pos[0]][temp].team != FLAG_EMPTY:
                break
            temp += 1
        temp = pos[0] - 1
        while temp > 0:
            if self.game_board.gameBoard[temp][pos[1]].team == FLAG_PLAYER_TEAM:
                targets = list(map(lambda a: self.game_board.gameBoard[a[0]][a[1]],
                                   self.character.skills[0].atk_range(pos, (1, pos[1]))))

                def temp(*_):
                    self.character.skills[0].execute(self.character, targets, pos,
                                                     self.character.skills[0].atk_range(pos, (1, pos[1])),
                                                     (5, pos[1]))

                motion_draw.add_motion(temp, 20, ())
                for i in range(15):
                    motion_draw.add_motion(lambda screen, a: screen.blit(sortie_preview, (1 - 1.4 ** a, 0)),
                                           14 - i, (i,))
                for i in range(5):
                    motion_draw.add_motion(lambda screen: screen.blit(sortie_preview, (0, 0)), 15 + i, ())
                return
            if self.game_board.gameBoard[temp][pos[1]].team != FLAG_EMPTY:
                break
            temp -= 1
        temp = pos[1] - 1
        while temp > 0:
            if self.game_board.gameBoard[pos[0]][temp].team == FLAG_PLAYER_TEAM:
                targets = list(map(lambda a: self.game_board.gameBoard[a[0]][a[1]],
                                   self.character.skills[0].atk_range(pos, (pos[0], 1))))

                def temp(*_):
                    self.character.skills[0].execute(self.character, targets, pos,
                                                     self.character.skills[0].atk_range(pos, (pos[0], 1)),
                                                     (5, pos[1]))

                motion_draw.add_motion(temp, 20, ())
                for i in range(15):
                    motion_draw.add_motion(lambda screen, a: screen.blit(sortie_preview, (1 - 1.4 ** a, 0)),
                                           14 - i, (i,))
                for i in range(5):
                    motion_draw.add_motion(lambda screen: screen.blit(sortie_preview, (0, 0)), 15 + i, ())
                return
            if self.game_board.gameBoard[pos[0]][temp].team != FLAG_EMPTY:
                break
            temp -= 1

        def temp(*_):
            self.character.skills[1].execute(self.character, "not used", pos,
                                             "not used",
                                             "not used")

        motion_draw.add_motion(temp, 20, ())
        for i in range(15):
            motion_draw.add_motion(lambda screen, a: screen.blit(prepare_defence_preview, (1 - 1.4 ** a, 0)),
                                   14 - i, (i,))
        for i in range(5):
            motion_draw.add_motion(lambda screen: screen.blit(prepare_defence_preview, (0, 0)), 15 + i, ())
