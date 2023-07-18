import pygame.image

from skill import Skill, SpecialSkill
from buff import Buff
from graphic_manager import motion_draw
from typing import TYPE_CHECKING
from settings import *
from math import sqrt, atan, pi, sin, cos

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
        for observer in caster.observers_attack:
            observer.attack_event(self, targets, self.game_board, "normal attack")


class Burn(Buff):
    def __init__(self, character: "PlayerCard", count: int, game_board):
        super().__init__(character, count, game_board, "화상", "./Tania/burn.png")
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
                    img_pos = (p1[0] + t * dx - 60, p1[1] + t * dy - 60)
                    image = pygame.image.load("./Tania/skill_motion/flame_shuriken/0.png")
                    image = pygame.transform.scale(image, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180 + i * 15
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i, (pos1, p1, i))
                motion_draw.add_motion(temp_move, i, (pos1, p2, i))
                motion_draw.add_motion(temp_move, i, (pos1, p3, i))
            for i in range(40):
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = 100 / sqrt(dx ** 2 + dy ** 2)
                    img_pos = (p1[0] + t * dx - 60, p1[1] + t * dy - 60)
                    image = pygame.image.load("./Tania/skill_motion/flame_shuriken/0.png")
                    image = pygame.transform.scale(image, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180 + i * 15
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
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
                    img_pos = (p1[0] + t * dx - 60, p1[1] + t * dy - 60)
                    image = pygame.image.load("./Tania/skill_motion/flame_shuriken/0.png")
                    image = pygame.transform.scale(image, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i1 + 60, (p1, pos2, i1))
                i1 += 1
            i2 = 0
            while (i2 * 40 - 40) ** 2 < (p2[0] - pos2[0]) ** 2 + (p2[1] - pos2[1]) ** 2:
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = i * 40 / sqrt(dx ** 2 + dy ** 2)
                    img_pos = (p1[0] + t * dx - 60, p1[1] + t * dy - 60)
                    image = pygame.image.load("./Tania/skill_motion/flame_shuriken/0.png")
                    image = pygame.transform.scale(image, (120, 120))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i2 + 60, (p2, pos2, i2))
                i2 += 1
            i3 = 0
            while (i3 * 40 - 40) ** 2 < (p3[0] - pos2[0]) ** 2 + (p3[1] - pos2[1]) ** 2:
                def temp_move(screen, p1, p2, i):
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    t = i * 40 / sqrt(dx ** 2 + dy ** 2)
                    img_pos = (p1[0] + t * dx - 50, p1[1] + t * dy - 50)
                    image = pygame.image.load("./Tania/skill_motion/flame_shuriken/0.png")
                    image = pygame.transform.scale(image, (100, 100))
                    angle = -atan(dy / (dx - 0.00001)) / pi * 180
                    if dx > 0: angle += 180
                    image = pygame.transform.rotate(image, angle)
                    screen.blit(image, img_pos)

                motion_draw.add_motion(temp_move, i3 + 60, (p3, pos2, i3))
                i3 += 1

            def temp_damage(screen, *_):
                caster.attack(1, target, "skill")
                for observer in caster.observers_attack:
                    observer.attack_event(self, targets, self.game_board, "skill")

            try:
                Burn(target, 1, target.game_board)
            except:
                pass

            motion_draw.add_motion(temp_damage, i1 + 60, ())
            motion_draw.add_motion(temp_damage, i2 + 60, ())
            motion_draw.add_motion(temp_damage, i3 + 60, ())


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
        caster_pos_real = transform_pos(caster_pos)
        for i in range(40):
            img1 = pygame.image.load(f"./Tania/skill_motion/flame_sward/14.png")
            img2 = pygame.image.load(f"./Tania/skill_motion/flame_sward/14.png")
            img1 = pygame.transform.rotate(img1, 270)
            img2 = pygame.transform.rotate(img2, 90)
            img1 = pygame.transform.scale(img1, (((39 - i) * 40), 2 * ((39 - i) * 40) / 3))
            img2 = pygame.transform.scale(img2, (((39 - i) * 40), 2 * ((39 - i) * 40) / 3))
            motion_draw.add_motion(
                lambda screen, img, pos: screen.blit(img, pos), i,
                (img1, (caster_pos_real[0] - ((39 - i) * 40) / 2,
                        caster_pos_real[1] - ((39 - i) * 40) / 3*2))
            )
            motion_draw.add_motion(
                lambda screen, img, pos: screen.blit(img, pos), i,
                (img2, (caster_pos_real[0] - ((39 - i) * 40) / 2,
                        caster_pos_real[1]))
            )


        def temp_func(screen, damage):
            for i in range(30):
                img = pygame.image.load(f"./Tania/skill_motion/flame_sward/{min(i, 14)}.png")
                if caster_pos[0] > execute_pos[0]:
                    img = pygame.transform.rotate(img, 270)
                    img_position = (execute_pos_real[0], execute_pos_real[1] - i * 30)
                elif caster_pos[0] < execute_pos[0]:
                    img = pygame.transform.rotate(img, 90)
                    img_position = (execute_pos_real[0], execute_pos_real[1] + i * 30)
                elif caster_pos[1] > execute_pos[1]:
                    img = pygame.transform.rotate(img, 0)
                    img_position = (execute_pos_real[0] - i * 30, execute_pos_real[1])
                else:
                    img = pygame.transform.rotate(img, 180)
                    img_position = (execute_pos_real[0] + i * 30, execute_pos_real[1])
                img_size = img.get_size()
                motion_draw.add_motion(lambda screen, img, pos: screen.blit(img, pos), i,
                                       (img, (img_position[0] - img_size[0] / 2, img_position[1] - img_size[1] / 2)))
            for target in targets:
                target.penetrateHit(damage, caster)
            for observer in caster.observers_attack:
                observer.attack_event(self, targets, self.game_board, "penetrate hit")

        motion_draw.add_motion(temp_func, 80, (4, ))
        motion_draw.add_motion(temp_func, 60, (3, ))
