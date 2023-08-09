import pygame
import time
from gameMap import GameMap
from select_character import SelectCharacter
from settings import *
import sys
from graphic_manager import motion_draw
from characters import *

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
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
                        return game, (game_board.result, stage_list[stage_num])
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


def game(p_info, e_info):
    game_board = GameMap(screen)
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
        bg = pygame.image.load("background.png")
        bg = pygame.transform.scale(bg, (1920, 1080))
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
