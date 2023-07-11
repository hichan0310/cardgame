import pygame
from skill import Skill
from character import characters_info
from buff import Buff
from copy import deepcopy
from main import game_board
from cell import Cell


class PlayerCard(Cell):
    def __init__(self, character_num: int, pos: tuple[int, int]):
        super().__init__()
        self.pos = pos
        self.skills: list[Skill]
        self.hp: int
        self.max_energy: int
        self.buff: list[Buff]
        self.skills, self.max_hp, self.max_energy, self.buff = deepcopy(characters_info[character_num])
        self.hp = self.max_hp
        self.__observers_hit: list[Buff] = []
        self.__observers_attack: list[Buff] = []
        self.__observers_die: list[Buff] = []
        self.__observers_move: list[Buff] = []
        self.shield = 0

    def register_hit(self, observer:Buff):
        self.__observers_hit.append(observer)
        observer.observing(self.__observers_hit)

    def register_attack(self, observer:Buff):
        self.__observers_attack.append(observer)
        observer.observing(self.__observers_attack)

    def register_die(self, observer:Buff):
        self.__observers_die.append(observer)
        observer.observing(self.__observers_die)

    def hit(self, damage):
        self.shield -= damage
        if self.shield < 0:
            self.hp += self.shield
            self.shield = 0
        if self.hp <= 0:
            self.die()
        for observer in self.__observers_hit:
            observer.hit_event()

    def attack(self, target):
        for observer in self.__observers_attack:
            observer.attack_event()

    def die(self):
        for observer in self.__observers_die:
            observer.die_event()

    def move(self, direction: tuple[int, int]):
        if game_board.move_card(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1])):
            for observer in self.__observers_move:
                observer.move_event()

    def heal(self, heal_amount):
        self.hp = min(self.max_hp, self.hp + heal_amount)
