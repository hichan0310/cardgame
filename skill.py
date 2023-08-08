class Skill:
    def __init__(self, cost: int, game_board, atk_type):
        self.atk_type=atk_type
        self.game_board = game_board
        self.cost = cost
        self.name = "empty skill"
        self.explaination = [
            "no explaination"
        ]
        self.skill_image_path = "./Chloe/skill_image/sprout_of_blue.png"

    def execute_one(self, caster, target):
        pass

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        for target in targets:
            self.execute_one(caster, target)

    def execute_range(self, pos):
        return [(i + 1, 1) for i in range(5)] + \
               [(i + 1, 2) for i in range(5)] + \
               [(i + 1, 3) for i in range(5)] + \
               [(i + 1, 4) for i in range(5)] + \
               [(i + 1, 5) for i in range(5)]

    def atk_range(self, caster_pos, pos):
        return [pos]


class SpecialSkill(Skill):
    def __init__(self, cost, energy, game_board, atk_type):
        super().__init__(cost, game_board, atk_type)
        self.max_energy = energy
        self.energy = 0
        self.name = "empty special skill"
        self.explaination = [
            "no explaination"
        ]
        self.skill_image_path = "./Chloe/skill_image/sprout_of_blue.png"
