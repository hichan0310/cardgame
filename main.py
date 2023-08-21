import pygame
import time
from gameMap import GameMap
from select_character import SelectCharacter
from settings import *
import sys
from graphic_manager import motion_draw
pygame.init()

from EventCards.BombThrowing.bomb_throwing import BombThrowing
from EventCards.EnergyRecharge.energy_recharge import EnergyRecharge
from EventCards.EnforceHit.enforce_hit import EnforceHit
from EventCards.FireSward.fire_sward import FireSward
from EventCards.HealingLight.healing_light import HealingLight
from EventCards.Lucky.lucky import Lucky
from EventCards.ManaSynthesizer.mana_synthesizer import ManaSynthesizer
from EventCards.SecondOpportunity.second_opertunity import SecondOpertunity
from EventCards.Sniping.sniping import Sniping
from EventCards.WarpGateOpen.warp_gate import WarpGate

from characters import *

"""
def loading(p):
    screen.fill("#000000")
    draw_text(f"loading : {p}%", size=30, center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), color="#FFFFFF")
    pygame.draw.rect(screen, "#FFFFFF", (0, 1040, p*SCREEN_WIDTH/100, 40), 40)
    pygame.display.update()


gacha_yonchool = [
    [(pygame.transform.scale(pygame.image.load(f"./gacha/tania/frame_{i}.png"), SCREEN_SIZE),
      loading(100 * (i) / (383 * 6)))[0] for i in range(383)],
    [(pygame.transform.scale(pygame.image.load(f"./gacha/chloe/frame_{i}.png"), SCREEN_SIZE),
      loading(100 * (i + 383) / (383 * 6)))[0] for i in range(383)],
    [(pygame.transform.scale(pygame.image.load(f"./gacha/lucifer/frame_{i}.png"), SCREEN_SIZE),
      loading(100 * (i + 383 * 2) / (383 * 6)))[0] for i in range(383)],
    [(pygame.transform.scale(pygame.image.load(f"./gacha/gidon/frame_{i}.png"), SCREEN_SIZE),
      loading(100 * (i + 383 * 3) / (383 * 6)))[0] for i in range(383)],
    [(pygame.transform.scale(pygame.image.load(f"./gacha/astin/frame_{i}.png"), SCREEN_SIZE),
      loading(100 * (i + 383 * 4) / (383 * 6)))[0] for i in range(383)],
    [(pygame.transform.scale(pygame.image.load(f"./gacha/petra/frame_{i}.png"), SCREEN_SIZE),
      loading(100 * (i + 383 * 5) / (383 * 6)))[0] for i in range(383)]
]


def gacha():
    images_banner = [
        pygame.transform.scale(pygame.image.load("./gacha/charactercard_gacha_banner.png"), SCREEN_SIZE),
        pygame.transform.scale(pygame.image.load("./gacha/eventcard_gacha_banner.png"), SCREEN_SIZE)
    ]
    button = [
        pygame.transform.scale(pygame.image.load("gacha/gacha_button_character.png"), (300, 150)),
        pygame.transform.scale(pygame.image.load("gacha/gacha_button_event.png"), (300, 150))
    ]
    gachamode = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 < x < 400 and 200 < y < 350:
                    gachamode = 0
                if 100 < x < 400 and 400 < y < 550:
                    gachamode = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return main, ()
        screen.blit(images_banner[gachamode], (0, 0))
        screen.blit(button[0], (100, 200))
        screen.blit(button[1], (100, 400))
        pygame.display.update()
        clock.tick(FPS)


def gacha_charactercard():
    result = random.randint(1, 10)
    if result > 5:
        result = 0
    for i in range(170):
        screen.blit(gacha_yonchool[result][i], (0, 0))
        pygame.display.update()
        clock.tick(FPS / 2)
    draw_text("클릭하여 카드 확인", size=30, color="#FFFFFF")
    pygame.display.update()
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
    for i in range(230, 383):
        screen.blit(gacha_yonchool[result][i], (0, 0))
        pygame.display.update()
        clock.tick(FPS/2)
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
    return gacha, ()
"""




def end(*_):
    pygame.quit()
    sys.exit()


