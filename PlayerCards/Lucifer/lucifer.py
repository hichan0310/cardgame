import pygame.transform

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import atan, pi, sqrt, sin, cos
import random

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from gameMap import GameMap

img_cursearrow=pygame.transform.scale(pygame.image.load("./PlayerCards/Lucifer/curse_arrow.png"), (150, 100))
curse_explode=[
    pygame.transform.scale(pygame.image.load(f"./PlayerCards/Lucifer/curse/{i}.png"), (500, 500)) for i in range(11)
]

class Curse(Buff):
    def __init__(self, character: "PlayerCard", game_board: "GameMap"):
        super().__init__(character, -1, game_board, "저주", "./PlayerCards/Lucifer/curse.png")
        character.register_curse(self)

    def curse_event(self, caster: "PlayerCard", target: "PlayerCard", game_board: "GameMap"):
        def tmp(scr):
            caster.attack(4, self.target, [TAG_SKILL, TAG_BUFF])
            for observer in caster.observers_attack:
                observer.attack_event(self, [target], self.game_board, [TAG_BUFF])
        motion_draw.add_motion(tmp, 11, ())
        x, y=self.target.pos_center
        for i in range(7):
            tmp_img_0=pygame.transform.scale(curse_explode[0], (500, 500))
            tmp_img_0.set_alpha(min(i*51, 255))
            motion_draw.add_motion(lambda scr, tmpp:scr.blit(tmpp, (x-250, y-250)), i, (tmp_img_0, ))
        for i in range(11):
            motion_draw.add_motion(lambda scr, ii:scr.blit(curse_explode[ii], (x-250, y-250)), i+7, (i, ))
        for i in range(10):
            tmp_img_10=pygame.transform.scale(curse_explode[10], (500, 500))
            tmp_img_10.set_alpha(min(255, (10-i)*25))
            motion_draw.add_motion(lambda scr, tmpp:scr.blit(tmpp, (x-250, y-250)), i+18, (tmp_img_10, ))
        self.remove()


class CurseArrow(Skill):
    def __init__(self, game_board: "GameMap"):
        super().__init__(3, game_board, [TAG_NORMAL_ATTACK, TAG_BUFF])
        self.name = "저주의 화살"
        self.explaination = [
            "cost : 3",
            "직선 방향에 있는 적에게 화살을 날려서 적에게 1의 피해를 준다. ",
            "적에게 저주 버프를 준다. 이 버프는 중첩될 수 있다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Lucifer/skill_image/curse_arrow.png"

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos: tuple[int, int],
                targets_pos: list[tuple[int, int]], execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        angle_rand=random.randint(0, 120)
        for target in targets:
            i=0
            for p1 in [(target.pos_center[0]+1000*cos(angle_rand*pi/180), target.pos_center[1]+1000*sin(angle_rand*pi/180)),
                       (target.pos_center[0]+1000*cos(angle_rand*pi/180+pi*2/3), target.pos_center[1]+1000*sin(angle_rand*pi/180+pi*2/3)),
                       (target.pos_center[0]+1000*cos(angle_rand*pi/180+pi*4/3), target.pos_center[1]+1000*sin(angle_rand*pi/180+pi*4/3))]:
                p2=target.pos_center
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                angle = -atan(dy / (dx - 0.00001)) / pi * 180
                if dx > 0: angle += 180
                angle += 180
                img_arrow = pygame.transform.rotate(img_cursearrow, angle)
                size = img_arrow.get_size()
                i = 0
                while (100 * i) ** 2 < dx ** 2 + dy ** 2:
                    def temp(screen, img_arrow_, i_, p1_, size_, dx_, dy_):
                        t = i_ * 100 / sqrt(dx_ ** 2 + dy_ ** 2)
                        img_pos = (p1_[0] + t * dx_ - size_[0] / 2, p1_[1] + t * dy_ - size_[1] / 2)
                        screen.blit(img_arrow_, img_pos)
                    motion_draw.add_motion(temp, i, (img_arrow, i, p1, size, dx, dy))
                    i += 1
            motion_draw.add_motion(lambda *_: caster.attack(1, target, self.atk_type), i, ())
            if target.team!=FLAG_EMPTY and target.team!=FLAG_SUMMONS:
                x, y = target.pos_center
                for j in range(20):
                    size = j * 20
                    img_temp = pygame.transform.scale(pygame.image.load("./PlayerCards/Lucifer/curse.png"), (size, size))
                    img_temp.set_alpha(min((20 - j) * 15, 255))
                    motion_draw.add_motion(lambda screen, image, size: screen.blit(image, (x - size / 2, y - size / 2)),
                                           i+j,
                                           (img_temp, size))
                Curse(target, target.game_board)
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)


