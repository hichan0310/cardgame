from skill import Skill, SpecialSkill
from buff import Buff
from settings import *
from typing import TYPE_CHECKING
from graphic_manager import motion_draw

if TYPE_CHECKING:
    from playerCard import PlayerCard


grow=[pygame.image.load(f"./PlayerCards/Chloe/grow/{i}.png") for i in range(13)]

def heal_grow(pos):
    pos=transform_pos(pos)
    for i in range(30):
        img=grow[min(i, 12)]
        motion_draw.add_motion(lambda scr, imgg, xx, yy:scr.blit(imgg, (pos[0]-xx/2, pos[1]-yy/2-50)), i, (img, *img.get_size()))



# 푸른 새싹
class SproutOfBlue(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_NORMAL_ATTACK, TAG_HEAL])
        self.name = "급속생장"
        self.explaination = [
            "cost : 2",
            "바로 앞 또는 옆에 있는 대상에게 스킬을 시전하여 체력 1을 회복한다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/fast_growth.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            motion_draw.add_motion(lambda scr:target.heal(1), 13, ())
            heal_grow(target.pos_gameboard)


# 대지의 새싹
class SproutOfEarth(Skill):
    def __init__(self, game_board):
        super().__init__(3, game_board, [TAG_SKILL, TAG_HEAL])
        self.name = "푸른 새싹"
        self.explaination = [
            "cost : 3",
            "아군 한 명을 지정하여 3의 체력을 회복하고 빠른 이동 상태로 만든다. ",
            "빠른 이동 상태에서 다음 이동 시 사용하는 cost가 1 감소한다. ",
            "빠른 이동 상태는 중첩될 수 없다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/sprout_of_blue.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            motion_draw.add_motion(lambda scr:target.heal(3), 13, ())
            target.quick_move = True
            heal_grow(target.pos_gameboard)


# 재생 버프
class Reincarnation(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "재생", "./PlayerCards/Chloe/reincarnation.png")
        character.register_move(self)

    def move_event(self, player: "PlayerCard", pos: tuple[int, int], game_board):
        x, y = pos
        def tmp(scr):
            self.game_board.heal((x + 1, y), 1)
            self.game_board.heal((x, y + 1), 1)
            self.game_board.heal((x - 1, y), 1)
            self.game_board.heal((x, y - 1), 1)
        motion_draw.add_motion(tmp, 13, ())
        heal_grow((x, y))
        heal_grow((x+1, y))
        heal_grow((x, y+1))
        heal_grow((x-1, y))
        heal_grow((x, y-1))
        player.heal(1)
        self.used(1)


# 재생의 씨앗
class SproutOfReincarnation(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(3, 4, game_board, [TAG_SPECIAL_SKILL, TAG_HEAL, TAG_BUFF])
        self.name = "세계수의 축복"
        self.explaination = [
            "cost : 3, energy : 4",
            "자기 자신에게 재생 상태를 부여한다. 재생 상태에서는 위치 이동 이후에 cost를 소모하지 않는다. ",
            "재생 상태에서 위치 이동을 하면 자기 자신과 바로 위, 아래, 옆에 있는 아군의 체력을 1만큼 회복한다. ",
            "이 상태는 7번 위치 이동 이후 사라지며 중첩이 가능하다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Chloe/skill_image/blessing_world_tree.png"

    def execute_range(self, pos):
        if self.energy == self.max_energy:
            return [pos]
        else:
            return []

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = 0
        for target in targets:
            Reincarnation(target, 7, target.game_board)
