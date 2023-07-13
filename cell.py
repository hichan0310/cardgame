import pygame
from settings import *


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_center, visible, game_board, group):
        super().__init__(group)
        self.name="empty cell"
        self.pos_center = pos_center
        self.game_board = game_board
        self.item = None
        self.image = pygame.Surface(CARD_SIZE)
        self.image.fill("#000000")
        self.rect = self.image.get_rect(center=pos_center)
        self.mask = pygame.mask.from_surface(self.image)
        self.quick_move=False
        if not visible: self.image.set_alpha(0)

    def heal(self, heal_amount):
        pass

    def click(self):
        pass

    def update_location(self):
        self.rect = self.image.get_rect(center=self.pos_center)
        self.mask = pygame.mask.from_surface(self.image)
