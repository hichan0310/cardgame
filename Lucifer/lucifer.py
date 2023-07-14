from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from gameMap import GameMap


class Curse(Buff):
    def __init__(self, character:"PlayerCard", game_board:"GameMap"):
        super().__init__(character, -1, game_board, "저주")
        character.register_curse(self)

    def curse_event(self, caster:"PlayerCard", target:"PlayerCard", game_board:"GameMap"):
        caster.attack(2, self.target, "skill")
        self.remove()


class CurseArrow(Skill):
    def __init__(self, game_board:"GameMap"):
        super().__init__(3, game_board)
        self.name = "저주의 화살"
        self.explaination = [
            "cost : 3",
            "직선 방향에 있는 적에게 화살을 날려서 적에게 1의 피해를 준다. ",
            "적에게 저주 버프를 준다. 이 버프는 중첩될 수 있다. "
        ]
        self.skill_image_path = "./Lucifer/skill_image/curse_arrow.png"

    def execute_range(self, pos:tuple[int, int]):
        return list(filter(
            lambda p: p != pos,
            [(pos[0], 1), (pos[0], 2), (pos[0], 3), (pos[0], 4), (pos[0], 5),
             (1, pos[1]), (2, pos[1]), (3, pos[1]), (4, pos[1]), (5, pos[1])]
        ))

    def execute(self, caster:"PlayerCard", targets:"list[PlayerCard]", caster_pos:tuple[int, int], targets_pos:list[tuple[int, int]]):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            if target.name!="empty cell":
                caster.attack(1, target, "normal attack")
                Curse(target, target.game_board)

class ExplodeCurse(Skill):
    def __init__(self, game_board:"GameMap"):
        super().__init__(3, game_board)
        self.name = "저주 폭발"
        self.explaination=[
            "cost : 3",
            "적들의 저주를 모두 폭주시킨다. ",
            "1개의 저주 버프는 적에게 2씩 피해를 준다. "
        ]
        self.skill_image_path = "./Lucifer/skill_image/explode_curse.png"

    def execute_range(self, pos:tuple[int, int]):
        return [pos]

    def atk_range(self, caster_pos:tuple[int, int], pos:tuple[int, int]):
        return list(filter(lambda a:a!=caster_pos, [(i+1, j+1) for i in range(5) for j in range(5)]))

    def execute(self, caster:"PlayerCard", targets:"list[PlayerCard]", caster_pos:tuple[int, int], targets_pos:list[tuple[int, int]]):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            target.curse_explode(caster)


class DoomsdayProphecy(Buff):
    def __init__(self, character:"PlayerCard", count:int, game_board:"GameMap"):
        super().__init__(character, count, game_board, "종말의 예언")
        game_board.register_turnover(self)

    def turnover_event(self, game_board:"GameMap"):
        self.target.buff.append(Curse(self.target, game_board))
        self.used(1)

    def turnstart_event(self, game_board:"GameMap"):
        self.target.buff.append(Curse(self.target, game_board))

class CommingApocalypse(SpecialSkill):
    def __init__(self, game_board:"GameMap"):
        super().__init__(4, 4, game_board)
        self.name="다가오는 종말"
        self.explaination=[
            "cost : 4, energy : 4",
            "적군 1명을 지정하여 종말의 예언을 내린다. ",
            "앞으로 3턴동안 턴이 시작하고 끝날 때 저주 버프를 부여한다. "
        ]
        self.skill_image_path = "./Lucifer/skill_image/comming_apocalypse.png"

    def execute(self, caster:"PlayerCard", targets:"list[PlayerCard]", caster_pos:tuple[int, int], targets_pos:list[tuple[int, int]]):
        caster.specialSkill.energy=0
        for target in targets:
            target.buff.append(DoomsdayProphecy(target, 3, target.game_board))

