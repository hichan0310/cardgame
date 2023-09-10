import pygame
import random
from settings import *


def gacha_eventcard():
    for i in range(74):
        screen.blit(images[i], (0, 0))
        pygame.display.update()
        clock.tick(FPS / 2)
    draw_text("화면을 클릭해주세요", center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100), size=30, color="#000000")
    pygame.display.update()
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
    for i in range(74, 281):
        screen.blit(images[i], (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    for img, pos in tmp_arr_char:
        screen.blit(img, pos)
        pygame.display.update()
        clock.tick(FPS)
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
    return gacha, ()
