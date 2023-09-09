import random
import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sin, cos

if TYPE_CHECKING:
    from playerCard import PlayerCard

astin_star = pygame.image.load("./PlayerCards/Astin/star.png")


class StarFall(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_NORMAL_ATTACK])
        self.name = "별빛 낙하"
        self.explaination = [
            "cost : 2",
            "적 1명을 지정하여 별을 떨어트리고 피해를 입힌다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Astin/skill_image/star_fall.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            x, y = target.pos_center
            dx, dy = random.randint(-30, 30), random.randint(-30, 30)
            img = pygame.transform.scale(astin_star, (50, 50))
            for i in range(16):
                motion_draw.add_motion(
                    lambda screen, ii: screen.blit(img, (x - 40 + dx, y + (ii ** 2 - 225) - 40 + dy)), i,
                    (i,))
            motion_draw.add_motion(lambda scr, tar: caster.attack(1, tar, [TAG_NORMAL_ATTACK]), 15, (target,))

        def tmp(screen):
            for observer in caster.observers_attack:
                observer.attack_event(self, targets, self.game_board, [TAG_NORMAL_ATTACK])

        motion_draw.add_motion(tmp, 15, ())


class CurtainOfNightSky(Buff):
    def __init__(self, character: "PlayerCard", count, game_board):
        super().__init__(character, count, game_board, "밤하늘의 장막", "./PlayerCards/Astin/skill_image/night_sky.png")
        game_board.register_turnover(self)
        try:
            character.register_hit(self)
        except:
            pass

    def turnover_event(self, game_board):
        self.used(1)

    def hit_event(self, caster, target, game_board, atk_type, damage):
        if TAG_PENETRATE in atk_type:
            return
        x, y = target.pos_center
        dx, dy = random.randint(-30, 30), random.randint(-30, 30)
        img = pygame.transform.scale(astin_star, (50, 50))
        for i in range(16):
            motion_draw.add_motion(lambda screen, ii: screen.blit(img, (x - 40 + dx, y + (ii ** 2 - 225) - 40 + dy)), i,
                                   (i,))
        motion_draw.add_motion(lambda scr: target.hit(1, target, [TAG_PENETRATE, TAG_BUFF]), 15, ())


class NightSky(Skill):
    def __init__(self, game_board):
        super().__init__(3, game_board, [TAG_SKILL, TAG_BUFF])
        self.name = "밤하늘의 장막"
        self.explaination = [
            "cost : 3",
            "적군 한 명을 지정하여 2턴동안 밤하늘의 장막 상태를 부여한다. ",
            "적이 피해를 받을 때마다 별이 떨어져서 관통 추가 피해 1을 가한다. ",
            "추가 피해는 관통 공격에 적용되지 않으며, 밤하늘의 장막 상태는 중첩이 가능하다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Astin/skill_image/night_sky.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            try:
                x_0, y_0 = target.pos_center
                for i in range(50):
                    motion_draw.add_motion(lambda scr, x: scr.blit(pygame.transform.scale(astin_star, (60 - x, 60 - x)),
                                                                   (x_0 + cos(x / 2.5) * (1.1 ** (60 - x)) - 30 + x / 2,
                                                                    y_0 + sin(x / 2.5) * (
                                                                                1.1 ** (60 - x)) - 30 + x / 2)), i,
                                           (i,))
                motion_draw.add_motion(lambda scr: CurtainOfNightSky(target, 2, target.game_board), 60, ())
            except:
                continue


class StarRain(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 5, game_board, [TAG_SPECIAL_SKILL])
        self.name = "유성우"
        self.explaination = [
            "cost : 4, energy : 5",
            "맵 전체에 유성우를 내려 적에게 1의 피해를 3번 가한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Astin/skill_image/star_rain.png"

    def execute_range(self, pos):
        if self.energy == self.max_energy:
            return [pos]
        else:
            return []

    def atk_range(self, caster_pos, pos):
        t = [(i + 1, 1) for i in range(5)] + \
            [(i + 1, 2) for i in range(5)] + \
            [(i + 1, 3) for i in range(5)] + \
            [(i + 1, 4) for i in range(5)] + \
            [(i + 1, 5) for i in range(5)]
        return list(
            filter(lambda p: p != caster_pos and self.game_board.gameBoard[p[0]][p[1]].team != FLAG_PLAYER_TEAM, t)
        )

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        def temp_damage(screen):
            for target in targets:
                caster.attack(1, target, self.atk_type)
                for observer in caster.observers_attack:
                    observer.attack_event(self, targets, self.game_board, self.atk_type)

        motion_draw.add_motion(temp_damage, 25, ())
        motion_draw.add_motion(temp_damage, 45, ())
        motion_draw.add_motion(temp_damage, 55, ())
        left, up = self.game_board.gameBoard[1][1].pos_center
        right, down = self.game_board.gameBoard[5][5].pos_center
        left -= CELL_WIDTH // 2
        up -= CELL_HEIGHT // 2
        right += CELL_WIDTH // 2
        down -= CELL_WIDTH // 2
        img = pygame.transform.scale(astin_star, (30, 30))

        def falling_star(screen):
            x, y = random.randint(left, right), random.randint(up, down)
            for i in range(21):
                motion_draw.add_motion(lambda scr, t: scr.blit(img, (x - t * t / 2 + 200, y + t * t - 400)), i, (i,))

        for i in range(40):
            for _ in range(5):
                motion_draw.add_motion(falling_star, i, ())
        caster.specialSkill.energy = 0
