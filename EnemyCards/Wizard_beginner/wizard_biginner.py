from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard
    from gameMap import GameMap


class EnergyBall(Skill):
    def __init__(self, game_board: "GameMap"):
        super().__init__(3, game_board)
        self.name = "에너지볼"
        self.explaination = [
            "적군 1명을 중심으로 1의 광역 피해를 가한다. "
        ]
        self.skill_image_path = "./PlayerCards/Lucifer/skill_image/curse_arrow.png"

    def atk_range(self, caster_pos, pos):
        return list(filter(
            lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
            [(pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] - 1, pos[1] + 1),
             (pos[0], pos[1] - 1), pos, (pos[0], pos[1] + 1),
             (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0] + 1, pos[1] + 1), ]
        ))

    def execute(self, caster: "EnemyCard", targets: "list[PlayerCard]", caster_pos: tuple[int, int],
                targets_pos: list[tuple[int, int]], execute_pos):
        for target in targets:
            if target.name != "empty cell":
                caster.attack(2, target, "normal attack")
        for observer in caster.observers_attack[::-1]:
            observer.attack_event(self, targets, self.game_board, "normal attack")


class AI_WizardBiginner:
    def __init__(self, game_board, character: "EnemyCard"):
        self.game_board = game_board
        self.character = character

    def execute(self, pos):
        print(self.character.name)
