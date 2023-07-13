from skill import Skill, SpecialSkill
from buff import Buff

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playerCard import PlayerCard


class StraightCut(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board)
        self.name = "직선 베기"
        self.explaination = [
            "cost : 2",
            "직선상의 모든 적을 관통하며 피해를 주고 맵의 끝으로 이동한다. ",
            "지나간 자리에 있는 적을 모두 한 칸씩 당긴다. "
        ]

    def execute_range(self, pos):
        return list(filter(
            lambda p: p != pos,
            [(pos[0], 1),
             (pos[0], 5),
             (1, pos[1]),
             (5, pos[1])]
        ))

    def atk_range(self, caster_pos, pos):
        result = []
        if pos[0] == 1 and caster_pos[0] != 1:
            while caster_pos[0] > 1:
                caster_pos = (caster_pos[0] - 1, caster_pos[1])
                result.append(caster_pos)
        elif pos[0] == 5 and caster_pos[0] != 5:
            while caster_pos[0] < 5:
                caster_pos = (caster_pos[0] + 1, caster_pos[1])
                result.append(caster_pos)
        elif pos[1] == 1 and caster_pos[1] != 1:
            while caster_pos[1] > 1:
                caster_pos = (caster_pos[0], caster_pos[1] - 1)
                result.append(caster_pos)
        elif pos[1] == 5 and caster_pos[1] != 5:
            while caster_pos[1] < 5:
                caster_pos = (caster_pos[0], caster_pos[1] + 1)
                result.append(caster_pos)
        return result

    def execute(self, caster, targets, caster_pos, targets_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy+1, caster.specialSkill.max_energy)
        for target_pos in targets_pos:
            caster.attack(2, self.game_board.gameBoard[target_pos[0]][target_pos[1]], "normal attack")
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]], self.game_board.gameBoard[target_pos[0]][target_pos[1]] = (
                self.game_board.gameBoard[target_pos[0]][target_pos[1]],
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]]
            )
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_center, self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_center = (
                self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_center,
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_center
            )
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].update_location()
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].update_location()
            caster_pos = target_pos
        print(len(targets))


class FireSward(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 4, game_board)
        self.name = "불의 칼날"
        self.explaination = [
            "cost : 4, energy : 4",
            "전방에 넓은 범위에 불의 칼날을 휘둘러 3, 4의 관통 피해를 한 번씩 총 2번 입힌다. ",
            "관통 피해는 버프를 통해서 피해가 오르거나 내려가지 않는다. "
        ]
        self.skill_image_path = "./Chloe/skill_image/sprout_of_blue.png"

    def execute_range(self, pos):
        if self.max_energy==self.energy:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
            ))
        else:return []

    def atk_range(self, caster_pos, pos):
        result = []
        if pos[0] == caster_pos[0] - 1:
            while caster_pos[0] > 1:
                caster_pos = (caster_pos[0] - 1, caster_pos[1])
                result += [(caster_pos[0], i) for i in range(1, 6)]
        elif pos[0] == caster_pos[0] + 1:
            while caster_pos[0] < 5:
                caster_pos = (caster_pos[0] + 1, caster_pos[1])
                result += [(caster_pos[0], i) for i in range(1, 6)]
        elif pos[1] == caster_pos[1] - 1:
            while caster_pos[1] > 1:
                caster_pos = (caster_pos[0], caster_pos[1] - 1)
                result += [(caster_pos[0], i) for i in range(1, 6)]
        elif pos[1] == caster_pos[1] + 1:
            while caster_pos[1] < 5:
                caster_pos = (caster_pos[0], caster_pos[1] + 1)
                result += [(caster_pos[0], i) for i in range(1, 6)]
        return result

    def execute(self, caster, targets, caster_pos, targets_pos):
        for target in targets:
            target.penetrateHit(3, caster)
        for target in targets:
            target.penetrateHit(4, caster)


