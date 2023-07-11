from cell import Cell
from buff import Buff


class GameMap:
    def __init__(self):
        self.gameBoard: list[list[Cell]] = [
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()],
            [Cell(), Cell(), Cell(), Cell(), Cell(), Cell(), Cell()]
        ]
        self.__observers_turnover: list[Buff] = []
        self.__observers_move: list[Buff] = []
        self.__observers_turnstart: list[Buff] = []
        self.cost = 0

    def addItem(self, item, pos):
        self.gameBoard[pos[0]][pos[1]].item = item

    def register_turnover(self, observer):
        self.__observers_turnover.append(observer)

    def register_turnstart(self, observer):
        self.__observers_turnstart.append(observer)

    def register_

    def turnover(self):
        for observer in self.__observers_turnover:
            observer.turnover_event()

    def heal(self, pos, heal_amount):
        self.gameBoard[pos[0]][pos[1]].heal(heal_amount)
