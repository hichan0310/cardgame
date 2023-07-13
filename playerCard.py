import pygame.image

from skill import Skill
from character import characters_info
from buff import Buff
from copy import deepcopy
from cell import Cell
from settings import *


class PlayerCard(Cell):
    def __init__(self, character_num: int, pos: tuple[int, int], game_board, group):
        super().__init__(pos, True, game_board, group)
        self.skills: list[Skill]
        self.hp: int
        self.max_energy: int
        self.buff: list[Buff]=[]
        self.name, self.skills, self.max_hp, self.max_energy, self.img_path = deepcopy(characters_info[character_num])
        self.skills=[]+self.skills
        if self.img_path!=None:
            self.image=pygame.image.load(self.img_path)
            self.image=pygame.transform.scale(self.image, CARD_SIZE)
        self.hp = self.max_hp
        self.__observers_hit: list[Buff] = []
        self.__observers_attack: list[Buff] = []
        self.__observers_die: list[Buff] = []
        self.__observers_move: list[Buff] = []
        self.shield = 0

    def register_hit(self, observer: Buff):
        self.__observers_hit.append(observer)
        observer.observing(self.__observers_hit)

    def register_attack(self, observer: Buff):
        self.__observers_attack.append(observer)
        observer.observing(self.__observers_attack)

    def register_die(self, observer: Buff):
        self.__observers_die.append(observer)
        observer.observing(self.__observers_die)

    def hit(self, damage, caster, atk_type):
        for b in self.buff:
            damage = b.hit_buff(caster, self, damage, atk_type)
        self.hp -= damage
        if self.hp <= 0:
            self.die()
        for observer in self.__observers_hit:
            observer.hit_event(caster, self, self.game_board)

    def attack(self, damage, target, atk_type):
        for b in self.buff:
            damage = b.atk_buff(self, target, damage, atk_type)
        target.hit(damage, self, 'normal')
        for observer in self.__observers_attack:
            observer.attack_event(self, target, self.game_board)

    def die(self):
        for observer in self.__observers_die:
            observer.die_event(self, self.game_board)

    def heal(self, heal_amount):
        self.hp = min(self.max_hp, self.hp + heal_amount)

    def click(self):
        pass