import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from summons import Summons
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard


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
                for target in targets:
                    target.hit(1, caster, [TAG_SUMMON])


class CrackOfEarth(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_SUMMON, TAG_SKILL])
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
            if target.name != "empty cell":
                caster.attack(1, target, self.atk_type)
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)


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
        return list(filter(lambda p: self.game_board.gameBoard[p[0]][p[1]].name == "empty cell", t))

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
        for target in targets:
            caster.attack(2, target, self.atk_type)
        caster.passive[0].destroyed = 0
        caster.specialSkill.energy = 0
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)