def main(*_):
    background = pygame.image.load("main_background.png")
    screen.blit(background, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 706 < x < 1216 and 392 < y < 505:
                    return select_stage, ()
                if 706 < x < 1216 and 537 < y < 651:
                    return forming, ()
                if 706 < x < 1216 and 684 < y < 800:
                    return dogam, ()
                if 706 < x < 1216 and 829 < y < 943:
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return end, ()


def select_stage(stage=0):
    stage_num = stage
    while True:
        screen.fill("#000000")
        screen.blit(
            pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % (len(stage_list) + 1)}.png"),
                                   (800, 800)),
            (SCREEN_WIDTH / 2 - 400, SCREEN_HEIGHT / 2 - 500))
        draw_text("방향키로 스테이지 이동, 스테이지를 클릭하여 시작하기",
                  center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150), size=50, color="#FFFFFF")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    stage_num -= 1 if stage_num >= 0 else 0
                if event.key == pygame.K_RIGHT:
                    stage_num += 1 if stage_num < len(stage_list) else 0
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    return main, ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_WIDTH / 2 - 400 < event.pos[0] < SCREEN_WIDTH / 2 + 400 and SCREEN_HEIGHT / 2 - 500 < \
                        event.pos[1] < SCREEN_HEIGHT / 2 + 300 and -1 < stage_num < len(stage_list):
                    return select_character, (stage_num,)
        motion_draw.draw(screen)
        pygame.display.update()


e_card_list = [
    BombThrowing,
    EnergyRecharge,
    EnforceHit,
    FireSward,
    HealingLight,
    Lucky,
    ManaSynthesizer,
    SecondOpertunity,
    Sniping,
    WarpGate,
]
e_cards = [2 for _ in range(len(e_card_list))]
e_card_list = e_card_list * 2


