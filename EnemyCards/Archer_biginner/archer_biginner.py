from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playerCard import PlayerCard
    from enemy import EnemyCard
    from gameMap import GameMap


class Arrow(Skill):
    def __init__(self, game_board:"GameMap"):
        super().__init__(3, game_board)
        self.name = "정조준"
        self.explaination = [
            "적군 1명에게 2의 피해를 가한다. "
        ]
        self.skill_image_path = "./PlayerCards/Lucifer/skill_image/curse_arrow.png"

    def execute(self, caster:"EnemyCard", targets:"list[PlayerCard]", caster_pos:tuple[int, int], targets_pos:list[tuple[int, int]], execute_pos):
        for target in targets:
            if target.name!="empty cell":
                caster.attack(2, target, "normal attack")
        for observer in caster.observers_attack[::-1]:
            observer.attack_event(self, targets, self.game_board, "normal attack")