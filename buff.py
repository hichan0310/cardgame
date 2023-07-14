class Buff:
    def __init__(self, character, use_num, game_board, name):
        self.name=name
        self.game_board = game_board
        character.buff.append(self)
        self.target = character
        self.use_num = use_num
        self.observing_list = []

    def observing(self, observed_event):
        self.observing_list.append(observed_event)

    def atk_buff(self, caster, target, damage: int, atk_type: str):
        return damage

    def hit_buff(self, caster, target, damage: int, atk_type: str):
        return damage

    def hit_event(self, caster, target, game_board):
        pass

    def attack_event(self, caster, target, game_board):
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


# 재생 버프



