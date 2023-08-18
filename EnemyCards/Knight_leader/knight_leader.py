import random

import pygame.image

from skill import Skill, SpecialSkill
from summons import Summons
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos
from EnemyCards.Knight_beginner.knight_beginner import Shield
from EnemyCards.Shielder.shielder import CounterAttackBuff
import random

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard


def warp_two(self, pos1, pos2):
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


energy_ball = pygame.transform.scale(pygame.image.load("./EnemyCards/Wizard_beginner/energy_ball.png"), (100, 75))
energy_ball_boom = pygame.image.load("./EnemyCards/Wizard_beginner/energy_bomb.png")


class StrongHit(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_NORMAL_ATTACK])
        self.name = "강타"
        self.explaination = [
            "검을 강하게 내려찍고 적 전체에게 10의 피해를 준다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./EnemyCards/Shielder/shield_of_wrath.png"

    def execute_range(self, pos):
        return [pos]

    def atk_range(self, caster_pos, pos):
        return [(i + 1, 1) for i in range(5)] + \
               [(i + 1, 2) for i in range(5)] + \
               [(i + 1, 3) for i in range(5)] + \
               [(i + 1, 4) for i in range(5)] + \
               [(i + 1, 5) for i in range(5)]

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        for target in self.game_board.players:
            caster.attack(10, target, self.atk_type)


class Shield(Buff):
    def __init__(self, character, game_board, amount):
        super().__init__(character, amount, game_board, "보호막", "./EnemyCards/Knight_beginner/shield.png")
        self.amount = amount

    def hit_buff(self, caster, target, damage: int, atk_type):
        if damage < self.amount:
            self.used(damage)
            return 0
        else:
            self.used(self.amount)
            return damage - self.amount


class SwordDestroyed(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, 1, game_board, "검 파괴", "./EnemyCards/Knight_beginner/shield.png")
        game_board.register_turnover(self)

    def turnover_event(self, game_board):
        self.used(1)


class SwordPhantom(Summons):
    def __init__(self, pos, game_board, group, knight, real):
        super().__init__(4, transform_pos(pos), game_board, group, knight, "./EnemyCards/Knight_leader/summon_sward.png", pos)
        self.name = "sward phantom"
        self.team=FLAG_SUMMONS
        if real:
            game_board.register_turnstart(self)

    def atk_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] + 1),
             (pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1),
             (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + 1), ]
        ))

    def turnstart_event(self, game_board):
        def energyball(scr, caster, target):
            p1 = caster.pos_center
            p2 = target.pos_center
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            angle = -atan(dy / (dx - 0.00001)) / pi * 180
            if dx > 0: angle += 180
            angle += 180
            img_arrow = pygame.transform.rotate(energy_ball, angle)
            size = img_arrow.get_size()
            i = 0
            while (50 * i) ** 2 < dx ** 2 + dy ** 2:
                def temp(scr, i):
                    t = i * 50 / sqrt(dx ** 2 + dy ** 2)
                    img_pos = (p1[0] + t * dx - size[0] / 2, p1[1] + t * dy - size[1] / 2)
                    scr.blit(img_arrow, img_pos)

                motion_draw.add_motion(temp, i, (i,))
                i += 1
            target_pos = target.pos_center
            size_change = [100, 130, 160, 200, 300, 440, 430, 400]
            for ii in range(8):
                motion_draw.add_motion(
                    lambda sc, size: sc.blit(pygame.transform.scale(energy_ball_boom, (size, size)), (
                        target_pos[0] - size / 2, target_pos[1] - size / 2)), ii + i, (size_change[ii],))
            for x, y in self.atk_range(target.pos_gameboard):
                if self.game_board.gameBoard[x][y].team == FLAG_PLAYER_TEAM or self.game_board.gameBoard[x][y].team == FLAG_SUMMONS:
                    motion_draw.add_motion(lambda s, xx, yy: self.game_board.gameBoard[xx][yy].hit(1, self, [TAG_SUMMON]), i + 6,
                                           (x, y))
        for target in game_board.players:
            motion_draw.add_motion(energyball, 0, (self, target))

    def hit(self, damage, caster, atk_type):
        if self.dead:
            return
        self.count -= 1
        if self.count == 0:
            if caster.team == FLAG_PLAYER_TEAM:
                for target in self.game_board.players:
                    Shield(target, self.game_board, 8)
            self.die()


