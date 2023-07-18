import pygame
from gameMap import GameMap
from settings import *
import sys
from Chloe.chloe import *
from Tania.tania import *
from Lucifer.lucifer import *
from Petra.petra import *
from Gidon.gidon import *
from Astin.astin import *
from graphic_manager import motion_draw
from copy import deepcopy

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.init()

clock = pygame.time.Clock()
game_board = GameMap(screen)
characters_info: list[str, tuple[list[Skill], SpecialSkill, int, int, list[Buff], str]] = [
    ["Chloe", [SproutOfBlue(game_board), SproutOfEarth(game_board)], SproutOfReincarnation(game_board), 20, 4, [],
     "./Chloe/chloe_card.png"],
    ["Tania", [StraightCut(game_board), FlameShuriken(game_board)], FlameSward(game_board), 20, 5, [],
     "./Tania/tania_card.png"],
    ["Lucifer", [CurseArrow(game_board), ExplodeCurse(game_board)], CommingApocalypse(game_board), 20, 4, [],
     "./Lucifer/lucifer_card.png"],
    ["Petra", [CrackOfEarth(game_board), SummonTurret(game_board)], BaseCollapse(game_board), 20, 4, [BaseInstability],
     "./Petra/petra_card.png"],
    ["Gidon", [BloodyBlow(game_board), VengeanceEye(game_board)], UnfinishedRage(game_board), 20, 4, [],
     "./Gidon/gidon_card.png"],
    ["Astin", [StarFall(game_board), NightSky(game_board)], StarRain(game_board), 20, 5, [],
     "./Astin/astin_card.png"]
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
    game_board.add_character(characters_info[0], (3, 3), "#00FF00")
    game_board.add_character(characters_info[1], (3, 4), "#FF0000")
    game_board.add_character(characters_info[2], (3, 2), "#FF00FF")
    game_board.add_character(characters_info[3], (3, 5), "#FFFFFF")
    game_board.add_character(characters_info[4], (3, 1), (217, 77, 60))
    game_board.add_character(characters_info[5], (2, 1), (0, 51, 235))
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
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


func = main
params = ()
while __name__ == "__main__":
    result = func(*params)
    func, *params = result
