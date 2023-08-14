import pygame
import time
from gameMap import GameMap
from select_character import SelectCharacter
from settings import *
import sys
from graphic_manager import motion_draw

from EventCards.BombThrowing.bomb_throwing import BombThrowing
from EventCards.EnergyRecharge.energy_recharge import EnergyRecharge
from EventCards.EnforceHit.enforce_hit import EnforceHit
from EventCards.FireSward.fire_sward import FireSward
from EventCards.HealingLight.healing_light import HealingLight
from EventCards.Lucky.lucky import Lucky
from EventCards.ManaSynthesizer.mana_synthesizer import ManaSynthesizer
from EventCards.SecondOpportunity.second_opertunity import SecondOpertunity
from EventCards.Sniping.sniping import Sniping
from EventCards.WarpGate.warp_gate import WarpGate

from characters import *

pygame.init()


def end(*_):
    pygame.quit()
    sys.exit()


def main(*_):
    screen.fill("#000000")
    img1 = pygame.image.load("main_fight.png")
    img2 = pygame.image.load("main_forming.png")
    img1 = pygame.transform.scale(img1, (500, 500))
    img2 = pygame.transform.scale(img2, (500, 500))
    screen.blit(img1, (SCREEN_WIDTH / 2 - 300 - 250, SCREEN_HEIGHT / 2 + 100 - 250))
    screen.blit(img2, (SCREEN_WIDTH / 2 + 300 - 250, SCREEN_HEIGHT / 2 + 100 - 250))
    draw_text("아주 멋진 게임 제목", size=100, center=(SCREEN_WIDTH / 2, 200))
    draw_text("뒤로 가기 : esc, backspace", size=50, center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150), color="#FFFFFF")
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_WIDTH / 2 - 300 - 250 < event.pos[
                    0] < SCREEN_WIDTH / 2 - 300 + 250 and SCREEN_HEIGHT / 2 + 100 - 250 < event.pos[
                    1] < SCREEN_HEIGHT / 2 + 100 + 250:
                    return select_stage, ()
                if SCREEN_WIDTH / 2 + 300 - 250 < event.pos[
                    0] < SCREEN_WIDTH / 2 + 300 + 250 and SCREEN_HEIGHT / 2 + 100 - 250 < event.pos[
                    1] < SCREEN_HEIGHT / 2 + 100 + 250:
                    return forming, ()
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
    WarpGate
]
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
    screen.fill("#000000")
    draw_text("아직 개발중임", center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), size=100, color="#FFFFFF")
    pygame.display.update()
    time.sleep(0.5)
    return main, ()


def draw_skill(skill, index):
    background = pygame.Surface(((SKILL_WIDTH + 20) * 4 - 20, SKILL_HEIGHT))
    background.fill("#000000")
    bg_rect = background.get_rect(
        center=(
        SCREEN_WIDTH / 2 + 30 - SKILL_WIDTH / 2 + (SKILL_WIDTH + 20) * 2-100, SCREEN_HEIGHT - 100 - 600 + index * 200))
    screen.blit(background, bg_rect)

    font = pygame.font.Font("./D2Coding.ttf", 26)
    text = font.render(skill.name, True, "#FFFFFF")
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2 + 40-100, SCREEN_HEIGHT - 50 - 600 + index * 200))
    screen.blit(text, text_rect)

    image = pygame.image.load(skill.skill_image_path)
    image = pygame.transform.scale(image, (80, 80))
    pos = (SCREEN_WIDTH / 2 + 40 - 40-100, SCREEN_HEIGHT - 60 - 35 - 60 - 600 + index * 200)
    screen.blit(image, pos)

    center_pos = (SCREEN_WIDTH / 2 + 40 + 40-100, SCREEN_HEIGHT - 60 - 35 - 60 - 600 + index * 200)
    pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
    draw_text(str(skill.cost), center=center_pos, color="#FFFFFF", size=16)
    try:
        if skill.max_energy is not None:
            center_pos = (SCREEN_WIDTH / 2 + 40 + 40-100, SCREEN_HEIGHT - 60 - 35 - 60 + 20 - 600 + index * 200)
            pygame.draw.circle(screen, "#000000", center_pos, 12, 12)
            draw_text(str(skill.max_energy), center=center_pos, color="#FFFFFF", size=16)
    except:
        pass

    i = 0
    for t in skill.explaination:
        font = pygame.font.Font("./D2Coding.ttf", 14)
        text = font.render(t, True, "#FFFFFF")
        text_rect = text.get_rect(centery=SCREEN_HEIGHT - 150 + i * 19-600+index*200, left=SCREEN_WIDTH / 2 + 40)
        screen.blit(text, text_rect)
        i += 1


def dogam_character(*_):
    index=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    index=min(len(characters_info)-1, index+1)
                    screen.fill("#000000")
                if event.key==pygame.K_LEFT:
                    index=max(0, index-1)
                    screen.fill("#000000")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        return
        name, skills, specialskill, hp, energy, passive, img_path, color=characters_info[index]
        img=pygame.transform.scale(pygame.image.load(img_path), (600, 900))
        font = pygame.font.Font("./D2Coding.ttf", 60)
        text = font.render(name, True, "#FFFFFF")
        text_rect = text.get_rect(centery=200, left=900)
        screen.blit(text, text_rect)
        screen.blit(img, (100, 90))
        draw_skill(skills[0](None), 0)
        draw_skill(skills[1](None), 1)
        draw_skill(specialskill(None), 2)
        motion_draw.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

def dogam_enemy(*_):
    index=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    index=min(len(enemies_info)-1, index+1)
                    screen.fill("#000000")
                if event.key==pygame.K_LEFT:
                    index=max(0, index-1)
                    screen.fill("#000000")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        return
        name, skills, hp, passive, ai, img_path=enemies_info[index]
        img=pygame.transform.scale(pygame.image.load(img_path), (600, 900))
        font = pygame.font.Font("./D2Coding.ttf", 60)
        text = font.render(name, True, "#FFFFFF")
        text_rect = text.get_rect(centery=200, left=900)
        screen.blit(text, text_rect)
        screen.blit(img, (100, 90))
        for i in range(len(skills)):
            draw_skill(skills[i](None), i)
        motion_draw.draw(screen)
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


func = dogam_enemy

params = ()
while __name__ == "__main__":
    result = func(*params)
    func, params = result
