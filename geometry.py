import math
from typing import Union, List, Collection

import shapely.geometry


class Canvas:
    def __init__(self):
        self.points = []
        self.lines = []
        self.shapes = []

    def __getitem__(self, item: str):
        if item == 'points':
            return self.points
        elif item == 'lines':
            return self.lines
        elif item == 'shapes':
            return self.shapes
        else:
            raise KeyError(item)

    def __setitem__(self, key: str, value: Union[List['Point'], List['Line'], List['Shape']]):
        if key == 'points':
            self.points = value
        elif key == 'lines':
            self.lines = value
        elif key == 'shapes':
            self.shapes = value
        else:
            raise KeyError(key)

    def add_point(self, point: 'Point'):
        self.points.append(point)

    def add_line(self, line: 'Line'):
        self.lines.append(line)

    def add_shape(self, shape: 'Shape'):
        self.shapes.append(shape)

    def clear(self):
        self.points = []
        self.lines = []
        self.shapes = []

    def get_closest(self, point: Union['Point', Collection[Union[int, float]]]):
        return sorted(self['points'], key=lambda x: x.get_distance(point))

    def is_in_any_triangle(self, point: Union['Point', Collection[Union[int, float]]]):
        if type(point) is Point:
            point = point.get_pos()
        point = shapely.geometry.Point(*point)
        return any(map(lambda x: x.obj.contains(point), self['shapes']))

    def point_exists(self, point: Union['Point', Collection[Union[int, float]]]):
        if type(point) is Point:
            point = point.get_pos()
        for cand_point in self['points']:
            if cand_point.get_pos() == point:
                return True
        return False

    def line_exists(self, line: Union['Line', Collection['Point']]):
        if type(line) is Line:
            line = line.get_points()
        for test_line in self['lines']:
            if test_line.get_points() == line:
                return True
        return False

    def would_cross(self, line: Union['Line', Collection[Collection[Union[int, float]]]]):
        line = set(map(lambda x: x.get_pos(), line.get_points())) if type(line) is Line else set(line)
        for cand_line in self['lines']:
            if cand_line.get_points(raw=True).isdisjoint(line) and \
                    shapely.geometry.LineString(self.point_list(line)).intersects(cand_line.obj):
                return True
        return False

    @classmethod
    def would_cross_lines(cls, line, test_lines):
        line_obj = shapely.geometry.LineString(cls.point_list(line))
        line = set(line)
        for test_line in test_lines:
            if line.isdisjoint(set(test_line)) and \
                    shapely.geometry.LineString(cls.point_list(test_line)).intersects(line_obj):
                return True
        return False

    @classmethod
    def is_inside(cls, point, test_points):
        points_obj = shapely.geometry.Polygon(cls.point_list(test_points, 3))
        return points_obj.contains(shapely.geometry.Point(point))

    def get_line(self, p1: 'Point', p2: 'Point'):
        points = {p1, p2}
        line = None
        for test_line in self['lines']:
            if test_line.get_points == points:
                line = test_line
                break
        if line is None:
            line = p1.new_line(p2)[1]
        return line

    @staticmethod
    def point_list(from_obj, size=2):
        to_return = list(from_obj)
        while len(to_return) < size:
            to_return.append(to_return[-1])
        return to_return


class Point:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.canvas.add_point(self)
        self.lines = []
        self.obj = shapely.geometry.Point(x, y)

    def get_pos(self):
        return self.x, self.y

    def get_lines(self):
        return self.lines

    def add_line(self, line: 'Line'):
        if line not in self.lines:
            self.lines.append(line)

    def new_line(self, point: Union['Point', Collection[Union[int, float]]]):
        if type(point) is not Point:
            point = Point(point[0], point[1], self.canvas)
        line = Line(self, point, self.canvas)
        self.add_line(line)
        point.add_line(line)
        return point, line

    def get_distance(self, point: Union['Point', Collection[Union[int, float]]]):
        x, y = point.get_pos() if type(point) is Point else point
        return math.hypot(abs(self.x - x), abs(self.y - y))

    def __eq__(self, other: 'Point'):
        return self.get_pos == other.get_pos

    def __hash__(self):
        return hash((self.x, self.y))


class Line:
    def __init__(self, p1, p2, canvas):
        self.points = frozenset((p1, p2))
        self.canvas = canvas
        self.canvas.add_line(self)
        self.obj = shapely.geometry.LineString((p1.get_pos(), p2.get_pos()))

    def get_points(self, raw=False):
        return set(map(lambda x: x.get_pos(), self.points)) if raw else self.points

    def __eq__(self, other):
        return self.points == other.points

    def __hash__(self):
        return hash(self.points)


class Shape:
    def __init__(self, sides: Collection[Line], canvas):
        self.sides = set(sides)
        self.canvas = canvas
        self.canvas.add_shape(self)
        self.obj = shapely.geometry.Polygon(map(lambda x: x.get_pos(), self.get_points()))

    def get_sides(self):
        return self.sides

    def get_points(self, raw=False):
        points = set()
        for side in self.sides:
            for point in side.get_points():
                points.add(point.get_pos() if raw else point)
        return points
