from game_objects.classes import *
from game_exceptions.exception import BoardException
from random import randint

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {dot.x+1} {dot.y+1}')
        return dot

class User(Player):
    def ask(self):
        while True:
            move = input('Ваш ход: ').split()

            if len(move) != 2:
                print('Введите 2 координаты! ')
                continue
            x, y = move

            if not(x.isdigit()) or not(y.isdigit()):
                print('Введите числа! ')
                continue
            x, y = int(x), int(y)

            if self.board.out_of_field(Dot(x-1, y-1)):
                print('Вы вышли за поле! ')
                continue

            return Dot(x-1, y-1)