import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from summons import Summons
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard

bloody_blows = [
    pygame.transform.scale(pygame.image.load(f"./PlayerCards/Gideon/bloody_blow/{i}.png"), (200 * 3, 200 * 2)) for i in
    range(7)]
unfinished_rage=[
    pygame.transform.scale(pygame.image.load(f"./PlayerCards/Gideon/unfinished_rage/{i}.png"), (800, 800)) for i in range(6)
]
boom=pygame.image.load("./PlayerCards/Gideon/boom.png")


class BloodyBlow(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_NORMAL_ATTACK])
        self.name = "피의 일격"
        self.explaination = [
            "cost : 2",
            "전방에 검을 휘둘러 1의 광역 피해를 가한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Gideon/skill_image/bloody_blow.png"

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
        x, y = transform_pos(execute_pos)
        y -= 200 * 3 / 2
        x -= 200 / 2+80
        angle = 90
        if caster_pos[0] < execute_pos[0]:
            x, y = transform_pos(execute_pos)
            x -= 200 * 3 / 2
            y -= 200 / 2+80
            angle = 0
        if caster_pos[0] > execute_pos[0]:
            x, y = transform_pos(execute_pos)
            x -= 200 * 3 / 2
            y -= 200 * 3 / 2-80
            angle = 180
        if caster_pos[1] > execute_pos[1]:
            x, y = transform_pos(execute_pos)
            y -= 200 * 3 / 2
            x -= 200 * 3 / 2-80
            angle = 270
        images = [pygame.transform.rotate(img, angle) for img in bloody_blows]
        for target in targets:
            caster.attack(1, target, self.atk_type)
        for observer in caster.observers_attack[::-1]:
            observer.attack_event(self, targets, self.game_board, self.atk_type)
        for i in range(7):
            motion_draw.add_motion(lambda scr, img: scr.blit(img, (x, y)), i, (images[i],))


class BloodRage(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "피의 분노", "./PlayerCards/Gideon/skill_image/vengeance_eye.png")
        character.register_attack(self)

    def atk_buff(self, caster, target, damage: int, atk_type: list[str]):
        if TAG_NORMAL_ATTACK in atk_type:
            if damage + min(caster.max_hp - caster.hp, 5)>36:
                return max(36, damage)
            else:
                return damage + min(caster.max_hp - caster.hp, 5)
        return damage

    def attack_event(self, caster, target, game_board, atk_type):
        if TAG_NORMAL_ATTACK in atk_type:
            self.used(1)


class VengeanceEye(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_SKILL, TAG_PENETRATE, TAG_BUFF])
        self.name = "복수의 눈빛"
        self.explaination = [
            "cost : 2",
            "자신에게 1의 관통 피해를 가하고 자신에게 피의 분노 상태를 부여한다. ",
            "피의 분노 상태는 일반 공격 2회까지 유지되고 일반 공격의 피해가 자신이 잃은 체력만큼 강해진다. ",
            "잃은 체력은 최대 체력에서 현재 체력을 뺀 값으로 계산되며 최대 5까지 피해가 증가한다. ",
            "자신의 체력이 2 이하일 경우 체력이 감소하지 않는다. ",
            "이 스킬로 필살기 에너지를 채울 수 없다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Gideon/skill_image/vengeance_eye.png"

    def execute_range(self, pos):
        return [pos]

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        for target in targets:
            if target.hp > 2:
                target.hit(1, caster, self.atk_type)
            BloodRage(target, 2, target.game_board)
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)


class UnfinishedRage(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 4, game_board, [TAG_SPECIAL_SKILL])
        self.name = "끝나지 않은 분노"
        self.explaination = [
            "cost : 4, energy : 4",
            "바로 앞의 적을 지정하여 15의 피해를 주고 3의 체력을 회복한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Gideon/skill_image/unfinished_rage.png"

    def execute_range(self, pos):
        if self.energy == self.max_energy:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
            ))
        else:
            return []

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        self.energy = 0
        for target in targets:
            target_pos = target.pos_gameboard
            x, y = caster.pos_center
            x-=400
            y-=400
            angle = 90
            if caster_pos[0] < execute_pos[0]:
                angle = 0
            if caster_pos[0] > execute_pos[0]:
                angle = 180
            if caster_pos[1] > execute_pos[1]:
                angle = 270
            images = [pygame.transform.rotate(img, angle) for img in unfinished_rage]
            for i in range(6):
                motion_draw.add_motion(lambda scr:scr.blit(images[0], (x, y)), i, ())
            for i in range(5):
                motion_draw.add_motion(lambda scr, ii:scr.blit(images[ii], (x, y)), i+6, (i, ))
            for i in range(12):
                motion_draw.add_motion(lambda scr:scr.blit(images[5], (x, y)), i+11, ())
            for i in range(24):
                size = min([1, 2 - 1.25 ** (i - 21)]) * 2
                tmp = pygame.transform.scale(boom, (500 * size, 500 * size))
                tmp.set_alpha(min([255 * (1.1 ** i - 1), 255]))

                motion_draw.add_motion(lambda scr, img: scr.blit(img, (
                target.pos_center[0] - img.get_size()[0] / 2, target.pos_center[1] - img.get_size()[1] / 2)),
                                       23 - i + 12,
                                       (tmp,))
            motion_draw.add_motion(lambda scr: caster.attack(15, target, self.atk_type), 14, ())
            motion_draw.add_motion(lambda scr: caster.heal(3), 14, ())
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, self.atk_type)
