from playerCard import PlayerCard
from main import game_board


class Buff:
    def __init__(self, character: PlayerCard, use_num):
        character.buff.append(self)
        self.target = character
        self.use_num = use_num
        self.observe_list=[]

    def atk_buff(self, caster: PlayerCard, target: PlayerCard, damage: int, type: int, element_type: int):
        return damage

    def hit_buff(self, caster: PlayerCard, target: PlayerCard, damage: int, type: int, element_type: int):
        return damage

    def hit_event(self): pass
    def attack_event(self): pass
    def die_event(self): pass
    def move_event(self): pass
    def turnover_event(self): pass
    def turnstart_event(self): pass

    def used(self, num):
        self.use_num -= num
        if self.use_num == 0:
            self.remove()

    def remove(self):
        self.target.buff.remove(self)
        for events


# 재생 버프
class Reincarnation(Buff):
    def __init__(self, character: PlayerCard, count: int):
        super().__init__(character, count)

    def move_event(self):
        x, y = self.target.pos
        game_board.heal((x + 1, y), 1)
        game_board.heal((x, y + 1), 1)
        game_board.heal((x - 1, y), 1)
        game_board.heal((x, y - 1), 1)
        self.used(1)

class Curse(Buff):
    def __init__(self):
        super().__init__(-1)
        self.stack=1

