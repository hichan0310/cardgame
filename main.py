import pygame
from gameMap import GameMap
from settings import *
import sys
from Chloe.chloe import *
from Tania.tania import *

pygame.init()

clock = pygame.time.Clock()
game_board = GameMap(screen)
characters_info:list[str, tuple[list[Skill], SpecialSkill, int, int, str]]=[
    ("Chloe", [SproutOfBlue(game_board), SproutOfEarth(game_board)], SproutOfReincarnation(game_board), 10, 4, "./Chloe/chloe_card.png"),
    ("Tania", [StraightCut(game_board)], FireSward(game_board), 10, 4, "./Tania/tania_card.png")
]

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
    game_board.add_character(characters_info[0], (2, 3))
    game_board.add_character(characters_info[1], (3, 4))
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
