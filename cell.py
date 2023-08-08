import pygame
from settings import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_center, visible, game_board, group, pos_gameboard):
        super().__init__(group)
        self.pos_gameboard = pos_gameboard
        self.team = FLAG_EMPTY
        self.name = "empty cell"
        self.buff = []
        self.pos_center = pos_center
        self.game_board = game_board
        self.item = None
        self.image = pygame.Surface(CARD_SIZE)
        self.image.fill("#000000")
        self.rect = self.image.get_rect(center=pos_center)
        self.mask = pygame.mask.from_surface(self.image)
        self.quick_move = False
        self.observing_list = []
        if not visible: self.image.set_alpha(0)

    def curse_explode(self, caster):
        pass

    def heal(self, heal_amount):
        pass

    def click(self):
        pass

    def hit(self, damage, caster, atk_type):
        pass

    def penetrateHit(self, damage, caster, atk_type):
        pass

    def draw_hp_energy(self, screen):
        pass

    def update_location(self):
        self.rect = self.image.get_rect(center=self.pos_center)
        self.mask = pygame.mask.from_surface(self.image)

    def observing(self, observed_event):
        self.observing_list.append(observed_event)

    def atk_buff(self, caster, target, damage: int, atk_type: str):
        return damage

    def hit_buff(self, caster, target, damage: int, atk_type: str):
        return damage

    def hit_event(self, caster, target, game_board):
        pass

    def attack_event(self, caster, targets, game_board, atk_type):
        pass

    def die_event(self, player, game_board):
        pass

    def move_event(self, player, pos: tuple[int, int], game_board):
        pass

    def turnover_event(self, game_board):
        pass

    def turnstart_event(self, game_board):
        pass

    def curse_event(self, caster, target, game_board):
        pass