def select_character(stage_num):
    game_board = SelectCharacter(stage_num, screen)
    while True:
        screen.fill("#333333")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_board.click(event.pos)
                x, y = event.pos
                if SCREEN_WIDTH - 500 < x < SCREEN_WIDTH - 100 and SCREEN_HEIGHT - 300 < y < SCREEN_HEIGHT - 100:
                    if len(game_board.result) != 0:
                        return game, (game_board.result, stage_list[stage_num], e_card_list)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return select_stage, (stage_num,)
        game_board.draw()
        screen.blit(pygame.transform.scale(pygame.image.load("start.png"), (400, 200)),
                    (SCREEN_WIDTH - 500, SCREEN_HEIGHT - 300))
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def forming():
    global e_cards, e_card_list
    screen.fill("#333333")
    cards = e_cards
    images = [pygame.transform.scale(pygame.image.load(img_path), (200, 300))
              for _, _, img_path, _, _ in event_card_info.values()]
    while True:
        screen.fill("#333333")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(10):
                    center_pos = (SCREEN_WIDTH / 2 + (i % 5 - 2) * 250, SCREEN_HEIGHT / 2 + (i // 5 - 0.5) * 400 - 50)
                    if center_pos[0] - 100 < x < center_pos[0] + 100 and center_pos[1] - 150 < y < center_pos[1] + 150:
                        cards[i] = (cards[i] + 1) % 3
                if 893 < x < 1026 and 966 < y < 991 and sum(cards) >= 15:
                    e_cards = cards
                    e_card_list = [Sniping for _ in range(cards[0])] + \
                                  [HealingLight for _ in range(cards[1])] + \
                                  [EnergyRecharge for _ in range(cards[2])] + \
                                  [Lucky for _ in range(cards[3])] + \
                                  [WarpGate for _ in range(cards[4])] + \
                                  [EnforceHit for _ in range(cards[5])] + \
                                  [SecondOpertunity for _ in range(cards[6])] + \
                                  [BombThrowing for _ in range(cards[7])] + \
                                  [ManaSynthesizer for _ in range(cards[8])] + \
                                  [FireSward for _ in range(cards[3])]
                    return main, ()
        if sum(cards) >= 15:
            draw_text("편성 완료", center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100), color="#FFFFFF", size=30)
        else:
            draw_text("15개 이상을 선택해야 합니다", center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100), color="#FFFFFF", size=30)
        for i in range(10):
            center_pos = (SCREEN_WIDTH / 2 + (i % 5 - 2) * 250, SCREEN_HEIGHT / 2 + (i // 5 - 0.5) * 400 - 50)
            screen.blit(images[i], (center_pos[0] - 100, center_pos[1] - 150))
            draw_text(str(cards[i]), color="#FFFFFF", center=(center_pos[0], center_pos[1] + 180), size=30)
        pygame.display.update()
    return main, ()


def draw_skill(skill, index):
    background = pygame.Surface(((SKILL_WIDTH + 20) * 4 - 20, SKILL_HEIGHT))
    background.fill("#000000")
    bg_rect = background.get_rect(
        center=(
            SCREEN_WIDTH / 2 + 30 - SKILL_WIDTH / 2 + (SKILL_WIDTH + 20) * 2 - 100,
            SCREEN_HEIGHT - 100 - 600 + index * 170 - 100))
    screen.blit(background, bg_rect)

    font = pygame.font.Font("./D2Coding.ttf", 26)
    text = font.render(skill.name, True, "#FFFFFF")
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2 + 40 - 100, SCREEN_HEIGHT - 50 - 600 + index * 170 - 100))
    screen.blit(text, text_rect)

    image = pygame.image.load(skill.skill_image_path)
    image = pygame.transform.scale(image, (80, 80))
    pos = (SCREEN_WIDTH / 2 + 40 - 40 - 100, SCREEN_HEIGHT - 60 - 35 - 60 - 600 + index * 170 - 100)
    screen.blit(image, pos)

    center_pos = (SCREEN_WIDTH / 2 + 40 + 40 - 100, SCREEN_HEIGHT - 60 - 35 - 60 - 600 + index * 170 - 100)
    pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
    draw_text(str(skill.cost), center=center_pos, color="#FFFFFF", size=16)
    try:
        if skill.max_energy is not None:
            center_pos = (SCREEN_WIDTH / 2 + 40 + 40 - 100, SCREEN_HEIGHT - 60 - 35 - 60 + 20 - 600 + index * 170 - 100)
            pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
            draw_text(str(skill.max_energy), center=center_pos, color="#FFFFFF", size=16)
    except:
        pass

    i = 0
    for t in skill.explaination:
        font = pygame.font.Font("./D2Coding.ttf", 14)
        text = font.render(t, True, "#FFFFFF")
        text_rect = text.get_rect(centery=SCREEN_HEIGHT - 150 + i * 19 - 600 + index * 170 - 100, left=SCREEN_WIDTH / 2 + 40)
        screen.blit(text, text_rect)
        i += 1


def draw_eventcard(eventcard_key, movement):
    x, y = movement
    x -= 900
    y -= 10
    name, cost, img_path, explaination, exe_type = event_card_info[eventcard_key]
    background = pygame.Surface((860, 160))
    background.fill("#000000")
    bg_rect = background.get_rect(
        center=(1330 + x, 330 + y))
    screen.blit(background, bg_rect)

    font = pygame.font.Font("./D2Coding.ttf", 20)
    text = font.render(name, True, "#FFFFFF")
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2 + 40 + x, SCREEN_HEIGHT - 50 - 650 + y))
    screen.blit(text, text_rect)

    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (60, 90))
    pos = (SCREEN_WIDTH / 2 + 40 - 30 + x, SCREEN_HEIGHT - 60 - 30 - 60 - 650 + y)
    screen.blit(image, pos)

    center_pos = (SCREEN_WIDTH / 2 + 40 + 40 + x, SCREEN_HEIGHT - 60 - 35 - 60 - 650 + y)
    pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
    draw_text(str(cost), center=center_pos, color="#FFFFFF", size=16)

    i = 0
    for t in explaination:
        font = pygame.font.Font("./D2Coding.ttf", 14)
        text = font.render(t, True, "#FFFFFF")
        text_rect = text.get_rect(centery=SCREEN_HEIGHT - 150 + i * 19 - 650 + y, left=SCREEN_WIDTH / 2 + 140 + x)
        screen.blit(text, text_rect)
        i += 1


