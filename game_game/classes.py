from game_objects.classes import *
from game_players.classes import *

class Game:
    def __init__(self, size):
        self.size = size

        user_field = self.random_board()
        ai_field = self.random_board()
        ai_field.hid = True

        self.ai = AI(ai_field, user_field)
        self.user = User(user_field, ai_field)

    def try_board(self):
        lens = [1, 1, 1, 1, 2, 2, 3]
        board = Board()
        attempts = 0

        for ln in lens:
            while True:
                attempts += 1
                if attempts > 4000:
                    return None
                ship = Ship(ln, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print(' ---------------------------')
        print('     Приветствуем вас       ')
        print('          в игре            ')
        print('        морской бой         ')
        print(' ---------------------------')
        print('     формат ввода: x y      ')
        print('     x - номер строки       ')
        print('     y - номер столбца      ')
        print(' ---------------------------')

    def boards_output(self):
        print(' ---------------------------')
        print('      Ваша доска:           ')
        print(self.user.board)
        print(' ---------------------------')
        print('      Доска компьютера:     ')
        print(self.ai.board)
        print(' ---------------------------')

    def loop(self):
        num = 0
        while True:
            self.boards_output()
            if num % 2 == 0:
                print('Вы ходите! ')
                repeat = self.user.move()
            else:
                print('Ходит компьютер! ')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.check():
                #self.boards_output()
                print(' ---------------------------')
                print('      Вы выиграли!:         ')
                break

            if self.user.board.check():
                #self.boards_output()
                print(' ---------------------------')
                print('      Компьютер выиграл!:         ')
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()