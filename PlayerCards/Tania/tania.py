import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos


if TYPE_CHECKING:
    from playerCard import PlayerCard

flame_shuriken=pygame.image.load("./PlayerCards/Tania/skill_motion/flame_shuriken/0.png")
flame_sward=[pygame.image.load(f"./PlayerCards/Tania/skill_motion/flame_sward/{i}.png") for i in range(15)]

class StraightCut(Skill):
    def __init__(self, game_board):
        super().__init__(2, game_board, [TAG_NORMAL_ATTACK, TAG_PYRO])
        self.name = "직선 베기"
        self.explaination = [
            "cost : 2",
            "직선상의 모든 적을 관통하며 1의 피해를 주고 맵의 끝으로 이동한다. ",
            "지나간 자리에 있는 적을 모두 한 칸씩 당긴다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Tania/skill_image/straight_cut.png"

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
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_gameboard, \
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_gameboard = (
                self.game_board.gameBoard[target_pos[0]][target_pos[1]].pos_gameboard,
                self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].pos_gameboard
            )
            self.game_board.gameBoard[caster_pos[0]][caster_pos[1]].update_location()
            self.game_board.gameBoard[target_pos[0]][target_pos[1]].update_location()
            caster.attack(1, self.game_board.gameBoard[caster_pos[0]][caster_pos[1]], self.atk_type)
            caster_pos = target_pos
        for observer in caster.observers_attack[::-1]:
            observer.attack_event(self, targets, self.game_board, self.atk_type)


class Burn(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "화상", "./PlayerCards/Tania/burn.png")
        game_board.register_turnover(self)

    def turnover_event(self, game_board):
        self.target.hit(1, self.target, [TAG_PYRO, TAG_BUFF])

        self.used(1)


