import pygame
from gameMap import GameMap
from settings import *
import sys
from PlayerCards.Chloe.chloe import *
from PlayerCards.Tania.tania import *
from PlayerCards.Lucifer.lucifer import *
from PlayerCards.Petra.petra import *
from PlayerCards.Gidon.gidon import *
from PlayerCards.Astin.astin import *
from EnemyCards.Knight_beginner.knight_biginner import *
from EnemyCards.Archer_biginner.archer_biginner import *
from EnemyCards.Wizard_beginner.wizard_biginner import *
from EnemyCards.Shielder.shielder import *
from graphic_manager import motion_draw

screen = pygame.display.set_mode(SCREEN_SIZE)  # , pygame.FULLSCREEN)
pygame.init()

clock = pygame.time.Clock()
characters_info: list[str, tuple[list[Skill], SpecialSkill, int, int, list[Buff], str]] = [
    ["Chloe", [SproutOfBlue, SproutOfEarth], SproutOfReincarnation, 20, 4, [],
     "./PlayerCards/Chloe/chloe_card.png"],
    ["Tania", [StraightCut, FlameShuriken], FlameSward, 20, 5, [],
     "./PlayerCards/Tania/tania_card.png"],
    ["Lucifer", [CurseArrow, ExplodeCurse], CommingApocalypse, 20, 4, [],
     "./PlayerCards/Lucifer/lucifer_card.png"],
    ["Petra", [CrackOfEarth, SummonTurret], BaseCollapse, 20, 4, [BaseInstability],
     "./PlayerCards/Petra/petra_card.png"],
    ["Gidon", [BloodyBlow, VengeanceEye], UnfinishedRage, 20, 4, [],
     "./PlayerCards/Gidon/gidon_card.png"],
    ["Astin", [StarFall, NightSky], StarRain, 20, 5, [],
     "./PlayerCards/Astin/astin_card.png"]
]

enemies_info = [
    ["기사 견습생", [Sortie, PrepareDefence], 10, [], AI_KnightBiginner,
     "./EnemyCards/Knight_beginner/knight_biginner_card.png"],
    ["궁수 견습생", [Arrow], 7, [], AI_ArcherBiginner, "./EnemyCards/Archer_biginner/archer_biginner_card.png"],
    ["마법사 견습생", [EnergyBall], 6, [], AI_WizardBiginner, "./EnemyCards/Wizard_beginner/wizard_biginner_card.png"]
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


def main(p_info, e_info):
    game_board = GameMap(screen)
    for num, pos, color in p_info:
        game_board.add_character(characters_info[num], pos, color)
    for num, pos, color in e_info:
        game_board.add_enemy(enemies_info[num], pos, color)
    while True:
        bg = pygame.image.load("./background.png")
        bg = pygame.transform.scale(bg, (1920, 1080))
        screen.blit(bg, (-1, -1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return end,
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return end,
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_board.turn != 4:
                    game_board.click(event.pos)
        if game_board.turn == 4:
            game_board.AI_execute()
            game_board.turnover()
            game_board.turn = 0
        game_board.draw()
        draw_text(str(game_board.cost.cost), size=40, center=(830, 40), color=(0, 0, 0))
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


func = main
params = ([(2, (1, 1), "#FF0000"),
           (3, (1, 2), "#FF0000"),
           (4, (1, 3), "#FF0000"),
           (5, (1, 4), "#FF0000")],
          [(0, (5, 4), "asdf"),
           (1, (5, 5), "asdf"),
           (2, (5, 3), "asdf")])
while __name__ == "__main__":
    result = func(*params)
    func, *params = result
