import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard


class StraightCut(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board)
        self.name = "직선 베기"
        self.explaination = [
            "cost : 2",
            "직선상의 모든 적을 관통하며 1의 피해를 주고 맵의 끝으로 이동한다. ",
            "지나간 자리에 있는 적을 모두 한 칸씩 당긴다. "
        ]
        self.skill_image_path = "./Tania/skill_image/straight_cut.png"

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

    def execute(self, caster: "PlayerCard", targets: "list[PlayerCard]", caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target_pos in targets_pos:
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]], self.game_board.gameBoard[target_pos[0]][
                target_pos[1]] = (
                self.game_board.gameBoard[target_pos[0]][target_pos[1]],
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]]
            )
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_center, \
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_center = (
                self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_center,
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_center
            )
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].update_location()
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].update_location()
            caster.attack(1, self.game_board.gameBoard[caster_pos[0]][caster_pos[1]], "normal attack")
            caster_pos = target_pos


class Burn(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "화상")
        game_board.register_turnover(self)

    def turnover_event(self, game_board):
        self.target.hp -= 1
        if self.target.hp <= 0:
            self.target.die()
        self.used(1)


class FlameShuriken(Skill):
    def __init__(self, game_board):
        super().__init__(3, game_board)
        self.name = "불꽃 수리검"
        self.explaination = [
            "cost : 3",
            "적 1명에게 불꽃 수리검을 날려서 3의 피해를 가하고 1턴간 화상 효과를 부여한다. ",
            "화상 효과가 부여된 적은 턴 종료 시 체력이 1 감소한다. ",
            "화상 효과는 중첩될 수 있다. "
        ]
        self.skill_image_path = "./Tania/skill_image/flame_shuriken.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target in targets:
            if target.name != "empty cell":
                caster.attack(3, target, "skill")
                Burn(target, 1, target.game_board)


class FlameSward(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 5, game_board)
        self.name = "불의 칼날"
        self.explaination = [
            "cost : 4, energy : 5",
            "전방에 넓은 범위에 불의 칼날을 휘둘러 3의 관통 피해를 2번 입힌다. ",
            "관통 피해는 버프를 통해서 피해가 오르거나 내려가지 않는다. "
        ]
        self.skill_image_path = "./Tania/skill_image/flame_sward.png"

    def execute_range(self, pos):
        if self.max_energy == self.energy:
            return list(filter(
                lambda p: 0 < p[0] < 6 and 0 < p[1] < 6,
                [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
            ))
        else:
            return []

    def atk_range(self, caster_pos, pos):
        result = []
        if pos[0] == caster_pos[0] - 1 and caster_pos[0] != 1:
            while caster_pos[0] > 1:
                caster_pos = (caster_pos[0] - 1, caster_pos[1])
                result += [(caster_pos[0], caster_pos[1]-1),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0], caster_pos[1]+1)]
        elif pos[0] == caster_pos[0] + 1 and caster_pos[0] != 5:
            while caster_pos[0] < 5:
                caster_pos = (caster_pos[0] + 1, caster_pos[1])
                result += [(caster_pos[0], caster_pos[1]-1),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0], caster_pos[1]+1)]
        elif pos[1] == caster_pos[1] - 1 and caster_pos[1] != 1:
            while caster_pos[1] > 1:
                caster_pos = (caster_pos[0], caster_pos[1] - 1)
                result += [(caster_pos[0]-1, caster_pos[1]),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0]+1, caster_pos[1])]
        elif pos[1] == caster_pos[1] + 1 and caster_pos[1] != 5:
            while caster_pos[1] < 5:
                caster_pos = (caster_pos[0], caster_pos[1] + 1)
                result += [(caster_pos[0]-1, caster_pos[1]),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0]+1, caster_pos[1])]
        return list(filter(lambda p: 0 < p[0] < 6 and 0 < p[1] < 6, result))

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = 0
        execute_pos_real = transform_pos(execute_pos)
        for i in range(15):
            img = pygame.image.load(f"./Tania/skill_motion/{i}.png")
            if caster_pos[0] > execute_pos[0]:
                img = pygame.transform.rotate(img, 90)
                img_position = (execute_pos_real[0], execute_pos_real[1] - i * 40)
            elif caster_pos[0] < execute_pos[0]:
                img = pygame.transform.rotate(img, 270)
                img_position = (execute_pos_real[0], execute_pos_real[1] + i * 40)
            elif caster_pos[1] > execute_pos[1]:
                img = pygame.transform.rotate(img, 0)
                img_position = (execute_pos_real[0] - i * 40, execute_pos_real[1])
            else:
                img = pygame.transform.rotate(img, 180)
                img_position = (execute_pos_real[0] + i * 40, execute_pos_real[1])
            img_size = img.get_size()
            motion_draw.add_motion(lambda screen, img, pos: screen.blit(img, pos), i,
                                   (img, (img_position[0] - img_size[0] / 2, img_position[1] - img_size[1] / 2)))
        for target in targets:
            target.penetrateHit(3, caster)

        def temp_func(screen, *_):
            for target in targets:
                target.penetrateHit(4, caster)

        motion_draw.add_motion(temp_func, 10, ())

        for i in range(15):
            img = pygame.image.load(f"./Tania/skill_motion/{i}.png")
            if caster_pos[0] > execute_pos[0]:
                img = pygame.transform.rotate(img, 90)
                img_position = (execute_pos_real[0], execute_pos_real[1] - i * 40)
            elif caster_pos[0] < execute_pos[0]:
                img = pygame.transform.rotate(img, 270)
                img_position = (execute_pos_real[0], execute_pos_real[1] + i * 40)
            elif caster_pos[1] > execute_pos[1]:
                img = pygame.transform.rotate(img, 0)
                img_position = (execute_pos_real[0] - i * 40, execute_pos_real[1])
            else:
                img = pygame.transform.rotate(img, 180)
                img_position = (execute_pos_real[0] + i * 40, execute_pos_real[1])
            img_size = img.get_size()
            motion_draw.add_motion(lambda screen, img, pos: screen.blit(img, pos), i + 10,
                                   (img, (img_position[0] - img_size[0] / 2, img_position[1] - img_size[1] / 2)))
