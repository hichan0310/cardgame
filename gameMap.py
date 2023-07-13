from cell import Cell
from buff import Buff
from settings import *
import pygame
from playerCard import PlayerCard


class CostBar(pygame.sprite.Sprite):
    def __init__(self, group, cost: int):
        super().__init__(group)
        self.cost: int = cost
        self.image = pygame.Surface((40, (SCREEN_HEIGHT - 100) * min(self.cost, 10) / 10))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(centerx=830, bottom=SCREEN_HEIGHT - 15)
        self.selected_card = None

    def plus(self, value: int):
        self.cost += value
        self.image = pygame.Surface((40, (SCREEN_HEIGHT - 100) * min(self.cost, 10) / 10))
        self.rect = self.image.get_rect(centerx=830, bottom=SCREEN_HEIGHT - 15)
        self.image.fill((100, 100, 100))

    def minus(self, value: int):
        self.cost -= value
        self.image = pygame.Surface((40, (SCREEN_HEIGHT - 100) * min(self.cost, 10) / 10))
        self.rect = self.image.get_rect(centerx=830, bottom=SCREEN_HEIGHT - 15)
        self.image.fill((100, 100, 100))


class SkillExplaination(pygame.sprite.Sprite):
    def __init__(self, skill, skill_index, group, pos_center):
        super().__init__(group)
        self.pos_center = pos_center
        self.image = pygame.Surface(SKILL_SIZE)
        self.image.fill("#000000")
        self.rect = self.image.get_rect(center=pos_center)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = skill.name
        self.explaination = skill.explaination
        self.img_path = skill.skill_image_path
        self.skill_index = skill_index

    def draw(self, screen):
        font = pygame.font.Font("./D2Coding.ttf", 24)
        text = font.render(self.name, True, "#FFFFFF")
        text_rect = text.get_rect(center=(self.pos_center[0], self.pos_center[1] + 40))
        screen.blit(text, text_rect)

        image = pygame.image.load(self.img_path)
        image = pygame.transform.scale(image, (70, 70))
        pos = (self.pos_center[0] - 35, self.pos_center[1] - 35 - 35)
        screen.blit(image, pos)


class SkillMoreExplaination:
    def __init__(self, skill):
        self.image_path = skill.skill_image_path
        self.name = skill.name
        self.explaination = skill.explaination

    def draw(self, screen):
        background = pygame.Surface(((SKILL_WIDTH + 20) * 4 - 20, SKILL_HEIGHT))
        background.fill("#000000")
        bg_rect = background.get_rect(
            center=(SCREEN_WIDTH / 2 + 30 - SKILL_WIDTH / 2 + (SKILL_WIDTH + 20) * 2, SCREEN_HEIGHT - 100))
        screen.blit(background, bg_rect)

        font = pygame.font.Font("./D2Coding.ttf", 26)
        text = font.render(self.name, True, "#FFFFFF")
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT - 50))
        screen.blit(text, text_rect)

        image = pygame.image.load(self.image_path)
        image = pygame.transform.scale(image, (80, 80))
        pos = (SCREEN_WIDTH/2 + 40 - 40, SCREEN_HEIGHT - 60 - 35 - 60)
        screen.blit(image, pos)


class SkillSelectBar:
    def __init__(self, skills):
        self.group = pygame.sprite.Group()
        self.skills = skills
        self.skill_sprites = []
        for i in range(len(skills)):
            self.skill_sprites.append(SkillExplaination(
                skills[i], i, self.group,
                (i * (SKILL_WIDTH + 20) + SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT * 5 / 7))
            )
        self.explainationbar = None

    def draw(self, screen):
        for sprite in self.skill_sprites:
            sprite.draw(screen)
        if self.explainationbar is not None:
            self.explainationbar.draw(screen)


