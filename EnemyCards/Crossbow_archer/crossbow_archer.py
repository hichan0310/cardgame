import random

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
import pygame
from math import atan, sin, cos, sqrt, pi
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard
    from gameMap import GameMap

continueous_firing=pygame.image.load("./EnemyCards/Crossbow_archer/continuous_firing.png")
continueous_firing_preview=pygame.image.load("./EnemyCards/Crossbow_archer/preview/continuous_firing.png")
penetrate_arrow_preview=pygame.image.load("./EnemyCards/Crossbow_archer/preview/penetrate_arrow.png")
arrow=pygame.image.load("./EnemyCards/Archer_beginner/arrow.png")

class PenetrateArrow(Skill):
    def __init__(self, game_board: "GameMap"):
        super().__init__(0, game_board, [TAG_NORMAL_ATTACK, TAG_PENETRATE])
        self.name = "관통하는 화살"
        self.explaination = [
            "적군 1명에게 3의 관통 피해를 가한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = None
        self.observer_addition_arrow = []

    def execute(self, caster: "EnemyCard", targets: "list[PlayerCard]", caster_pos: tuple[int, int],
                targets_pos: list[tuple[int, int]], execute_pos):
        img_arrow = pygame.transform.scale(arrow, (100, 30))
        i = 1
        for target_pos, target in zip(targets_pos, targets):
            for observer in self.observer_addition_arrow[::-1]:
                motion_draw.add_motion(lambda screen, obs: obs.active_event(caster_pos, target_pos), 2 * i, (observer,))
                i += 1
            p1 = transform_pos(caster_pos)
            p2 = transform_pos(target_pos)
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            angle = -atan(dy / (dx - 0.00001)) / pi * 180
            if dx > 0: angle += 180
            angle += 180
            img_arrow = pygame.transform.rotate(img_arrow, angle)
            size = img_arrow.get_size()
            i = 0
            while (80 * i) ** 2 < dx ** 2 + dy ** 2:
                def temp(screen, i):
                    t = i * 80 / sqrt(dx ** 2 + dy ** 2)
                    img_pos = (p1[0] + t * dx - size[0] / 2, p1[1] + t * dy - size[1] / 2)
                    screen.blit(img_arrow, img_pos)

                motion_draw.add_motion(temp, i, (i,))
                i += 1
            motion_draw.add_motion(lambda *_: caster.attack(3, target, self.atk_type), i, tuple())
        for observer in caster.observers_attack[::-1]:
            observer.attack_event(self, targets, self.game_board, self.atk_type)

    def register_active(self, observer):
        self.observer_addition_arrow.append(observer)
        observer.observing(self.observer_addition_arrow)


class ContinuousFiringBuff(Buff):
    def __init__(self, character: "PlayerCard", count, game_board):
        super().__init__(character, count, game_board, "연속 발사", "./EnemyCards/Crossbow_archer/multy_shot.png")
        character.skills[0].register_active(self)
        game_board.register_turnover(self)

    def active_event(self, caster_pos, target_pos):
        img_arrow = pygame.transform.scale(arrow, (80, 24))
        p1 = transform_pos(caster_pos)
        p2 = transform_pos(target_pos)
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = -atan(dy / (dx - 0.00001)) / pi * 180
        if dx > 0: angle += 180
        angle += 180
        img_arrow = pygame.transform.rotate(img_arrow, angle)
        size = img_arrow.get_size()
        i = 0
        while (80 * i) ** 2 < dx ** 2 + dy ** 2:
            def temp(screen, i):
                t = i * 80 / sqrt(dx ** 2 + dy ** 2)
                img_pos = (p1[0] + t * dx - size[0] / 2, p1[1] + t * dy - size[1] / 2)
                screen.blit(img_arrow, img_pos)

            motion_draw.add_motion(temp, i, (i,))
            i += 1
        motion_draw.add_motion(
            lambda *_: self.target.attack(2, self.game_board.gameBoard[target_pos[0]][target_pos[1]],
                                          [TAG_NORMAL_ATTACK, TAG_PENETRATE])
            , i, tuple()
        )


class ContinuousFiring(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_SKILL, TAG_BUFF])
        self.name = "연속 발사"
        self.explaination = [
            "3턴동안 자신에게 일반 공격을 하면 추가 화살을 발사하는 버프를 건다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = None

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        ContinuousFiringBuff(caster, 3, self.game_board)
        x, y = transform_pos(caster_pos)
        for i in range(20):
            size = i * 20
            img_temp = pygame.transform.scale(continueous_firing, (2*size, size))
            img_temp.set_alpha(min((20 - i) * 15, 255))
            motion_draw.add_motion(lambda screen, image, size: screen.blit(image, (x - size, y - size / 2)), i,
                                   (img_temp, size))


class AI_Crossbow:
    def __init__(self, game_board, character: "EnemyCard"):
        self.game_board = game_board
        self.character = character
        self.turn=0

    def execute(self, pos):
        if self.turn % 2==1:
            self.turn += random.randint(0, 1)
            target = random.choice(self.game_board.players)
            target_pos = target.pos_gameboard

            for i in range(15):
                motion_draw.add_motion(lambda screen, a: screen.blit(penetrate_arrow_preview, (1 - 1.4 ** a, 0)), 14 - i, (i,))
            for i in range(5):
                motion_draw.add_motion(lambda screen: screen.blit(penetrate_arrow_preview, (0, 0)), 15 + i, tuple())
            motion_draw.add_motion(lambda screen: self.character.skills[0].execute(self.character, [target],
                                                                                   self.character.pos_gameboard,
                                                                                   [target_pos], target_pos), 20, tuple())
        else:
            self.turn += 1
            for i in range(15):
                motion_draw.add_motion(lambda screen, a: screen.blit(continueous_firing_preview, (1 - 1.4 ** a, 0)), 14 - i, (i,))
            for i in range(5):
                motion_draw.add_motion(lambda screen: screen.blit(continueous_firing_preview, (0, 0)), 15 + i, tuple())
            motion_draw.add_motion(
                lambda screen: self.character.skills[1].execute(self.character, [self.character],
                                                                self.character.pos_gameboard,
                                                                [self.character.pos_gameboard],
                                                                self.character.pos_gameboard), 20, tuple()
            )
