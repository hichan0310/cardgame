import pygame
from cell import Cell
from settings import *
from characters import *
from playerCard import PlayerCard


class Playercard_preview(pygame.sprite.Sprite):
    def __init__(self, pos_center, group, pos_gameboard, image_path):
        super().__init__(group)
        self.pos_center = pos_center
        self.pos_gameboard = pos_gameboard
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, CARD_SIZE)
        self.rect = self.image.get_rect(center=pos_center)
        self.using = False

    def draw_using(self, screen):
        if self.using:
            image = pygame.image.load("using.png")
            image = pygame.transform.scale(image, CARD_SIZE)
            image.set_alpha(180)
            screen.blit(image, (self.pos_center[0] - CARD_WIDTH / 2, self.pos_center[1] - CARD_HEIGHT / 2))


class SelectCharacter:
    def __init__(self, stage_num, screen):
        self.group = pygame.sprite.Group()
        self.gameBoard: list[list[Cell]] = [[Cell(
            (30 - CELL_WIDTH / 2 + (CARD_WIDTH + 30) * i, 30 - CELL_HEIGHT / 2 - 35 + (CELL_HEIGHT + 10) * j),
            not (i == 0 or i == 6 or j == 0 or j == 6), self, self.group, (j, i))
            for i in range(7)] for j in range(7)]
        self.characters = [
            Playercard_preview((30 - CELL_WIDTH / 2 + (CARD_WIDTH + 8) * (i % 7) + SCREEN_WIDTH / 2,
                                30 - CELL_HEIGHT / 2 - 35 + (CELL_HEIGHT + 8) * (i // 7 + 1)),
                               self.group, (i // 7, i % 7), characters_info[i][6]) for i in range(len(characters_info))]
        self.stage = stage_num
        self.screen = screen
        for enemy_num, location in stage_list[stage_num]:
            name, skills, hp, passive, ai, img_path = enemies_info[enemy_num]
            self.change_image(location, img_path)
            self.gameBoard[location[0]][location[1]].team = FLAG_ENEMY_TEAM
        self.result = []
        self.selected_char = None

    def change_image(self, location, img_path):
        x, y = location
        self.gameBoard[x][y].image = pygame.transform.scale(pygame.image.load(img_path), CARD_SIZE)
        self.gameBoard[x][y].mask = pygame.mask.from_surface(self.gameBoard[x][y].image)

    def reset_image(self, location):
        x, y = location
        self.gameBoard[x][y].image = pygame.Surface(CARD_SIZE)
        self.gameBoard[x][y].image.fill("#000000")
        self.gameBoard[x][y].mask = pygame.mask.from_surface(self.gameBoard[x][y].image)

    def draw(self):
        if self.selected_char is not None:
            x, y = self.characters[self.selected_char].pos_center
            pygame.draw.rect(self.screen, "#777777",
                             [x - (CELL_WIDTH - 20) / 2, y - (CELL_HEIGHT-10) / 2, CELL_WIDTH - 20, CELL_HEIGHT-10])
        self.group.draw(self.screen)
        for playable in self.characters:
            playable.draw_using(self.screen)

    def click(self, pos):
        for i in range(1, 6):
            for j in range(1, 6):
                if (pos[0] - CARD_WIDTH / 2 < self.gameBoard[i][j].pos_center[0] < pos[0] + CARD_WIDTH / 2
                        and pos[1] - CARD_HEIGHT / 2 < self.gameBoard[i][j].pos_center[1] < pos[
                            1] + CARD_HEIGHT / 2):
                    if self.gameBoard[i][j].team == FLAG_PLAYER_TEAM:
                        self.reset_image((i, j))
                        for num, location in self.result:
                            if location == (i, j):
                                self.result.remove((num, location))
                                self.characters[num].using = False
                                self.gameBoard[i][j].team = FLAG_EMPTY
                    if self.selected_char is not None and self.gameBoard[i][j].team == FLAG_EMPTY and len(
                            self.result) < 4:
                        self.change_image((i, j), characters_info[self.selected_char][-2])
                        self.result.append((self.selected_char, (i, j)))
                        self.characters[self.selected_char].using = True
                        self.gameBoard[i][j].team = FLAG_PLAYER_TEAM
                    self.selected_char = None
        for i in range(len(self.characters)):
            if (pos[0] - CARD_WIDTH / 2 < self.characters[i].pos_center[0] < pos[0] + CARD_WIDTH / 2
                    and pos[1] - CARD_HEIGHT / 2 < self.characters[i].pos_center[1] < pos[
                        1] + CARD_HEIGHT / 2):
                if not self.characters[i].using:
                    self.selected_char = i