class ResonanceSword(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_SUMMON])
        self.name = "검의 울림"
        self.explaination = [
            "에너지를 검에 담는다. ",
            "이 과정에서 맵의 무작위 위치에 4개의 검의 환영을 소환한다. ",
            "4개의 검의 환영 중 1개만 진짜이다. ",
            "검의 환령은 턴이 시작될 때 적에게 에너지볼을 날리고 진짜 검의 환영만 피해를 준다. ",
            "진짜 검의 환영을 파괴할 경우 파괴한 팀의 모든 아군에게 8의 보호막 버프를 준다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./EnemyCards/Knight_leader/resonance_sword.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        arr = [(i, j) for i in range(1, 6) for j in range(1, 6) if self.game_board.gameBoard[i][j].team == FLAG_EMPTY]
        random.shuffle(arr)
        real = True
        for pos in arr[:4]:
            self.game_board.add_summons(pos, SwordPhantom(pos, self.game_board, self.game_board.group, caster, real))
            real = False


class GuardianShieldBuff(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, 3, game_board, "수호신의 방패", "./PlayerCards/Petra/skill_image/summon_turret.png")
        game_board.register_turnstart(self)

    def turnstart_event(self, game_board):
        self.used(1)

    def hit_buff(self, caster, target, damage: int, atk_type):
        return 0


class GuardianShield(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_BUFF, TAG_SPECIAL_SKILL])
        self.name = "수호신의 방패"
        self.explaination = [
            "자신에게 2턴간 모든 데미지를 무효화하는 버프를 건다.",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./EnemyCards/Knight_leader/guardian_shield.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        GuardianShieldBuff(caster, self.game_board)


class LastSkillBuff(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, 2, game_board, "마지막 일격", "./PlayerCards/Petra/skill_image/summon_turret.png")
        self.over3_attack = 0
        character.register_hit(self)
        game_board.register_turnstart(self)

    def turnstart_event(self, game_board):
        self.used(1)

    def remove(self):
        super().remove()
        if self.over3_attack < 2:
            for x, y in [(i, j) for i in range(1, 6) for j in range(1, 6) if (i, j) != self.target.pos_gameboard]:
                target = self.game_board.gameBoard[x][y]
                self.target.attack(8, target, [TAG_SPECIAL_SKILL])
                self.target.heal(10)
        else:
            for x, y in [(i, j) for i in range(1, 6) for j in range(1, 6) if (i, j) != self.target.pos_gameboard]:
                target = self.game_board.gameBoard[x][y]
                self.target.attack(5, target, [TAG_SPECIAL_SKILL])
                motion_draw.add_motion(lambda scr: self.target.die(), 10, ())


class LastSkill(Skill):
    def __init__(self, game_board):
        super().__init__(0, game_board, [TAG_BUFF, TAG_SPECIAL_SKILL])
        self.name = "발악 패턴"
        self.explaination = [
            "hp 10이하가 되면 자신에게 3개의 반격 버프를 걸고 맵의 중앙으로 워프 게이트를 타고 이동한다. ",
            "이 다음 턴에 3 이상의 데미지가 2번 이상 들어가면 맵 전체에 5의 피해를 가하고 죽는다. ",
            "만약 2번 이상 들어가지 않으면 맵 전체에 8의 피해를 가하고 체력 10을 회복한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./EnemyCards/Knight_leader/last_skill.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        CounterAttackBuff(caster, 1, self.game_board)
        CounterAttackBuff(caster, 1, self.game_board)
        CounterAttackBuff(caster, 1, self.game_board)
        # tmp = WarpGate((0, 0), self.game_board, self.game_board.group)
        # tmp.execute_two(caster.pos_gameboard, (3, 3),
        #                 self.game_board.gameBoard[caster_pos[0]][caster_pos[1]], self.game_board.gameBoard[3][3])
        # tmp.kill()
        warp_two(self, caster_pos, (3, 3))
        LastSkillBuff(caster, self.game_board)


class AI_KnightLeader:
    def __init__(self, game_board, character):
        self.game_board = game_board
        self.character = character
        self.turn = 0

    def execute(self, pos):
        if self.character.hp <= 10:
            self.character.skills[3].execute(self.character, None, None, None, None)
        elif self.turn % 3 == 0:
            self.character.skills[1].execute(self.character, None, None, None, None)
        elif self.turn % 3 == 1:

            self.character.skills[0].execute(self.character, None, None, None, None)
        elif self.turn % 3 == 2:
            self.character.skills[2].execute(self.character, None, None, None, None)
        self.turn+=1
