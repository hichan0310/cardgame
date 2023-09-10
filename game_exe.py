import pygame
import time
from gameMap import GameMap
from select_character import SelectCharacter
from settings import *
import sys
import csv
import threading
from graphic_manager import motion_draw
import pygame.mixer

pygame.init()
pygame.mixer.init()

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

screen.fill("#000000")
draw_text("캐릭터에 대한 자세한 설명은 영상 설명란 링크에 있습니다", size=30, color="#FFFFFF", center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-20))
draw_text("도감의 내용을 분석하여 알 수는 있지만 어려울 수도 있습니다", size=30, color="#FFFFFF", center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+20))
pygame.display.update()

gacha_loading = []
gacha_yonchool_char = [[], [], [], [], [], []]


def loading(p):
    print(f"\rloading : {p}%                             ", end='')


def load_gacha():
    for i in range(170):
        gacha_loading.append(pygame.image.load(f"./gacha/tania/frame_{i}.png"))
        loading(100 * (i + 1) / 1088)
    for i in range(230, 383):
        gacha_yonchool_char[0].append(pygame.image.load(f"./gacha/tania/frame_{i}.png"))
        loading(100 * (i + 1 - 60) / 1088)
    for i in range(230, 383):
        gacha_yonchool_char[1].append(pygame.image.load(f"./gacha/chloe/frame_{i}.png"))
        loading(100 * (i + 1 + 93) / 1088)
    for i in range(230, 383):
        gacha_yonchool_char[2].append(pygame.image.load(f"./gacha/lucifer/frame_{i}.png"))
        loading(100 * (i + 1 + 246) / 1088)
    for i in range(230, 383):
        gacha_yonchool_char[3].append(pygame.image.load(f"./gacha/gidon/frame_{i}.png"))
        loading(100 * (i + 1 + 399) / 1088)
    for i in range(230, 383):
        gacha_yonchool_char[4].append(pygame.image.load(f"./gacha/astin/frame_{i}.png"))
        loading(100 * (i + 1 + 552) / 1088)
    for i in range(230, 383):
        gacha_yonchool_char[5].append(pygame.image.load(f"./gacha/petra/frame_{i}.png"))
        loading(100 * (i + 1 + 705) / 1088)


loadgacha = threading.Thread(target=load_gacha)
loadgacha.start()

opening = []


def load_opening():
    for i in range(605):
        opening.append(pygame.image.load(f"./opening/{i}.png"))


loadopening = threading.Thread(target=load_opening)
loadopening.start()
time.sleep(2)

degi_music = pygame.mixer.Sound("degi.mp3")
degi_music.set_volume(0.2)
opening_music = pygame.mixer.Sound("opening.mp3")
opening_music.set_volume(0.2)
gaming_music = pygame.mixer.Sound("gaming.mp3")
gaming_music.set_volume(0.2)
opening_music.play()


def playmusic_gaming():
    while True:
        gaming_music.play()
        time.sleep(6 * 60 + 5)


gaming_music_thread = threading.Thread(target=playmusic_gaming)
gaming_music_thread.start()
gaming_music.set_volume(0)


def playmusic_degi():
    while True:
        degi_music.play()
        time.sleep(3 * 60 + 27)


degi_music_thread = threading.Thread(target=playmusic_degi)
degi_music_thread.start()
degi_music.set_volume(0)

ind = 0
while ind < 605:
    try:
        screen.blit(opening[ind], (0, 0))
        pygame.display.update()
        clock.tick(FPS)
        ind += 1
    except:
        pass
opening_music.stop()


def gacha_charactercard():
    result = random.randint(1, 10)
    if result > 5:
        result = 0
    for i in range(170):
        screen.blit(gacha_loading[i], (0, 0))
        pygame.display.update()
        clock.tick(45)
    draw_text("클릭하여 카드 확인", size=30, color="#FFFFFF")
    pygame.display.update()
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
    for i in range(153):
        screen.blit(gacha_yonchool_char[result][i], (0, 0))
        pygame.display.update()
        clock.tick(45)
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
    return gacha, ()


