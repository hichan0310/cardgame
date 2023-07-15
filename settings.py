import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1060
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

CELL_WIDTH = 150
CELL_HEIGHT = 200
CELL_SIZE = (CELL_WIDTH, CELL_HEIGHT)

CARD_WIDTH = 120
CARD_HEIGHT = 180
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

FPS = 30


SKILL_WIDTH = 200
SKILL_HEIGHT = 160
SKILL_SIZE = (SKILL_WIDTH, SKILL_HEIGHT)

# 게임판 위 위치를 실제 위치로 변환
def transform_pos(pos):
    j, i=pos
    return (30 - CELL_WIDTH / 2 + (CARD_WIDTH + 30) * i, 30 - CELL_HEIGHT / 2 - 35 + (CELL_HEIGHT + 10) * j)
