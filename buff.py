import pygame.draw
from settings import *


class EventTag:
    def __init__(self, name):
        self.name=name
class HitEvent(EventTag):
    def __init__(self, caster, target, damage, tag):
        super(HitEvent, self).__init__("hit")
        self.caster=caster
        self.target=target
        self.damage=damage
        self.tag=tag
class AtkEvent(EventTag):
    def __init__(self, caster, target, damage, tag):
        super(AtkEvent, self).__init__("attack")
        self.caster=caster
        self.target=target
        self.damage=damage
        self.tag=tag
class TurnoverEvent(EventTag):
    def __init__(self):
        super(TurnoverEvent, self).__init__("turnover")

class Buff:
    def __init__(self, character, use_num, game_board, name, img_path):
        self.image_path = img_path
        self.name = name
        self.game_board = game_board
        character.buff.append(self)
        self.target = character
        self.use_num = use_num
        self.observing_list = []

    def draw(self, centerpos, screen):
        pygame.draw.rect(screen, "#000000",
                         [centerpos[0] - BUFF_WIDTH / 2, centerpos[1] - BUFF_HEIGHT / 2-20, BUFF_WIDTH, BUFF_HEIGHT])
        image = pygame.image.load(self.image_path)
        image = pygame.transform.scale(image, (80, 80))
        pos = (centerpos[0] - 40, centerpos[1] - 40 - 30)
        screen.blit(image, pos)

        pygame.draw.circle(screen, "#000000", (pos[0]+80, pos[1]), 10, 10)
        draw_text(str(self.use_num), center=(pos[0]+80, pos[1]), color="#FFFFFF", size=16)

        font = pygame.font.Font("./D2Coding.ttf", 14)
        text = font.render(self.name, True, "#FFFFFF")
        text_rect = text.get_rect(center=(centerpos[0], centerpos[1] + 20))
        screen.blit(text, text_rect)

    def event(self, event_tag:list[EventTag]):
        pass

    def observing(self, observed_event):
        self.observing_list.append(observed_event)

    def atk_buff(self, caster, target, damage: int, atk_type):
        return damage

    def hit_buff(self, caster, target, damage: int, atk_type):
        return damage

    def hit_event(self, caster, target, game_board, atk_type, damage):
        pass

    def attack_event(self, caster, targets, game_board, atk_type):
        pass

    def die_event(self, player, game_board):
        pass

    def move_event(self, player, pos: tuple[int, int], game_board):
        pass

    def turnover_event(self, game_board):
        pass

    def turnstart_event(self, game_board):
        pass

    def curse_event(self, caster, target, game_board):
        pass

    def used(self, num):
        self.use_num -= num
        if self.use_num == 0:
            self.remove()

    def remove(self):
        self.target.buff.remove(self)
        for events in self.observing_list:
            events.remove(self)
