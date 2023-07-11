import playerCard
from main import game_board


class Skill:
    def __init__(self, cost):
        self.cost = cost

    def execute(self, caster: tuple[int, int], target: tuple[int, int]):
        game_board.cost-=self.cost


# 푸른 새싹
class sprout_of_blue(Skill):
    def __init__(self):
        super().__init__(2)
        self.name = "푸른 새싹"
        self.explaination = "바로 옆에 있는 대상에게 스킬을 시전하면 아군은 체력 +1, 적군은 체력 -1"

    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def execute(self, caster: tuple[int, int], target: tuple[int, int]):
        game_board.gameBoard[target[0]][target[1]].heal(1)


# 대지의 새싹
class sprout_of_earth(Skill):
    def __init__(self):
        super().__init__(3)