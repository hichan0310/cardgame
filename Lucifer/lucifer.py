from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playerCard import PlayerCard


class Curse(Buff):
    def __init__(self, character, game_board):
        super().__init__(character, -1, game_board, "저주")
        character.register_curse(self)

    def curse_event(self, caster:"PlayerCard", target:"PlayerCard", game_board):
        caster.attack(2, target, "skill")
        self.remove()


class CurseArrow(Skill):
    def __init__(self, game_board):
        super().__init__(3, game_board)
        self.name = "저주의 화살"
        self.explaination = [
            "cost : 3",
            "직선 방향에 있는 적에게 화살을 날려서 적에게 1의 피해를 준다. ",
            "적에게 저주 버프를 준다. 이 버프는 중첩될 수 있다. "
        ]
        self.skill_image_path = "./Lucifer/skill_image/curse_arrow.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: p != pos,
            [(pos[0], 1), (pos[0], 2), (pos[0], 3), (pos[0], 4), (pos[0], 5),
             (1, pos[1]), (2, pos[1]), (3, pos[1]), (4, pos[1]), (5, pos[1])]
        ))

    def execute(self, caster:"PlayerCard", targets:"list[PlayerCard]", caster_pos, targets_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            if target.name!="empty cell":
                caster.attack(1, target, "normal attack")
                target.buff.append(Curse(target, target.game_board))

# class ExplodeCurse(Skill):
#     def __init__(self, game_board):
#         super().__init__(game_board, 3)
#         self.name = ""

class DoomsdayProphecy(Buff):
    def __init__(self, character:"PlayerCard", count, game_board):
        super().__init__(character, count, game_board, "종말의 예언")
        game_board.register_turnover(self)

    def turnover_event(self, game_board):
        self.target.buff.append(Curse(self.target, game_board))
        self.used(1)

    def turnstart_event(self, game_board):
        self.target.buff.append(Curse(self.target, game_board))

class CommingApocalypse(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 4, game_board)
        self.name="다가오는 종말"
        self.explaination=[
            "cost : 4, energy : 4",
            "적군 1명을 지정하여 종말의 예언을 내린다. ",
            "앞으로 3턴동안 턴이 시작하고 끝날 때 저주 버프를 부여한다. "
        ]
        self.skill_image_path = "./Lucifer/skill_image/comming_apocalypse.png"

    def execute(self, caster, targets, caster_pos, targets_pos):
        caster.specialSkill.energy=0
        for target in targets:
            target.buff.append(DoomsdayProphecy(target, 3, target.game_board))

