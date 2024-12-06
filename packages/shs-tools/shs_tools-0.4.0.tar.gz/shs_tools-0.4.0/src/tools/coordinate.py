from __future__ import annotations
from enum import Enum
from math import gcd, sqrt, inf, atan2, degrees, isclose
from .math import round_half_up
from typing import Union, List, Iterable
from .tools import minmax


class DistanceAlgorithm(Enum):
    MANHATTAN = 0
    EUCLIDEAN = 1
    PYTHAGOREAN = 1
    CHEBYSHEV = 2
    CHESSBOARD = 2


class Coordinate(tuple):
    def __new__(cls, x: int | float, y: int | float, z: int | float | None = None):
        return tuple.__new__(cls, (x, y, z))

    @property
    def x(self) -> int | float:
        return self[0]

    @property
    def y(self) -> int | float:
        return self[1]

    @property
    def z(self) -> int | float:
        return self[2]

    def is3D(self) -> bool:
        return self[2] is not None

    def getDistanceTo(
        self,
        target: Coordinate | tuple,
        algorithm: DistanceAlgorithm = DistanceAlgorithm.EUCLIDEAN,
        includeDiagonals: bool = False,
    ) -> int | float:
        """
        Get distance to target Coordinate

        :param target:
        :param algorithm: Calculation Algorithm (s. DistanceAlgorithm)
        :param includeDiagonals: in Manhattan Mode specify if diagonal
                                 movements are allowed (counts as 1.4 in 2D, 1.7 in 3D)
        :return: Distance to Target
        """
        if algorithm == DistanceAlgorithm.EUCLIDEAN:
            if self[2] is None:
                return sqrt(abs(self[0] - target[0]) ** 2 + abs(self[1] - target[1]) ** 2)
            else:
                return sqrt(
                    abs(self[0] - target[0]) ** 2 + abs(self[1] - target[1]) ** 2 + abs(self[2] - target[2]) ** 2
                )
        elif algorithm == DistanceAlgorithm.CHEBYSHEV:
            if self[2] is None:
                return max(abs(target[0] - self[0]), abs(target[1] - self[1]))
            else:
                return max(
                    abs(target[0] - self[0]),
                    abs(target[1] - self[1]),
                    abs(target[2] - self[2]),
                )
        elif algorithm == DistanceAlgorithm.MANHATTAN:
            if not includeDiagonals:
                if self[2] is None:
                    return abs(self[0] - target[0]) + abs(self[1] - target[1])
                else:
                    return abs(self[0] - target[0]) + abs(self[1] - target[1]) + abs(self[2] - target[2])
            else:
                dist = [abs(self[0] - target[0]), abs(self[1] - target[1])]
                if self[2] is None:
                    o_dist = max(dist) - min(dist)
                    return o_dist + 1.4 * min(dist)
                else:
                    dist.append(abs(self[2] - target[2]))
                    d_steps = min(dist)
                    dist.remove(min(dist))
                    dist = [x - d_steps for x in dist]
                    o_dist = max(dist) - min(dist)
                    return 1.7 * d_steps + o_dist + 1.4 * min(dist)

    def inBoundaries(
        self,
        minX: int | float,
        minY: int | float,
        maxX: int | float,
        maxY: int | float,
        minZ: int | float = -inf,
        maxZ: int | float = inf,
    ) -> bool:
        if self[2] is None:
            return minX <= self[0] <= maxX and minY <= self[1] <= maxY
        else:
            return minX <= self[0] <= maxX and minY <= self[1] <= maxY and minZ <= self[2] <= maxZ

    def getCircle(
        self,
        radius: int | float = 1,
        algorithm: DistanceAlgorithm = DistanceAlgorithm.EUCLIDEAN,
        minX: int | float = -inf,
        minY: int | float = -inf,
        maxX: int | float = inf,
        maxY: int | float = inf,
        minZ: int | float = -inf,
        maxZ: int | float = inf,
    ) -> list[Coordinate]:
        ret = []
        if self[2] is None:  # mode 2D
            for x in range(self[0] - radius * 2, self[0] + radius * 2 + 1):
                for y in range(self[1] - radius * 2, self[1] + radius * 2 + 1):
                    target = Coordinate(x, y)
                    if not target.inBoundaries(minX, minY, maxX, maxY):
                        continue
                    dist = round_half_up(self.getDistanceTo(target, algorithm=algorithm, includeDiagonals=False))
                    if dist == radius:
                        ret.append(target)

        else:
            for x in range(self[0] - radius * 2, self[0] + radius * 2 + 1):
                for y in range(self[1] - radius * 2, self[1] + radius * 2 + 1):
                    for z in range(self[2] - radius * 2, self[2] + radius * 2 + 1):
                        target = Coordinate(x, y)
                        if not target.inBoundaries(minX, minY, maxX, maxY, minZ, maxZ):
                            continue
                        dist = round_half_up(self.getDistanceTo(target, algorithm=algorithm, includeDiagonals=False))
                        if dist == radius:
                            ret.append(target)

        return ret

    def getNeighbours(
        self,
        includeDiagonal: bool = True,
        minX: int | float = -inf,
        minY: int | float = -inf,
        maxX: int | float = inf,
        maxY: int | float = inf,
        minZ: int | float = -inf,
        maxZ: int | float = inf,
        dist: int | float = 1,
    ) -> list[Coordinate]:
        """
        Get a list of neighbouring coordinates.

        :param includeDiagonal: include diagonal neighbours
        :param minX: ignore all neighbours that would have an X value below this
        :param minY: ignore all neighbours that would have an Y value below this
        :param minZ: ignore all neighbours that would have an Z value below this
        :param maxX: ignore all neighbours that would have an X value above this
        :param maxY: ignore all neighbours that would have an Y value above this
        :param maxZ: ignore all neighbours that would have an Z value above this
        :param dist: distance to neighbour coordinates
        :return: list of Coordinate
        """
        if self[2] is None:
            if includeDiagonal:
                nb_list = [
                    (-dist, -dist),
                    (-dist, 0),
                    (-dist, dist),
                    (0, -dist),
                    (0, dist),
                    (dist, -dist),
                    (dist, 0),
                    (dist, dist),
                ]
            else:
                nb_list = [(-dist, 0), (dist, 0), (0, -dist), (0, dist)]

            for dx, dy in nb_list:
                if minX <= self[0] + dx <= maxX and minY <= self[1] + dy <= maxY:
                    yield self.__class__(self[0] + dx, self[1] + dy)
        else:
            if includeDiagonal:
                nb_list = [(x, y, z) for x in [-dist, 0, dist] for y in [-dist, 0, dist] for z in [-dist, 0, dist]]
                nb_list.remove((0, 0, 0))
            else:
                nb_list = [
                    (-dist, 0, 0),
                    (0, -dist, 0),
                    (dist, 0, 0),
                    (0, dist, 0),
                    (0, 0, dist),
                    (0, 0, -dist),
                ]

            for dx, dy, dz in nb_list:
                if minX <= self[0] + dx <= maxX and minY <= self[1] + dy <= maxY and minZ <= self[2] + dz <= maxZ:
                    yield self.__class__(self[0] + dx, self[1] + dy, self[2] + dz)

    def getAngleTo(self, target: Coordinate | tuple, normalized: bool = False) -> float:
        """normalized returns an angle going clockwise with 0 starting in the 'north'"""
        if self[2] is not None:
            raise NotImplementedError()  # which angle?!?!

        dx = target[0] - self[0]
        dy = target[1] - self[1]
        if not normalized:
            return degrees(atan2(dy, dx))
        else:
            angle = degrees(atan2(dx, dy))
            if dx >= 0:
                return 180.0 - angle
            else:
                return 180.0 + abs(angle)

    def getLineTo(self, target: Coordinate | tuple) -> List[Coordinate]:
        """this will probably not yield what you expect, when using float coordinates"""
        if target == self:
            return [self]
        diff = target - self

        if self[2] is None:
            steps = gcd(diff[0], diff[1])
            step_x = diff[0] // steps
            step_y = diff[1] // steps
            return [self.__class__(self[0] + step_x * i, self[1] + step_y * i) for i in range(steps + 1)]
        else:
            steps = gcd(diff[0], diff[1], diff[2])
            step_x = diff[0] // steps
            step_y = diff[1] // steps
            step_z = diff[2] // steps
            return [
                self.__class__(self[0] + step_x * i, self[1] + step_y * i, self[2] + step_z * i)
                for i in range(steps + 1)
            ]

    def reverse(self) -> Coordinate:
        if self[2] is None:
            return self.__class__(-self[0], -self[1])
        else:
            return self.__class__(-self[0], -self[1], -self[2])

    def __hash__(self) -> int:
        return hash((self[0], self[1], self[2]))

    def __eq__(self, other: Coordinate | tuple) -> bool:
        if self[2] is None:
            return self[0] == other[0] and self[1] == other[1]
        else:
            return self[0] == other[0] and self[1] == other[1] and self[2] == other[2]

    def __add__(self, other: Coordinate | tuple) -> Coordinate:
        if self[2] is None:
            return self.__class__(self[0] + other[0], self[1] + other[1])
        else:
            return self.__class__(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other: Coordinate | tuple) -> Coordinate:
        if self[2] is None:
            return self.__class__(self[0] - other[0], self[1] - other[1])
        else:
            return self.__class__(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, other: int | float) -> Coordinate:
        if self[2] is None:
            return self.__class__(self[0] * other, self[1] * other)
        else:
            return self.__class__(self[0] * other, self[1] * other, self[2] * other)

    def __mod__(self, other: int | float) -> Coordinate:
        if self[2] is None:
            return self.__class__(self[0] % other, self[1] % other)
        else:
            return self.__class__(self[0] % other, self[1] % other, self[2] % other)

    def __floordiv__(self, other: int | float) -> Coordinate:
        if self[2] is None:
            return self.__class__(self[0] // other, self[1] // other)
        else:
            return self.__class__(self[0] // other, self[1] // other, self[2] // other)

    def __truediv__(self, other: int | float) -> Coordinate:
        if self[2] is None:
            return self.__class__(self[0] / other, self[1] / other)
        else:
            return self.__class__(self[0] / other, self[1] / other, self[2] / other)

    def __str__(self):
        if self[2] is None:
            return "({},{})".format(self[0], self[1])
        else:
            return "({},{},{})".format(self[0], self[1], self[2])

    def __repr__(self):
        if self[2] is None:
            return "{}(x={}, y={})".format(self.__class__.__name__, self[0], self[1])
        else:
            return "{}(x={}, y={}, z={})".format(
                self.__class__.__name__,
                self[0],
                self[1],
                self[2],
            )

    @classmethod
    def generate(
        cls,
        from_x: int | float,
        to_x: int | float,
        from_y: int | float,
        to_y: int | float,
        from_z: int | float = None,
        to_z: int | float = None,
        step: int | float = 1,
    ) -> List[Coordinate]:
        if from_z is None or to_z is None:
            return [cls(x, y) for x in range(from_x, to_x + step, step) for y in range(from_y, to_y + step, step)]
        else:
            return [
                cls(x, y, z)
                for x in range(from_x, to_x + step, step)
                for y in range(from_y, to_y + step, step)
                for z in range(from_z, to_z + step, step)
            ]


class Shape:
    def __init__(self, top_left: Coordinate, bottom_right: Coordinate):
        """
        in 2D mode: top_left is the upper left corner and bottom_right the lower right
                    (top_left.x <= bottom_right.x and top_left.y <= bottom_right.y)
        in 3D mode: same logic applied, just for 3D Coordinates
                    top_left is the upper left rear corner and bottom_right the lower right front
                    (top_left.x <= bottom_right.x and top_left.y <= bottom_right.y and top_left.z <= bottom_right.z)
        """
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.mode_3d = top_left.z is not None and bottom_right.z is not None

    def __len__(self):
        if not self.mode_3d:
            return (self.bottom_right.x - self.top_left.x + 1) * (self.bottom_right.y - self.top_left.y + 1)
        else:
            return (
                (self.bottom_right.x - self.top_left.x + 1)
                * (self.bottom_right.y - self.top_left.y + 1)
                * (self.bottom_right.z - self.top_left.z + 1)
            )

    def intersection(self, other: Shape) -> Union[Shape, None]:
        """
        returns a Shape of the intersecting part, or None if the Shapes don't intersect
        """
        if self.mode_3d != other.mode_3d:
            raise ValueError("Cannot calculate intersection between 2d and 3d shape")

        if not self.mode_3d:
            intersect_top_left = Coordinate(
                self.top_left.x if self.top_left.x > other.top_left.x else other.top_left.x,
                self.top_left.y if self.top_left.y > other.top_left.y else other.top_left.y,
            )
            intersect_bottom_right = Coordinate(
                self.bottom_right.x if self.bottom_right.x < other.bottom_right.x else other.bottom_right.x,
                self.bottom_right.y if self.bottom_right.y < other.bottom_right.y else other.bottom_right.y,
            )
        else:
            intersect_top_left = Coordinate(
                self.top_left.x if self.top_left.x > other.top_left.x else other.top_left.x,
                self.top_left.y if self.top_left.y > other.top_left.y else other.top_left.y,
                self.top_left.z if self.top_left.z > other.top_left.z else other.top_left.z,
            )
            intersect_bottom_right = Coordinate(
                self.bottom_right.x if self.bottom_right.x < other.bottom_right.x else other.bottom_right.x,
                self.bottom_right.y if self.bottom_right.y < other.bottom_right.y else other.bottom_right.y,
                self.bottom_right.z if self.bottom_right.z < other.bottom_right.z else other.bottom_right.z,
            )

        if intersect_top_left <= intersect_bottom_right:
            return self.__class__(intersect_top_left, intersect_bottom_right)

    def __and__(self, other):
        return self.intersection(other)

    def __rand__(self, other):
        return self.intersection(other)

    def __contains__(self, item: Coordinate) -> bool:
        if not self.mode_3d:
            return self.top_left.x <= item.x <= self.bottom_right.x and self.top_left.y <= item.y <= self.bottom_right.y
        else:
            return (
                self.top_left.x <= item.x <= self.bottom_right.x
                and self.top_left.y <= item.y <= self.bottom_right.y
                and self.top_left.z <= item.z <= self.bottom_right.z
            )

    def __str__(self):
        return "%s(%s -> %s)" % (
            self.__class__.__name__,
            self.top_left,
            self.bottom_right,
        )

    def __repr__(self):
        return "%s(%s, %s)" % (
            self.__class__.__name__,
            self.top_left,
            self.bottom_right,
        )


class Rectangle(Shape):
    def __init__(self, top_left, bottom_right):
        super(Rectangle, self).__init__(top_left, bottom_right)
        self.mode_3d = False


class Cube(Shape):
    def __init__(self, top_left, bottom_right):
        if top_left.z is None or bottom_right.z is None:
            raise ValueError("Both Coordinates need to be 3D")
        super(Cube, self).__init__(top_left, bottom_right)


# FIXME: Line could probably also just be a subclass of Shape
class Line:
    def __init__(self, start: Coordinate, end: Coordinate):
        if start[2] is not None or end[2] is not None:
            raise NotImplementedError("3D Lines are hard(er)")
        self.start, self.end = minmax(start, end)

    def is_horizontal(self) -> bool:
        return self.start[1] == self.end[1]

    def is_vertical(self) -> bool:
        return self.start[0] == self.end[0]

    def connects_to(self, other: Line) -> bool:
        return self.start == other.start or self.start == other.end or self.end == other.start or self.end == other.end

    def intersects(self, other: Line, strict: bool = True) -> bool:
        try:
            self.get_intersection(other, strict=strict)
            return True
        except ValueError:
            return False

    def get_intersection(self, other: Line, strict: bool = True) -> Coordinate:
        xdiff = (self.start[0] - self.end[0], other.start[0] - other.end[0])
        ydiff = (self.start[1] - self.end[1], other.start[1] - other.end[1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise ValueError("lines do not intersect")

        d = (det(self.start, self.end), det(other.start, other.end))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        ret = Coordinate(x, y)

        if not strict:
            return ret
        else:
            if ret in self and ret in other:
                return ret
            else:
                raise ValueError("intersection out of bounds")

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other: Line) -> bool:
        return hash(self) == hash(other)

    def __lt__(self, other: Line) -> bool:
        return self.start < other.start

    def __contains__(self, point: Coordinate | tuple) -> bool:
        return isclose(
            self.start.getDistanceTo(self.end),
            self.start.getDistanceTo(point) + self.end.getDistanceTo(point),
        )

    def __len__(self) -> int:
        return int(self.start.getDistanceTo(self.end))

    def __str__(self):
        return f"Line({self.start} -> {self.end})"

    def __repr__(self):
        return str(self)


class Polygon:
    def __init__(self, points: list[Coordinate]) -> None:
        """points have to be in (counter)clockwise order, not repeating the first coordinate"""
        if len(set(points)) != len(points):
            raise ValueError("Polygon contains repeated points")

        self.points = points
        self.lines = set()
        for i in range(len(points) - 1):
            self.lines.add(Line(points[i], points[i + 1]))
        self.lines.add(Line(points[-1], points[0]))

    def get_circumference(self) -> float:
        return sum(len(x) for x in self.lines)

    def get_area(self) -> float:
        S = 0
        for i in range(len(self.points)):
            S += (
                self.points[i].x * self.points[(i + 1) % len(self.points)].y
                - self.points[(i + 1) % len(self.points)].x * self.points[i].y
            )

        return abs(S) / 2

    def decompose(self) -> Iterable[Rectangle]:
        points_left = list(self.points)

        def flip(point: Coordinate):
            if point in points_left:
                points_left.remove(point)
            else:
                points_left.append(point)

        while points_left:
            pk, pl, pm = None, None, None
            for c in sorted(points_left, key=lambda p: (p[1], p[0])):
                if pk is None:
                    pk = c
                    continue

                if pl is None:
                    pl = c
                    continue

                if pk.x <= c.x < pl.x and pk.y < c.y:
                    pm = c
                    break

            flip(pk)
            flip(pl)
            flip(Coordinate(pk.x, pm.y))
            flip(Coordinate(pl.x, pm.y))
            yield Rectangle(pk, Coordinate(pl.x, pm.y))