def gacha():
    images_banner = pygame.transform.scale(pygame.image.load("./gacha/charactercard_gacha_banner.png"), SCREEN_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1300 < x < 1550 and 860 < y < 930:
                    return gacha_charactercard, ()
                if 70 < x < 240 and 40 < y < 110:
                    return main, ()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return main, ()
        screen.blit(images_banner, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def end(*_):
    pygame.quit()
    sys.exit()


def main(*_):
    background = pygame.image.load("main_background.png")
    screen.blit(background, (0, 0))
    gaming_music.set_volume(0)
    degi_music.set_volume(0.2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 706 < x < 1216 and 392 < y < 505:
                    return select_stage, ()
                if 706 < x < 1216 and 537 < y < 651:
                    return dogam, ()
                if 706 < x < 1216 and 684 < y < 800:
                    return forming, ()
                if 706 < x < 1216 and 829 < y < 943 and not loadgacha.is_alive():
                    return gacha, ()
                if 1768 < x < 1892 and 1024 < y < 1059:
                    return end, ()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return end, ()


def select_stage(stage=0):
    star_img = pygame.transform.scale(pygame.image.load("star.png"), (100, 100))
    emptystar_img = pygame.transform.scale(pygame.image.load("emptystar.png"), (100, 100))
    record = []
    with open("record.csv", "r") as file:
        for line in csv.reader(file):
            record = list(map(int, line))
            break
    stage_num = stage
    bg = pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % 11}.png"), SCREEN_SIZE)
    while True:
        screen.blit(bg, (0, 0))
        # screen.blit(
        #     pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % (len(stage_list) + 1)}.png"),
        #                            (600, 600)),
        #     (SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT / 2 - 300))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    stage_num -= 1 if stage_num >= 0 else 0
                    bg = pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % 11}.png"),
                                                SCREEN_SIZE)
                if event.key == pygame.K_RIGHT:
                    stage_num += 1 if stage_num < len(stage_list) else 0
                    bg = pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % 11}.png"),
                                                SCREEN_SIZE)
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    return main, ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 340 < x < 1580 and 335 < y < 716:
                    return select_character, (stage_num,)
                if 1784 < x < 1851 and 486 < y < 582:
                    stage_num += 1 if stage_num < len(stage_list) - 1 else 0
                    bg = pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % 11}.png"),
                                                SCREEN_SIZE)
                if 67 < x < 144 and 486 < y < 582:
                    stage_num -= 1 if stage_num >= 1 else 0
                    bg = pygame.transform.scale(pygame.image.load(f"./stage_img/{(stage_num + 1) % 11}.png"),
                                                SCREEN_SIZE)
                if 72 < x < 283 and 50 < y < 105:
                    return main, ()
        motion_draw.draw(screen)
        try:
            star = record[stage_num]
            emptystar = 3 - star
            for i in range(star):
                screen.blit(star_img, (SCREEN_WIDTH / 2 + (i - 1) * 200 - 50, 100))
            for i in range(emptystar):
                screen.blit(emptystar_img, (SCREEN_WIDTH / 2 + (-i + 1) * 200 - 50, 100))
        except:
            pass
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
    background = pygame.transform.scale(pygame.image.load("before_game.png"), SCREEN_SIZE)
    game_board = SelectCharacter(stage_num, screen)
    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_board.click(event.pos)
                x, y = event.pos
                if 1460 < x < 1790 and 800 < y < 970:
                    if len(game_board.result) != 0:
                        return game, (game_board.result, stage_list[stage_num], e_card_list, stage_num)
                if 1850 < x < 1900 and 1000 < y < 1060:
                    return select_stage, (stage_num,)
        game_board.draw()
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def forming():
    global e_cards, e_card_list
    screen.fill("#333333")
    cards = e_cards
    images = [pygame.transform.scale(pygame.image.load(img_path), (200, 300))
              for _, _, img_path, _, _ in event_card_info.values()]
    bg = pygame.image.load("pyonsoung_bg.png")
    while True:
        screen.blit(bg, (0, 0))
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