class ExplodeCurse(Skill):
    def __init__(self, game_board: "GameMap"):
        super().__init__(3, game_board, [TAG_SKILL, TAG_PENETRATE, TAG_BUFF])
        self.name = "저주 폭발"
        self.explaination = [
            "cost : 3",
            "적들의 저주를 모두 폭주시킨다. ",
            "1개의 저주 버프는 적에게 2씩 피해를 준다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Lucifer/skill_image/explode_curse.png"

    def execute_range(self, pos: tuple[int, int]):
        return [pos]

    def atk_range(self, caster_pos: tuple[int, int], pos: tuple[int, int]):
        return list(filter(lambda a: a != caster_pos, [(i + 1, j + 1) for i in range(5) for j in range(5)]))

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos: tuple[int, int],
                targets_pos: list[tuple[int, int]], execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            target.curse_explode(caster)


class DoomsdayProphecy(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board: "GameMap"):
        super().__init__(character, count, game_board, "종말의 예언", "./PlayerCards/Lucifer/doomsday_prophecy.png")
        game_board.register_turnover(self)

    def turnover_event(self, game_board: "GameMap"):
        self.target.buff.append(Curse(self.target, game_board))
        self.used(1)

    def turnstart_event(self, game_board: "GameMap"):
        self.target.buff.append(Curse(self.target, game_board))


doomsday=[
    pygame.transform.scale(pygame.image.load(f"./PlayerCards/Lucifer/doomsday/{i}.png"), (600, 600)) for i in range(15)
]

class CommingApocalypse(SpecialSkill):
    def __init__(self, game_board: "GameMap"):
        super().__init__(4, 4, game_board, [TAG_SPECIAL_SKILL, TAG_BUFF])
        self.name = "다가오는 종말"
        self.explaination = [
            "cost : 4, energy : 4",
            "적군 1명을 지정하여 종말의 예언을 내린다. ",
            "앞으로 3턴동안 턴이 시작하고 끝날 때 저주 버프를 부여한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Lucifer/skill_image/comming_apocalypse.png"

    def execute_range(self, pos):
        if self.energy == self.max_energy:
            return [(i + 1, 1) for i in range(5)] + \
                   [(i + 1, 2) for i in range(5)] + \
                   [(i + 1, 3) for i in range(5)] + \
                   [(i + 1, 4) for i in range(5)] + \
                   [(i + 1, 5) for i in range(5)]
        else:
            return []

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos: tuple[int, int],
                targets_pos: list[tuple[int, int]], execute_pos):
        caster.specialSkill.energy = 0
        for target in targets:
            try:
                x, y=target.pos_center
                for i in range(7):
                    motion_draw.add_motion(lambda scr, ii, xx, yy:scr.blit(doomsday[0], (xx-300, yy-250-20*1.5**(6-ii))), i, (i, x, y))
                for i in range(15):
                    motion_draw.add_motion(lambda scr, ii, xx, yy:scr.blit(doomsday[ii], (xx-300, yy-250)), i+7, (i, x, y))
                for i in range(8):
                    tmp_img_14=pygame.transform.scale(doomsday[14], (600, 600))
                    tmp_img_14.set_alpha(255-i*35)
                    motion_draw.add_motion(lambda scr, img, xx, yy:scr.blit(img, (xx-300, yy-250)), i+22, (tmp_img_14, x, y))
                DoomsdayProphecy(target, 3, target.game_board)
            except:
                pass
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)
