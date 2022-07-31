class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == int:
            return Point(self.x * other, self.y * other)
        return Point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if type(other) == int:
            return Point(self.x / other, self.y / other)
        return Point(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        if type(other) == int:
            return Point(self.x // other, self.y // other)
        return Point(self.x // other.x, self.y // other.y)
