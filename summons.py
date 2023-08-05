import pygame
from cell import Cell
from buff import Buff
from graphic_manager import motion_draw
import random
from typing import TYPE_CHECKING
from settings import *

if TYPE_CHECKING:
    from playerCard import PlayerCard


class Summons(Cell):
    def __init__(self, count: int, pos: tuple[int, int], game_board, group, summoner: "PlayerCard", img_path,
                 pos_gameboard):
        super().__init__(pos, True, game_board, group, pos_gameboard)
        self.team = FLAG_SUMMONS
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, CARD_SIZE)
        self.name = "summons"
        self.count = count
        self.summoner = summoner
        self.dead = False
        self.__observers_die: list[Buff, Cell] = []

    def die(self):
        if self.dead:
            return
        for observer in self.__observers_die:
            observer.die_event(self, self.game_board)
        self.image.fill("#000000")
        self.dead = True

    def hit(self, damage, caster, atk_type):
        if self.dead:
            return
        self.count -= 1
        if self.count == 0:
            self.die()

    def penetrateHit(self, damage, caster):
        if self.dead:
            return
        self.hit(damage, caster, "penetrate")

    def draw_hp_energy(self, screen):
        if self.dead:
            return
        pygame.draw.circle(
            screen, color="#000000",
            center=(self.pos_center[0] + CARD_WIDTH / 2, self.pos_center[1] - CARD_HEIGHT / 2), radius=20)

        hp_font = pygame.font.Font("./D2Coding.ttf", 20)
        hp_text = hp_font.render(str(self.count), True, "#FFFFFF")
        hp_text_rect = hp_text.get_rect(
            center=(self.pos_center[0] + CARD_WIDTH / 2, self.pos_center[1] - CARD_HEIGHT / 2))
        screen.blit(hp_text, hp_text_rect)
