from playerCard import PlayerCard
from main import game_board


class Buff:
    def __init__(self, character: PlayerCard, use_num):
        character.buff.append(self)
        self.target = character
        self.use_num = use_num
        self.observing_list=[]

    def observing(self, observed_event):
        self.observing_list.append(observed_event)

    def atk_buff(self, caster: PlayerCard, target: PlayerCard, damage: int, atk_type: str):
        return damage

    def hit_buff(self, caster: PlayerCard, target: PlayerCard, damage: int, atk_type: str):
        return damage

    def hit_event(self, caster:PlayerCard): pass
    def attack_event(self, target:PlayerCard): pass
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
        for events in self.observing_list:
            events.remove(self)


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
    def __init__(self, target:PlayerCard):
        super().__init__(target, -1)
        self.stack=0

    def add_Curse(self, num):
        self.stack+=num
        if self.stack>=5:
            self.stack -= 5
            self.target.hp -= 4
            if self.target.hp<=0:
                self.target.die()