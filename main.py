import pygame
from pygame.math import Vector2 as vec2
from gameMap import GameMap
from cell import Cell
from settings import *
import sys

pygame.init()

clock = pygame.time.Clock()

def draw_text(text, *, center=None, size=None, color=None):
    font = pygame.font.Font("./D2Coding.ttf", size or 24)
    text = font.render(text, True, color or (255, 255, 255))
    if center is None:
        text_rect = text.get_rect()
        text_rect.centerx = SCREEN_WIDTH // 2
        text_rect.centery = SCREEN_HEIGHT // 2
    else:
        text_rect = text.get_rect(center=center)
    screen.blit(text, text_rect)

def end(*_):
    pygame.quit()
    sys.exit()

def main(*_):
    game_board = GameMap(screen)
    game_board.add_character(0, (2, 3))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return end,
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_board.click(event.pos)
        screen.fill("#FFFFFF")
        game_board.draw()
        draw_text(str(game_board.cost.cost), size=40, center=(830, 40), color=(0, 0, 0))
        pygame.display.update()
        clock.tick(FPS)


func = main
params = ()
while __name__ == "__main__":
    result = func(*params)
    func, *params = result
