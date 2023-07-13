from skill import Skill
from buff import Buff


# 푸른 새싹
class Sprout_of_blue(Skill):
    def __init__(self):
        super().__init__(2)
        self.cost=2
        self.name = "푸른 새싹"
        self.explaination = [
            "바로 앞 또는 옆에 있는 대상에게 스킬을 시전하여 1의 피해를 준다. "
        ]
        self.skill_image_path = "./Chloe/skill_image/sprout_of_blue.png"

    def execute_range(self, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        ))

    def execute_one(self, caster, target):
        target.heal(1)

    def execute(self, caster, targets):
        print("스킬 푸른 새싹의 execute 함수 호출됨")
        for target in targets:
            print(target.name)
            target.heal(1)


# 대지의 새싹
class Sprout_of_earth(Skill):
    def __init__(self):
        super().__init__(3)
        self.cost=3
        self.name="대지의 새싹"
        self.explaination=[
            "아군 한 명을 지정하여 3의 체력을 회복하고 빠른 이동 상태로 만든다. ",
            "빠른 이동 상태에서 다음 이동 시 사용하는 cost가 1 감소한다. ",
            "빠른 이동 상태는 중첩될 수 없다. "
        ]
        self.skill_image_path = "./Chloe/skill_image/sprout_of_earth.png"

    def execute(self, caster, targets):
        print("스킬 대지의 새싹의 execute 함수 호출됨")
        for target in targets:
            print(target.name)
            target.heal(3)
            target.quick_move=True
        print()



class Reincarnation(Buff):
    def __init__(self, character, count: int):
        super().__init__(character, count)

    def move_event(self, player, pos: tuple[int, int], game_board):
        x, y = pos
        game_board.heal((x + 1, y), 1)
        game_board.heal((x, y + 1), 1)
        game_board.heal((x - 1, y), 1)
        game_board.heal((x, y - 1), 1)
        self.used(1)