class FlameShuriken(Skill):
    def __init__(self, game_board):
        super().__init__(3, game_board, [TAG_PYRO, TAG_BUFF, TAG_SKILL])
        self.name = "불꽃 수리검"
        self.explaination = [
            "cost : 3",
            "적 1명에게 불꽃 수리검을 날려서 1의 피해를 3번 가하고 1턴간 화상 효과를 부여한다. ",
            "화상 효과가 부여된 적은 턴 종료 시 체력이 1 감소한다. ",
            "화상 효과는 중첩될 수 있다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Tania/skill_image/flame_shuriken.png"

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = min(caster.specialSkill.energy + 1, caster.specialSkill.max_energy)
        for target_pos in targets_pos:
            target = self.game_board.gameBoard[target_pos[0]][target_pos[1]]
            pos1 = transform_pos(caster_pos)
            pos2 = transform_pos(target_pos)
            p1 = (pos1[0] + 100 * cos(pi / 3), pos1[1] + 200 * sin(pi / 3))
            p2 = (pos1[0] + 100 * cos(pi), pos1[1] + 200 * sin(pi))
            p3 = (pos1[0] + 100 * cos(-pi / 3), pos1[1] + 200 * sin(-pi / 3))
            for i in range(20):
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = i * 5 / sqrt(dx ** 2 + dy ** 2)
                    image = pygame.transform.scale(flame_shuriken, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180 + i * 30
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    size=image.get_size()
                    img_pos = (p1[0] + t * dx - size[0]/2, p1[1] + t * dy - size[1]/2)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i, (pos1, p1, i))
                motion_draw.add_motion(temp_move, i, (pos1, p2, i))
                motion_draw.add_motion(temp_move, i, (pos1, p3, i))
            for i in range(10):
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = 100 / sqrt(dx ** 2 + dy ** 2)
                    image = pygame.transform.scale(flame_shuriken, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180 + i * 30
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    size=image.get_size()
                    img_pos = (p1[0] + t * dx - size[0]/2, p1[1] + t * dy - size[1]/2)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i + 20, (pos1, p1, i + 20))
                motion_draw.add_motion(temp_move, i + 20, (pos1, p2, i + 20))
                motion_draw.add_motion(temp_move, i + 20, (pos1, p3, i + 20))

            i1 = 0
            while (i1 * 40 - 40) ** 2 < (p1[0] - pos2[0]) ** 2 + (p1[1] - pos2[1]) ** 2:
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = i * 40 / sqrt(dx ** 2 + dy ** 2)
                    image = pygame.transform.scale(flame_shuriken, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    size=image.get_size()
                    img_pos = (p1[0] + t * dx - size[0]/2, p1[1] + t * dy - size[1]/2)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i1 + 30, (p1, pos2, i1))
                i1 += 1
            i2 = 0
            while (i2 * 40 - 40) ** 2 < (p2[0] - pos2[0]) ** 2 + (p2[1] - pos2[1]) ** 2:
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = i * 40 / sqrt(dx ** 2 + dy ** 2)
                    image = pygame.transform.scale(flame_shuriken, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    size=image.get_size()
                    img_pos = (p1[0] + t * dx - size[0]/2, p1[1] + t * dy - size[1]/2)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i2 + 30, (p2, pos2, i2))
                i2 += 1
            i3 = 0
            while (i3 * 40 - 40) ** 2 < (p3[0] - pos2[0]) ** 2 + (p3[1] - pos2[1]) ** 2:
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = i * 40 / sqrt(dx ** 2 + dy ** 2)
                    image = pygame.transform.scale(flame_shuriken, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    size=image.get_size()
                    img_pos = (p1[0] + t * dx - size[0]/2, p1[1] + t * dy - size[1]/2)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i3 + 30, (p3, pos2, i3))
                i3 += 1

            def temp_damage(screen, *_):
                caster.attack(1, target, self.atk_type)
                for observer in caster.observers_attack[::-1]:
                    observer.attack_event(self, targets, self.game_board, self.atk_type)

            try:
                motion_draw.add_motion(lambda scr:Burn(target, 1, target.game_board), max(i1, i2, i3)+30, ())
            except:
                pass

            motion_draw.add_motion(temp_damage, i1 + 30, ())
            motion_draw.add_motion(temp_damage, i2 + 30, ())
            motion_draw.add_motion(temp_damage, i3 + 30, ())


class FlameSward(SpecialSkill):
    def __init__(self, game_board):
        super().__init__(4, 5, game_board, [TAG_PYRO, TAG_PENETRATE, TAG_SPECIAL_SKILL])
        self.name = "불의 칼날"
        self.explaination = [
            "cost : 4, energy : 5",
            "전방에 넓은 범위에 불의 칼날을 휘둘러 3의 관통 피해를 2번 입힌다. ",
            "관통 피해는 버프를 통해서 피해가 오르거나 내려가지 않는다. ",
            ", ".join(self.atk_type)
        ]
        self.skill_image_path = "./PlayerCards/Tania/skill_image/flame_sward.png"

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
                result += [(caster_pos[0], caster_pos[1] - 1),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0], caster_pos[1] + 1)]
        elif pos[0] == caster_pos[0] + 1 and caster_pos[0] != 5:
            while caster_pos[0] < 5:
                caster_pos = (caster_pos[0] + 1, caster_pos[1])
                result += [(caster_pos[0], caster_pos[1] - 1),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0], caster_pos[1] + 1)]
        elif pos[1] == caster_pos[1] - 1 and caster_pos[1] != 1:
            while caster_pos[1] > 1:
                caster_pos = (caster_pos[0], caster_pos[1] - 1)
                result += [(caster_pos[0] - 1, caster_pos[1]),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0] + 1, caster_pos[1])]
        elif pos[1] == caster_pos[1] + 1 and caster_pos[1] != 5:
            while caster_pos[1] < 5:
                caster_pos = (caster_pos[0], caster_pos[1] + 1)
                result += [(caster_pos[0] - 1, caster_pos[1]),
                           (caster_pos[0], caster_pos[1]),
                           (caster_pos[0] + 1, caster_pos[1])]
        return list(filter(lambda p: 0 < p[0] < 6 and 0 < p[1] < 6, result))

    def execute(self, caster, targets, caster_pos, targets_pos, execute_pos):
        caster.specialSkill.energy = 0
        execute_pos_real = transform_pos(execute_pos)
        def temp_func(screen, damage):
            for i in range(30):
                if caster_pos[0] > execute_pos[0]:
                    img = pygame.transform.rotate(flame_sward[min(i, 14)], 270)
                    img_position = (execute_pos_real[0], execute_pos_real[1] - i * 30)
                elif caster_pos[0] < execute_pos[0]:
                    img = pygame.transform.rotate(flame_sward[min(i, 14)], 90)
                    img_position = (execute_pos_real[0], execute_pos_real[1] + i * 30)
                elif caster_pos[1] > execute_pos[1]:
                    img = pygame.transform.rotate(flame_sward[min(i, 14)], 0)
                    img_position = (execute_pos_real[0] - i * 30, execute_pos_real[1])
                else:
                    img = pygame.transform.rotate(flame_sward[min(i, 14)], 180)
                    img_position = (execute_pos_real[0] + i * 30, execute_pos_real[1])
                img_size = img.get_size()
                motion_draw.add_motion(lambda screen, img, pos: screen.blit(img, pos), i,
                                       (img, (img_position[0] - img_size[0] / 2, img_position[1] - img_size[1] / 2)))
            for target in targets:
                target.hit(damage, caster, self.atk_type)
            for observer in caster.observers_attack:
                observer.attack_event(self, targets, self.game_board, self.atk_type)

        motion_draw.add_motion(temp_func, 10, (4,))
        motion_draw.add_motion(temp_func, 0, (3,))
