import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from summons import Summons
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import atan, pi, sqrt

if TYPE_CHECKING:
    from playerCard import PlayerCard

img_stone=pygame.image.load("./PlayerCards/Petra/turret_stone.png")
crack_line=pygame.transform.scale(pygame.image.load("./PlayerCards/Petra/crack_line.png"), (30, 30))
special=pygame.transform.scale(pygame.image.load("./PlayerCards/Petra/special.png"), (1000, 1000))

class BaseInstability(Buff):
    def __init__(self, character: "PlayerCard", game_board):
        super().__init__(character, -1, game_board, "기반 불안정", "./PlayerCards/Petra/base_instability.png")
        self.destroyed = 0

    def turret_die_event(self):
        self.destroyed += 1

    def atk_buff(self, caster, target, damage: int, atk_type: list[str]):
        if TAG_SPECIAL_SKILL in atk_type:
            damage += self.destroyed
        return damage


class StoneTurret(Summons):
    def __init__(self, pos, game_board, group, petra: "PlayerCard", base_instability):
        pos_real = transform_pos(pos)
        super().__init__(3, pos_real, game_board, group, petra, "./PlayerCards/Petra/turret_img.png", pos)
        self.name = "petra turret"
        self.base_instability = base_instability
        petra.register_attack(self)

    def die(self):
        self.base_instability.turret_die_event()
        super().die()

    def attack_event(self, caster, targets, game_board, atk_type):
        if TAG_NORMAL_ATTACK in atk_type:
            if not self.dead:
                p1=self.pos_center
                for target in targets:
                    p2=target.pos_center
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    angle += 180
                    img_arrow = pygame.transform.rotate(img_stone, angle)
                    size = img_arrow.get_size()
                    i = 0
                    while (80 * i) ** 2 < dx ** 2 + dy ** 2:
                        def temp(screen, i):
                            t = i * 80 / sqrt(dx ** 2 + dy ** 2)
                            img_pos = (p1[0] + t * dx - size[0] / 2, p1[1] + t * dy - size[1] / 2)
                            screen.blit(img_arrow, img_pos)

                        motion_draw.add_motion(temp, 10+i, (i,))
                        i += 1
                    motion_draw.add_motion(lambda *_: target.hit(1, caster, [TAG_SUMMON]), i + 10, ())



class CrackOfEarth(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_SUMMON, TAG_NORMAL_ATTACK])
        self.name = "대지의 균열"
        self.explaination = [
            "cost : 2",
            "땅을 갈라서 1의 피해를 줍니다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Petra/skill_image/crack_of_earth.png"

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            for observer in caster.observers_attack:
                observer.attack_event(caster, targets, self.game_board, self.atk_type)
                if observer.name=="petra turret":
                    p1=target.pos_center
                    p2=observer.pos_center
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    angle += 90
                    img_arrow = pygame.transform.rotate(crack_line, angle)
                    size = img_arrow.get_size()
                    i = 0
                    while (30 * i) ** 2 < dx ** 2 + dy ** 2:
                        def temp(screen, img_arrow_, i_, p1_, size_, dx_, dy_):
                            t = i_ * 30 / sqrt(dx_ ** 2 + dy_ ** 2)
                            img_pos = (p1_[0] + t * dx_ - size_[0] / 2, p1_[1] + t * dy_ - size_[1] / 2)
                            screen.blit(img_arrow_, img_pos)

                        for j in range(15, 24):
                            img_arrow.set_alpha(min([255 * (1.1 ** i - 1), 255]))
                            motion_draw.add_motion(temp, j-15+i//6, (img_arrow, i, p1, size, dx, dy))
                        i += 1
            if target.name != "empty cell":
                petra_normal_crack=pygame.image.load("./PlayerCards/Petra/crack.png")
                for i in range(24):
                    size = min([1, 2 - 1.25 ** (i - 21)]) * 200
                    tmp = pygame.transform.scale(petra_normal_crack, (size, size))
                    tmp.set_alpha(min([255 * (1.1 ** i - 1), 255]))

                    motion_draw.add_motion(lambda scr, img: scr.blit(img, (
                    target.pos_center[0] - img.get_size()[0] / 2, target.pos_center[1] - img.get_size()[1] / 2)),
                                           23 - i,
                                           (tmp,))
                caster.attack(1, target, self.atk_type)


class SummonTurret(Skill):
    def __init__(self, game_board):
        super().__init__(3, game_board, [TAG_SKILL, TAG_SUMMON])
        self.name = "공명하는 바위"
        self.explaination = [
            "cost : 3",
            "일반 공격과 공명하는 바위 포탑을 소환합니다. ",
            "포탑은 3번 공격받으면 파괴되고 대지의 균열 발동 시 협동 공격으로 1의 피해를 가한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Petra/skill_image/summon_turret.png"

    def execute_range(self, pos):
        t = [(i + 1, 1) for i in range(5)] + \
            [(i + 1, 2) for i in range(5)] + \
            [(i + 1, 3) for i in range(5)] + \
            [(i + 1, 4) for i in range(5)] + \
            [(i + 1, 5) for i in range(5)]
        return list(filter(lambda p: self.game_board.gameBoard[p[0]][p[1]].team==FLAG_EMPTY, t))

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target_pos in targets_pos:
            self.game_board.add_summons(target_pos,
                                        StoneTurret(target_pos, self.game_board, self.game_board.group, caster,
                                                    caster.passive[0]))


class BaseCollapse(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 4, game_board, [TAG_SPECIAL_SKILL])
        self.name = "기반 붕괴"
        self.explaination = [
            "cost : 4, energy : 4",
            "맵 전체에 기반 붕괴로 2의 피해를 가한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Petra/skill_image/base_collapse.png"

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
        return list(filter(lambda p: p != caster_pos, t))

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        x, y=transform_pos((3, 3))
        pos=(x-500, y-500)
        for i in range(20):
            special.set_alpha(min(255, 300-i*15))
            motion_draw.add_motion(lambda scr, sp:scr.blit(sp, pos), i, (special, ))
        for target in targets:
            caster.attack(2, target, self.atk_type)
        caster.passive[0].destroyed = 0
        caster.specialSkill.energy = 0
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)