def dogam_character(*_):
    background = pygame.image.load("dogam_char.png")
    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 59 < x < 351 and 144 < y < 1015:
                    return dogam_character_index, (0,)
                if 360 < x < 652 and 144 < y < 1015:
                    return dogam_character_index, (1,)
                if 662 < x < 955 and 144 < y < 1015:
                    return dogam_character_index, (2,)
                if 964 < x < 1257 and 144 < y < 1015:
                    return dogam_character_index, (3,)
                if 1265 < x < 1558 and 144 < y < 1015:
                    return dogam_character_index, (4,)
                if 1565 < x < 1859 and 144 < y < 1015:
                    return dogam_character_index, (5,)
                if 60 < x < 292 and 38 < y < 103:
                    return dogam, ()
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def dogam_character_index(index):
    name, skills, specialskill, hp, energy, passive, img_path, color = characters_info[index]
    bg_img = pygame.image.load(f"./dogam_background/{name}.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1713 < x < 1872 and 42 < y < 88:
                    return dogam_character, ()
        screen.blit(bg_img, (0, 0))
        draw_skill(skills[0](None), 0)
        draw_skill(skills[1](None), 1)
        draw_skill(specialskill(None), 2)
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def dogam_enemy(*_):
    screen.fill("#333333")
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index = min(len(enemies_info) - 1, index + 1)
                    screen.fill("#333333")
                if event.key == pygame.K_LEFT:
                    index = max(0, index - 1)
                    screen.fill("#333333")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        return dogam, ()
        name, skills, hp, passive, _, ai, img_path = enemies_info[index]
        img = pygame.transform.scale(pygame.image.load(img_path), (600, 900))
        font = pygame.font.Font("./D2Coding.ttf", 60)
        text = font.render(name, True, "#FFFFFF")
        text_rect = text.get_rect(centery=100, left=900)
        screen.blit(text, text_rect)
        screen.blit(img, (100, 90))
        for i in range(len(skills)):
            draw_skill(skills[i](None), i)
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def dogam_eventcard(*_):
    screen.fill("#333333")
    i = 0
    for key in event_card_info.keys():
        draw_eventcard(key, (70 + 920 * (i % 2), (i // 2) * 180 - 150))
        i += 1
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return dogam, ()
        clock.tick(FPS)


def dogam():
    background = pygame.transform.scale(pygame.image.load("dogam.png"), SCREEN_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 203 < event.pos[0] < 645 and 420 < event.pos[1] < 833:
                    return dogam_character, ()
                if 750 < event.pos[0] < 1189 and 420 < event.pos[1] < 833:
                    return dogam_enemy, ()
                if 1262 < event.pos[0] < 1676 and 434 < event.pos[1] < 815:
                    return dogam_eventcard, ()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return main, ()
        screen.blit(background, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def game_end(win):
    screen.fill("#000000")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return main, ()
        draw_text("WIN" if win else "LOSE", size=100, center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40),
                  color="#FFFFFF")
        draw_text("마우스 클릭으로 나가기" if win else "LOSE", size=40, center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40),
                  color="#FFFFFF")
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def game(p_info, e_info, eventcard_list):
    game_board = GameMap(screen, eventcard_list)
    bg = pygame.image.load("background.png")
    bg = pygame.transform.scale(bg, (1920, 1080))
    for num, pos in p_info:
        game_board.add_character(characters_info[num], pos)
    for num, pos in e_info:
        game_board.add_enemy(enemies_info[num], pos)
    ai_enemy_index = 0
    while True:
        if len(game_board.players) == 0 and not motion_draw.motion_playing():
            return game_end, (False,)
        if len(game_board.enemys) == 0 and not motion_draw.motion_playing():
            return game_end, (True,)
        screen.blit(bg, (-1, -1))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_board.turn != 4:
                    game_board.click(event.pos)
        if game_board.turn == 4:
            if len(game_board.enemys) > ai_enemy_index:
                if not motion_draw.motion_playing():
                    game_board.AI_execute(ai_enemy_index)
                    ai_enemy_index += 1
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
                    ai_enemy_index = 0
                    game_board.turnstart()
        game_board.draw()
        draw_text(str(game_board.cost.cost), size=40, center=(830, 40), color=(0, 0, 0))
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)








func = main

params = ()
while __name__ == "__main__":
    result = func(*params)
    func, params = result