class GameMap:
    def __init__(self, screen):
        self.screen = screen
        self.group = pygame.sprite.Group()
        self.gameBoard: list[list[Cell]] = [[Cell(
            (30 - CELL_WIDTH / 2 + (CARD_WIDTH + 30) * i, 30 - CELL_HEIGHT / 2 - 35 + (CELL_HEIGHT + 10) * j),
            not (i == 0 or i == 6 or j == 0 or j == 6), self, self.group)
            for i in range(7)] for j in range(7)]
        self.__observers_turnover: list[Buff] = []
        self.__observers_move: list[Buff] = []
        self.__observers_turnstart: list[Buff] = []
        self.cost = CostBar(self.group, 10)
        self.selected_card = None
        self.skill_select = SkillSelectBar([])
        self.selected_skill = None

    def addItem(self, item, pos):
        self.gameBoard[pos[0]][pos[1]].item = item

    def register_turnover(self, observer):
        self.__observers_turnover.append(observer)

    def register_turnstart(self, observer):
        self.__observers_turnstart.append(observer)

    def register_move(self, observer):
        self.__observers_move.append(observer)

    def turnover(self):
        for observer in self.__observers_turnover:
            observer.turnover_event(self)

    def move_card(self, pos1, pos2):
        self.gameBoard[pos1[0]][pos1[1]], self.gameBoard[pos2[0]][pos2[1]] = (
            self.gameBoard[pos2[0]][pos2[1]],
            self.gameBoard[pos1[0]][pos1[1]]
        )
        self.gameBoard[pos1[0]][pos1[1]].pos_center, self.gameBoard[pos2[0]][pos2[1]].pos_center = (
            self.gameBoard[pos2[0]][pos2[1]].pos_center,
            self.gameBoard[pos1[0]][pos1[1]].pos_center
        )
        self.cost.minus(1)
        self.gameBoard[pos1[0]][pos1[1]].update_location()
        self.gameBoard[pos2[0]][pos2[1]].update_location()

    def heal(self, pos, heal_amount):
        self.gameBoard[pos[0]][pos[1]].heal(heal_amount)

    def add_character(self, character_num, pos):
        self.gameBoard[pos[0]][pos[1]] = PlayerCard(
            character_num,
            self.gameBoard[pos[0]][pos[1]].pos_center,
            self,
            self.group
        )

    def draw(self):
        self.group.draw(self.screen)
        self.skill_select.group.draw(self.screen)
        self.skill_select.draw(self.screen)

    def click(self, pos):
        if self.selected_card == None:
            for i in range(1, 6):
                for j in range(1, 6):
                    if (pos[0] - CARD_WIDTH / 2 < self.gameBoard[i][j].pos_center[0] < pos[0] + CARD_WIDTH / 2
                            and pos[1] - CARD_HEIGHT / 2 < self.gameBoard[i][j].pos_center[1] < pos[
                                1] + CARD_HEIGHT / 2):
                        self.gameBoard[i][j].click()
                        self.selected_card = (i, j)
                        try:
                            self.skill_select = SkillSelectBar(self.gameBoard[i][j].skills)
                        except:
                            self.skill_select = SkillSelectBar([])
                            self.selected_card = None
        else:
            for i in range(1, 6):
                for j in range(1, 6):
                    if (pos[0] - CARD_WIDTH / 2 < self.gameBoard[i][j].pos_center[0] < pos[0] + CARD_WIDTH / 2
                            and pos[1] - CARD_HEIGHT / 2 < self.gameBoard[i][j].pos_center[1] < pos[
                                1] + CARD_HEIGHT / 2):
                        if self.selected_card in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                            self.move_card((i, j), self.selected_card)
                            self.skill_select = SkillSelectBar([])
                            self.selected_card = None
                            return
                        self.skill_select = SkillSelectBar([])
                        self.selected_card = None
                        return
            for i in range(len(self.skill_select.skills)):
                p = self.skill_select.skill_sprites[i].pos_center
                if p[0] - SKILL_WIDTH / 2 < pos[0] < p[0] + SKILL_WIDTH / 2 and p[1] - SKILL_HEIGHT / 2 < pos[1] < p[
                    1] + SKILL_HEIGHT / 2:
                    self.skill_select.explainationbar = SkillMoreExplaination(self.skill_select.skills[i])
                    self.selected_skill = self.skill_select.skills[i]
                    return
            if self.selected_skill is None:
                self.skill_select = SkillSelectBar([])
                self.selected_card = None
                return
            self.selected_skill = None
            self.skill_select.explainationbar = None
