from cell import *
from skill import Skill
from buff import Buff
from settings import *
import random
from graphic_manager import motion_draw


class EnemyCard(Cell):
    def __init__(self, character_params, pos: tuple[int, int], game_board, group, pos_game_board):
        super().__init__(pos, True, game_board, group, pos_game_board)
        self.team = FLAG_ENEMY_TEAM
        self.skills: list[Skill]
        self.hp: int
        self.max_energy: int
        self.buff: list[Buff] = []
        self.passive: list[Buff] = []
        self.name, self.skills, self.max_hp, self.passive, self.limit_hp, self.ai, self.img_path = character_params
        t = []
        for passive_buff in self.passive:
            t.append(passive_buff(self, game_board))
        self.passive = t
        self.skills = [*map(lambda a: a(game_board), self.skills)]
        self.ai = self.ai(game_board, self)
        if self.img_path is not None:
            self.image = pygame.image.load(self.img_path)
            self.image = pygame.transform.scale(self.image, CARD_SIZE)
        self.hp = self.max_hp
        self.observers_curse: list[Buff, Cell] = []
        self.observers_hit: list[Buff, Cell] = []
        self.observers_attack: list[Buff, Cell] = []
        self.observers_die: list[Buff, Cell] = []
        self.observers_move: list[Buff, Cell] = []
        self.shield = 0
        self.dead = False

    def draw_hp_energy(self, screen):
        if self.dead:
            return
        pygame.draw.circle(
            screen, color="#000000",
            center=(self.pos_center[0] + CARD_WIDTH / 2, self.pos_center[1] - CARD_HEIGHT / 2), radius=20)

        hp_font = pygame.font.Font("./D2Coding.ttf", 20)
        hp_text = hp_font.render(str(self.hp), True, "#FFFFFF")
        hp_text_rect = hp_text.get_rect(
            center=(self.pos_center[0] + CARD_WIDTH / 2, self.pos_center[1] - CARD_HEIGHT / 2))
        screen.blit(hp_text, hp_text_rect)
        if len(self.buff) != 0:
            pygame.draw.circle(
                screen, color="#000000",
                center=(self.pos_center[0] - CARD_WIDTH / 2, self.pos_center[1] + CARD_HEIGHT / 2), radius=20)
            hp_font = pygame.font.Font("./D2Coding.ttf", 20)
            hp_text = hp_font.render(str(len(self.buff)), True, "#FFFFFF")
            hp_text_rect = hp_text.get_rect(
                center=(self.pos_center[0] - CARD_WIDTH / 2, self.pos_center[1] + CARD_HEIGHT / 2))
            screen.blit(hp_text, hp_text_rect)

    def register_hit(self, observer: "Buff, Cell"):
        self.observers_hit.append(observer)
        observer.observing(self.observers_hit)

    def register_attack(self, observer: "Buff, Cell"):
        self.observers_attack.append(observer)
        observer.observing(self.observers_attack)

    def register_die(self, observer: "Buff, Cell"):
        self.observers_die.append(observer)
        observer.observing(self.observers_die)

    def register_move(self, observer: "Buff, Cell"):
        self.observers_move.append(observer)
        observer.observing(self.observers_move)

    def register_curse(self, observer: "Buff, Cell"):
        self.observers_curse.append(observer)
        observer.observing(self.observers_curse)

    def curse_explode(self, caster):
        if self.dead: return
        for observer in self.observers_curse[::-1]:
            observer.curse_event(caster, self, self.game_board)

    def hit(self, damage, caster, atk_type):
        if self.dead: return
        if TAG_PENETRATE in atk_type:
            self.penetrateHit(damage, caster, atk_type)
            return
        for b in self.buff[::-1]:
            damage = b.hit_buff(caster, self, damage, atk_type)
        self.hp -= damage
        a = random.random() * 2 - 1
        b = random.random() * 2 - 1
        for _ in range(15):
            def temp_func(screen, pos, i):
                damage_font = pygame.font.Font("./D2Coding.ttf", 40)
                damage_text = damage_font.render(str(-damage), True, "#FFFFFF", "#000000")
                damage_text_rect = damage_text.get_rect(
                    center=(pos[0], pos[1] - 60 + 50 / i * 2))
                screen.blit(damage_text, damage_text_rect)

            motion_draw.add_motion(temp_func, _, ((self.pos_center[0] + a * 10, self.pos_center[1] + b * 10), _ + 1))
        if self.limit_hp is not None:
            if self.hp < self.limit_hp:
                self.hp = self.limit_hp
        if self.hp <= 0:
            self.die()
        for observer in self.observers_hit[::-1]:
            observer.hit_event(caster, self, self.game_board, atk_type, damage)

    def penetrateHit(self, damage, caster, atk_type):
        if self.dead: return
        self.hp -= damage
        a = random.random() * 2 - 1
        b = random.random() * 2 - 1
        for _ in range(15):
            def temp_func(screen, pos, i):
                damage_font = pygame.font.Font("./D2Coding.ttf", 30)
                damage_text = damage_font.render("관통 " + str(-damage), True, "#FFFFFF", "#000000")
                damage_text_rect = damage_text.get_rect(
                    center=(pos[0], pos[1] - 60 + 50 / i * 2))
                screen.blit(damage_text, damage_text_rect)

            motion_draw.add_motion(temp_func, _, ((self.pos_center[0] + a * 20, self.pos_center[1] + b * 20), _ + 1))
        if self.limit_hp is not None:
            if self.hp < self.limit_hp:
                self.hp = self.limit_hp
        if self.hp <= 0:
            self.die()
        for observer in self.observers_hit[::-1]:
            observer.hit_event(caster, self, self.game_board, atk_type + [TAG_PENETRATE], damage)

    def attack(self, damage, target, atk_type):
        if self.dead: return
        for b in self.buff[::-1]:
            damage = b.atk_buff(self, target, damage, atk_type)
        target.hit(damage, self, atk_type)

    def die(self):
        if self.dead: return
        for observer in self.observers_die[::-1]:
            observer.die_event(self, self.game_board)
        self.image.fill("#000000")
        self.game_board.enemys.remove(self)
        self.game_board.gameBoard[self.pos_gameboard[0]][self.pos_gameboard[1]] = Cell(self.pos_center,
                                                                                       True,
                                                                                       self.game_board,
                                                                                       self.game_board.group,
                                                                                       self.pos_gameboard)
        self.dead = True
        self.image.set_alpha(0)
        self.kill()

    def heal(self, heal_amount):
        if self.dead: return
        hp_before = self.hp
        self.hp = min(self.max_hp, self.hp + heal_amount)
        a = random.random() * 2 - 1
        b = random.random() * 2 - 1
        for _ in range(8):
            def temp_func(screen, pos, i):
                damage_font = pygame.font.Font("./D2Coding.ttf", 30)
                damage_text = damage_font.render('+' + str(self.hp - hp_before), True, "#FFFFFF", "#000000")
                damage_text_rect = damage_text.get_rect(
                    center=(pos[0], pos[1] - 60 + 50 / i))
                screen.blit(damage_text, damage_text_rect)

            motion_draw.add_motion(temp_func, _, ((self.pos_center[0] + a * 20, self.pos_center[1] + b * 20), _ + 1))

    def move(self, pos):
        if self.dead: return
        for observer in self.observers_move[::-1]:
            observer.move_event(self, pos, self.game_board)

    def click(self):
        pass
