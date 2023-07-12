import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.item=None

    def heal(self, heal_amount):
        pass