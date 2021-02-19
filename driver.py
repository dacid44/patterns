from geometry import Canvas, Point, Line, Shape

from typing import Union, List, Collection


class Driver:
    def __init__(self, setup_func, color_weight=2.5):
        self.canvas = Canvas(color_weight)
        self.setup_func = setup_func
        self.types = {'point': Point, 'line': Line, 'shape': Shape}
        self.setup_func(self.canvas, self.types)

    def clear(self):
        self.canvas.clear()
        self.setup_func(self.canvas, self.types)

    def new_triangle(self, pos, color=None):
        closest = self.canvas.get_closest(pos)
        valid = list(filter(lambda x: not self.canvas.would_cross([x.get_pos(), pos]), closest))
        if not self.canvas.point_exists(pos) and not self.canvas.is_in_any_triangle(pos) and not \
                self.canvas.would_cross([valid[0].get_pos(), valid[1].get_pos()]):
            while len(valid) >= 2:
                if not self.canvas.line_exists(set(valid[:2])):
                    valid.pop(1)
                else:
                    new_point = Point(*pos, self.canvas)
                    old_line = self.canvas.get_line(valid[0], valid[1])
                    line1 = self.canvas.get_line(valid[0], new_point)
                    line2 = self.canvas.get_line(valid[1], new_point)
                    Shape((old_line, line1, line2), self.canvas, color=color)
                    break

    def fill_triangle(self, pos, color=None):
        if not self.canvas.point_exists(pos) and not self.canvas.is_in_any_triangle(pos):
            closest = self.canvas.get_closest(pos)
            valid = list(filter(lambda x: not self.canvas.would_cross([x.get_pos(), pos]), closest))
            while len(valid) >= 3:
                test_lines = [
                    [valid[0].get_pos(), valid[1].get_pos()],
                    [valid[1].get_pos(), valid[2].get_pos()],
                    [valid[0].get_pos(), valid[1].get_pos()]
                ]
                skip = False
                for i in range(3):
                    if self.canvas.would_cross_lines([valid[i].get_pos(), pos], test_lines) or not \
                            self.canvas.is_inside(pos, map(lambda x: x.get_pos(), valid[:3])):
                        valid.pop(i)
                        skip = True
                        break
                if not skip:
                    line1 = self.canvas.get_line(valid[0], valid[1])
                    line2 = self.canvas.get_line(valid[1], valid[2])
                    line3 = self.canvas.get_line(valid[0], valid[2])
                    Shape((line1, line2, line3), self.canvas, color=color)
                    break

    def __getitem__(self, item: str):
        if item == 'points':
            return self.canvas.points
        elif item == 'lines':
            return self.canvas.lines
        elif item == 'shapes':
            return self.canvas.shapes
        else:
            raise KeyError(item)

    def __setitem__(self, key: str, value: List[Union[Point, Line, Shape]]):
        if key == 'points':
            self.canvas.points = value
        elif key == 'lines':
            self.canvas.lines = value
        elif key == 'shapes':
            self.canvas.shapes = value
        else:
            raise KeyError(key)
