import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

CELL_WIDTH = 150
CELL_HEIGHT = 200
CELL_SIZE = (CELL_WIDTH, CELL_HEIGHT)

CARD_WIDTH = 120
CARD_HEIGHT = 180
CARD_SIZE = (CARD_WIDTH, CARD_HEIGHT)

FPS = 60

SKILL_WIDTH = 200
SKILL_HEIGHT = 160
SKILL_SIZE = (SKILL_WIDTH, SKILL_HEIGHT)


# 게임판 위 위치를 실제 위치로 변환
def transform_pos(pos):
    j, i = pos
    return (30 - CELL_WIDTH / 2 + (CARD_WIDTH + 30) * i, 30 - CELL_HEIGHT / 2 - 35 + (CELL_HEIGHT + 10) * j)

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)

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


EVENT_TYPE_0 = "zero"
EVENT_TYPE_1 = "one"
EVENT_TYPE_2 = "two"



BUFF_WIDTH = 120
BUFF_HEIGHT = 160

FLAG_EMPTY = 0
FLAG_PLAYER_TEAM = 1
FLAG_ENEMY_TEAM = 2
FLAG_SUMMONS = 3

TAG_NORMAL_ATTACK = "normal attack"
TAG_SKILL = "skill"
TAG_SPECIAL_SKILL = "special skill"
TAG_PENETRATE = "penetrate hit"
TAG_HEAL = "heal"
TAG_SUMMON = "summon"
TAG_BUFF = "buff"
TAG_PYRO = "fire"
TAG_HYDRO = "water"
TAG_ELECTRIC = "electric"
TAG_ICE = "ice"
TAG_PLANT = "plant"
TAG_STONE = "stone"
TAG_DARK = "dark"

# colors={
#     TAG_HEAL:"#B4E179",
#     TAG_PYRO:""
# }
