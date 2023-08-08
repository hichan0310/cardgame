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
from EnemyCards.Knight_beginner.knight_beginner import *
from EnemyCards.Archer_beginner.archer_beginner import *
from EnemyCards.Wizard_beginner.wizard_beginner import *
from EnemyCards.Shielder.shielder import *
from EnemyCards.Crossbow_archer.crossbow_archer import *
from graphic_manager import motion_draw

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
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
     "./EnemyCards/Knight_beginner/knight_beginner_card.png"],
    ["궁수 견습생", [Arrow], 7, [], AI_ArcherBiginner,
     "./EnemyCards/Archer_beginner/archer_beginner_card.png"],
    ["마법사 견습생", [EnergyBall], 6, [], AI_WizardBiginner,
     "./EnemyCards/Wizard_beginner/wizard_beginner_card.png"],
    ["방패병", [ShieldOfWrath, CounterAttack], 15, [], AI_Shielder,
     "./EnemyCards/Shielder/shielder_card.png"],
    ["석궁병", [PenetrateArrow, ContinuousFiring], 10, [], AI_Crossbow,
     "./EnemyCards/Crossbow_archer/crossbow_archer_card.png"]
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

def game_end(win):
    screen.fill("#000000")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        draw_text("WIN" if win else "LOSE", size=100, center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40), color="#FFFFFF")
        draw_text("마우스 클릭으로 나가기" if win else "LOSE", size=40, center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2+40), color="#FFFFFF")
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def main(p_info, e_info):
    game_board = GameMap(screen)
    for num, pos, color in p_info:
        game_board.add_character(characters_info[num], pos, color)
    for num, pos, color in e_info:
        game_board.add_enemy(enemies_info[num], pos, color)
    ai_enemy_index=0
    while True:
        if len(game_board.players)==0 and not motion_draw.motion_playing():
            return game_end, (False, )
        if len(game_board.enemys)==0 and not motion_draw.motion_playing():
            return game_end, (True, )
        bg = pygame.image.load("background.png")
        bg = pygame.transform.scale(bg, (1920, 1080))
        screen.blit(bg, (-1, -1))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_board.turn != 4:
                    game_board.click(event.pos)
        if game_board.turn == 4:
            if len(game_board.enemys)>ai_enemy_index:
                if not motion_draw.motion_playing():
                    game_board.AI_execute(ai_enemy_index)
                    ai_enemy_index+=1
                game_board.draw()
                draw_text(str(game_board.cost.cost), size=40, center=(830, 40), color=(0, 0, 0))
                motion_draw.draw(screen)
                pygame.display.update()
                clock.tick(FPS)
                continue
            else:
                if motion_draw.motion_playing():
                    game_board.draw()
                    draw_text(str(game_board.cost.cost), size=40, center=(830, 40), color=(0, 0, 0))
                    motion_draw.draw(screen)
                    pygame.display.update()
                    clock.tick(FPS)
                    continue
                else:
                    game_board.turnover()
                    game_board.turn = 0
                    ai_enemy_index=0
        game_board.draw()
        draw_text(str(game_board.cost.cost), size=40, center=(830, 40), color=(0, 0, 0))
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


func = main
params = ([(0, (1, 1), "#FF0000"),
           (1, (1, 2), "#FF0000"),
           (2, (1, 3), "#FF0000"),
           (4, (1, 4), "#FF0000")],
          [(3, (3, 3), "asdf"),
           (0, (3, 1), "asdf"),
           (0, (3, 2), "asdf"),
           (0, (3, 4), "asdf"),
           (0, (3, 5), "asdf"),
           (4, (4, 1), "asdf"),
           (4, (4, 5), "asdf"),
           (2, (5, 2), "asdf"),
           (2, (5, 4), "asdf")])
func=game_end
params=(True, )
while __name__ == "__main__":
    result = func(*params)
    func, params = result