def draw_skill(skill, index, char=False):
    a, b = (200, 0) if char else (170, 100)
    background = pygame.Surface(((SKILL_WIDTH + 20) * 4 - 20, SKILL_HEIGHT))
    background.fill("#000000")
    bg_rect = background.get_rect(
        center=(
            SCREEN_WIDTH / 2 + 30 - SKILL_WIDTH / 2 + (SKILL_WIDTH + 20) * 2 - 100,
            SCREEN_HEIGHT - 100 - 600 + index * a - b))
    screen.blit(background, bg_rect)

    font = pygame.font.Font("./D2Coding.ttf", 26)
    text = font.render(skill.name, True, "#FFFFFF")
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2 + 40 - 100, SCREEN_HEIGHT - 50 - 600 + index * a - b))
    screen.blit(text, text_rect)

    image = pygame.image.load(skill.skill_image_path)
    image = pygame.transform.scale(image, (80, 80))
    pos = (SCREEN_WIDTH / 2 + 40 - 40 - 100, SCREEN_HEIGHT - 60 - 35 - 60 - 600 + index * a - b)
    screen.blit(image, pos)

    center_pos = (SCREEN_WIDTH / 2 + 40 + 40 - 100, SCREEN_HEIGHT - 60 - 35 - 60 - 600 + index * a - b)
    pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
    draw_text(str(skill.cost), center=center_pos, color="#FFFFFF", size=16)
    try:
        if skill.max_energy is not None:
            center_pos = (SCREEN_WIDTH / 2 + 40 + 40 - 100, SCREEN_HEIGHT - 60 - 35 - 60 + 20 - 600 + index * a - b)
            pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
            draw_text(str(skill.max_energy), center=center_pos, color="#FFFFFF", size=16)
    except:
        pass

    i = 0
    for t in skill.explaination:
        font = pygame.font.Font("./D2Coding.ttf", 14)
        text = font.render(t, True, "#FFFFFF")
        text_rect = text.get_rect(centery=SCREEN_HEIGHT - 150 + i * 19 - 600 + index * a - b,
                                  left=SCREEN_WIDTH / 2 + 40)
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
                    return dogam_character_index, (4,)
                if 662 < x < 955 and 144 < y < 1015:
                    return dogam_character_index, (1,)
                if 964 < x < 1257 and 144 < y < 1015:
                    return dogam_character_index, (2,)
                if 1265 < x < 1558 and 144 < y < 1015:
                    return dogam_character_index, (3,)
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
        draw_skill(skills[0](None), 0, char=True)
        draw_skill(skills[1](None), 1, char=True)
        draw_skill(specialskill(None), 2, char=True)
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def dogam_enemy(*_):
    bg_img = pygame.image.load(f"./dogam_enemy.png")
    index = 0
    while True:
        screen.blit(bg_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1848 < x < 1900 and 470 < y < 540:
                    index = min(len(enemies_info) - 1, index + 1)
                if 20 < x < 74 and 470 < y < 540:
                    index = max(0, index - 1)
                if 25 < x < 100 and 20 < y < 70:
                    return dogam, ()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index = min(len(enemies_info) - 1, index + 1)
                if event.key == pygame.K_LEFT:
                    index = max(0, index - 1)
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
    background = pygame.transform.scale(pygame.image.load("dogam_event.png"), SCREEN_SIZE)
    screen.blit(background, (0, 0))
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 60 < x < 180 and 20 < y < 70:
                    return dogam, ()
        clock.tick(FPS)


def dogam():
    background = pygame.transform.scale(pygame.image.load("dogambg.png"), SCREEN_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 500 < event.pos[0] < 1340 and 178 < event.pos[1] < 400:
                    return dogam_character, ()
                if 500 < event.pos[0] < 1340 and 430 < event.pos[1] < 650:
                    return dogam_enemy, ()
                if 500 < event.pos[0] < 1340 and 678 < event.pos[1] < 900:
                    return dogam_eventcard, ()
                if 67 < event.pos[0] < 240 and 40 < event.pos[1] < 114:
                    return main, ()
        screen.blit(background, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


ending_img = []


def load_ending():
    for i in range(292):
        ending_img.append(pygame.image.load(f"./ending/{i}.png"))


threading.Thread(target=load_ending).start()


def ending():
    opening_music.play()
    for i in range(292):
        screen.blit(ending_img[i], (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return main, ()


def game_end(win, stage_num, turn):
    screen.fill("#000000")
    star = 1 if win else 0
    if turn <= 6:
        star *= 3
    elif turn <= 10:
        star *= 2
    now = []
    with open("record.csv", "r") as file:
        for line in csv.reader(file):
            now = list(map(int, line))
            break
    before = now[stage_num]
    now[stage_num] = max(star, now[stage_num])
    with open("record.csv", "w", newline='') as file:
        csv.writer(file).writerow(now)
    if stage_num == 9 and star == 3 and before != 3:
        return ending, ()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return main, ()
        if win:
            screen.blit(pygame.image.load(f"win_{star}star.png"), (0, 0))
        else:
            screen.blit(pygame.image.load("lose.png"), (0, 0))
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


def game(p_info, e_info, eventcard_list, stage_num):
    game_board = GameMap(screen, eventcard_list)
    bg = pygame.image.load("background.png")
    gaming_music.set_volume(0.2)
    degi_music.set_volume(0)
    bg = pygame.transform.scale(bg, (1920, 1080))
    for num, pos in p_info:
        game_board.add_character(characters_info[num], pos)
    for num, pos in e_info:
        game_board.add_enemy(enemies_info[num], pos)
    ai_enemy_index = 0
    exit_game = False
    while True:
        if exit_game:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 824 < x < 922 and 542 < y < 590:
                        motion_draw.clear()
                        return main, ()
                    if 1000 < x < 1100 and 542 < y < 590:
                        exit_game = False
            clock.tick(FPS)
            continue
        if len(game_board.players) == 0 and not motion_draw.motion_playing():
            return game_end, (False, stage_num, game_board.turn_count)
        if len(game_board.enemys) == 0 and not motion_draw.motion_playing():
            return game_end, (True, stage_num, game_board.turn_count)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1840 < x < 1900 and 1000 < y < 1060:
                    exit_game = True
                    img = pygame.image.load("pause.png")
                    x, y = img.get_size()
                    screen.blit(img, ((SCREEN_WIDTH - x) / 2, (SCREEN_HEIGHT - y) / 2))
                    pygame.display.update()
                    clock.tick(FPS)
                elif game_board.turn != 4:
                    game_board.click(event.pos)
        if exit_game:
            continue
        screen.blit(bg, (-1, -1))
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
