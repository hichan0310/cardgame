import random

import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos
from EnemyCards.Knight_beginner.knight_beginner import Shield

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard


class ShieldOfWrath(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_NORMAL_ATTACK])
        self.name = "분노의 방패"
        self.explaination = [
            "바로 앞의 넓은 영역에 2의 광역 피해를 가한다. ",
            "자신의 몸에 2번의 피격까지 유지되는 기사의 보호막을 두른다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/fast_growth.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def atk_range(self, caster_pos, pos):
        if caster_pos[0] < pos[0]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1] + 1),
                 (pos[0], pos[1]), (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
            ))
        if caster_pos[0] > pos[0]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1] + 1),
                 (pos[0], pos[1]), (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
            ))
        if caster_pos[1] < pos[1]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0], pos[1]), (pos[0] - 1, pos[1]),
                 (pos[0] + 1, pos[1] + 1), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1] + 1)]
            ))
        if caster_pos[1] > pos[1]:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0], pos[1]), (pos[0] - 1, pos[1]),
                 (pos[0] + 1, pos[1] - 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1] - 1)]
            ))

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        for target in targets:
            caster.attack(2, target, self.atk_type)
        Shield(caster, 2, caster.game_board)
        img = pygame.image.load("./EnemyCards/Shielder/rage_shield.png")
        x, y = transform_pos(caster_pos)
        for i in range(20):
            size = i * 20
            img_temp = pygame.transform.scale(img, (size, size))
            img_temp.set_alpha(min((20 - i) * 15, 255))
            motion_draw.add_motion(lambda screen, image, size: screen.blit(image, (x - size / 2, y - size / 2)), i,
                                   (img_temp, size))


class CounterAttackBuff(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "반격", "./EnemyCards/Shielder/counter_attack.png")
        character.register_hit(self)
        game_board.register_turnover(self)

    def hit_event(self, caster: "PlayerCard", target: "PlayerCard", game_board, atk_type):
        if TAG_PENETRATE in atk_type: return
        p = target.pos_gameboard
        for x, y in list(filter(lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                                [(p[0] - 1, p[1] - 1), (p[0] - 1, p[1]), (p[0] - 1, p[1] + 1),
                                 (p[0], p[1] - 1), (p[0], p[1] + 1),
                                 (p[0] + 1, p[1] - 1), (p[0] + 1, p[1]), (p[0] + 1, p[1] + 1)])):
            t = game_board.gameBoard[x][y]
            target.attack(2 if t.team==FLAG_PLAYER_TEAM else 1, t, [TAG_BUFF, TAG_PENETRATE])
        image=pygame.image.load("./EnemyCards/Shielder/counter.png")
        image=pygame.transform.scale(image, (360, 360))
        motion_draw.add_motion(
            lambda screen: screen.blit(image, (target.pos_center[0] - 180, target.pos_center[1] - 180)), 1, tuple()
        )
        motion_draw.add_motion(
            lambda screen: screen.blit(image, (target.pos_center[0] - 180, target.pos_center[1] - 180)), 2, tuple()
        )
        motion_draw.add_motion(
            lambda screen: screen.blit(image, (target.pos_center[0] - 180, target.pos_center[1] - 180)), 3, tuple()
        )
        motion_draw.add_motion(
            lambda screen: screen.blit(image, (target.pos_center[0] - 180, target.pos_center[1] - 180)), 4, tuple()
        )

    def turnover_event(self, game_board):
        self.used(1)


class CounterAttack(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_BUFF, TAG_SKILL])
        self.name = "반격"
        self.explaination = [
            "3턴동안 자신에게 피해를 받으면 주변에 2의 관통 피해를 가하는 버프를 부여한다. ",
            "이 공격은 관통 공격에 발동되지 않는다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/fast_growth.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        CounterAttackBuff(caster, 3, self.game_board)
        img = pygame.image.load("./EnemyCards/Shielder/rage_shield.png")
        x, y = transform_pos(caster_pos)
        for i in range(20):
            size = i * 20
            img_temp = pygame.transform.scale(img, (size, size))
            img_temp.set_alpha(min((20 - i) * 15, 255))
            motion_draw.add_motion(lambda screen, image, size: screen.blit(image, (x - size / 2, y - size / 2)), i,
                                   (img_temp, size))


class AI_Shielder:
    def __init__(self, game_board, character: "EnemyCard"):
        self.game_board = game_board
        self.character = character
        self.counter = 2
        self.rage = 2

    def execute(self, pos):
        if random.randint(1, self.counter + self.rage) < self.rage:
            skill = self.character.skills[0]
            exe_pos = skill.execute_range(pos)
            best = (exe_pos[0], 0)
            for exep in skill.execute_range(pos):
                atk = skill.atk_range(pos, exep)
                now = len(list(filter(lambda p: self.game_board.gameBoard[p[0]][p[1]].team != FLAG_EMPTY and
                                                self.game_board.gameBoard[p[0]][p[1]].team != FLAG_ENEMY_TEAM, atk)))
                if now > best[1]:
                    best = (exep, now)
            best_pos = best[0]
            best_pos_tar = skill.atk_range(pos, best_pos)
            img = pygame.image.load("./EnemyCards/Shielder/preview/shield_of_wrath.png")
            for i in range(15):
                motion_draw.add_motion(lambda screen, a: screen.blit(img, (1 - 1.4 ** a, 0)), 14 - i, (i,))
            for i in range(5):
                motion_draw.add_motion(lambda screen: screen.blit(img, (0, 0)), 15 + i, tuple())
            motion_draw.add_motion(lambda screen: skill.execute(self.character,
                                                                list(map(
                                                                    lambda p: self.game_board.gameBoard[p[0]][p[1]],
                                                                    best_pos_tar
                                                                )), pos, best_pos_tar, best_pos), 20, tuple())
        else:
            skill=self.character.skills[1]
            img = pygame.image.load("./EnemyCards/Shielder/preview/counterattack.png")
            for i in range(15):
                motion_draw.add_motion(lambda screen, a: screen.blit(img, (1 - 1.4 ** a, 0)), 14 - i, (i,))
            for i in range(5):
                motion_draw.add_motion(lambda screen: screen.blit(img, (0, 0)), 15 + i, tuple())
            motion_draw.add_motion(lambda scr:skill.execute(self.character, [self.character], pos, [pos], pos), 20, tuple())

