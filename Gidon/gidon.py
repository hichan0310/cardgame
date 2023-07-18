import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from summons import Summons
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard


class BloodyBlow(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board)
        self.name = "피의 일격"
        self.explaination = [
            "cost : 2",
            "전방에 검을 휘둘러 1의 광역 피해를 가한다. "
        ]
        self.skill_image_path = "./Tania/skill_image/straight_cut.png"

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

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            caster.attack(1, target, "normal attack")


class BloodRage(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "피의 분노", "./Tania/burn.png")
        game_board.register_turnover(self)

    def atk_buff(self, caster, target, damage: int, atk_type: str):
        if atk_type == "normal attack":
            return damage + min(caster.max_hp - caster.hp, 5)
        return damage

    def normal_attack_event(self, caster, target, game_board):
        self.used(1)

class VengeanceEyes(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board)
        self.name="복수의 눈빛"
        self.explaination = [
            "cost : 2",
            "자신에게 1의 관통 피해를 가하고 자신에게 피의 분노 상태를 부여한다. ",
            "피의 분노 상태는 일반 공격 2회까지 유지되고 일반 공격의 피해가 자신이 잃은 체력만큼 강해진다. ",
            "잃은 체력은 최대 체력에서 현재 체력을 뺀 값으로 계산되며 최대 5까지 피해가 증가한다. ",
            "자신의 체력이 2 이하일 경우 체력이 감소하지 않는다. "
            "이 스킬로 필살기 에너지를 채울 수 없다. "
        ]
        self.skill_image_path="./Chloe/skill_image/sprout_of_earth.png"

    def execute_range(self, pos):
        return [pos]

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        for target in targets:
            if target.hp>2:
                target.penetrateHit(1, caster)
            BloodRage(target, 2, target.game_board)


class UnfinishedRage(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 4, game_board)
        self.name="끝나지 않은 분노"
        self.explaination=[
            "cost : 4, energy : 4",
            "바로 앞의 적을 지정하여 15의 피해를 준다. "
        ]
    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        for target in targets:
            caster.attack(15, target, "special skill")


