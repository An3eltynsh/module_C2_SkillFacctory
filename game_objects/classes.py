from game_exceptions.exception import *

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

class Ship:
    def __init__(self, length, bow, direct):
        self.length = length
        self.bow = bow
        self.direct = direct
        self.hp = length
    # direct: 0 - горизонтально, 1 - вертикально
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            dot_x = self.bow.x
            dot_y = self.bow.y

            if self.direct == 0:
                dot_x += i
            elif self.direct == 1:
                dot_y += i
            ship_dots.append(Dot(dot_x, dot_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size

        self.count = 0 # подстрелянные корабли
        self.field = [['O' for i in range(size)] for j in range(size)]
        self.ships = []
        self.busy = []

    def __str__(self):
        res = ''
        res += '   | 1 | 2 | 3 | 4 | 5 | 6 |'
        res += '\n ---------------------------'
        for i, item in enumerate(self.field):
            res += f'\n {i + 1} | {" | ".join(item)} |'
            res += '\n ---------------------------'

        if self.hid:
            res = res.replace('\u25A0', 'O') # ■
        return res

    def out_of_field(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contr(self, ship, flag = False):
        delt_dot = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for delt_x, delt_y in delt_dot:
                cont = Dot(dot.x + delt_x, dot.y + delt_y)
                if not(self.out_of_field(cont)) and cont not in self.busy:
                    if flag:
                        self.field[cont.x][cont.y] = '.'
                    self.busy.append(cont)

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out_of_field(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = '\u25A0' # ■
            self.busy.append(dot)
        self.ships.append(ship)
        self.contr(ship)

    def shoot(self, dot):
        if self.out_of_field(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if ship.shooten(dot):
                ship.hp -= 1
                self.field[dot.x][dot.y] = '\u26DD' # ⛝
                if ship.hp == 0:
                    self.count += 1
                    for dot in ship.dots: self.field[dot.x][dot.y] = '\u2020' # †
                    self.contr(ship, True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True

        self.field[dot.x][dot.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []
    def check(self):
        return self.count == len(self.ships)