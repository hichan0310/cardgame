import pygame
from eventCard import EventCard
from settings import *

class Potal(EventCard):
    def __init__(self, pos_center, game_board, group):
        super().__init__(pos_center, "./EventCards/Potal/potal_card.png", EVENT_TYPE_2, game_board, group)

    def click_two(self, pos1, pos2):
        pass