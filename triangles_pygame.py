import sys
from random import randint

import pygame
from pygame import gfxdraw

from geometry import Canvas, Point, Line, Shape


pygame.init()

colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
}
size = (800, 600)

canvas = Canvas()
canvas.display = pygame.display.set_mode(size)
center1 = Point(size[0] // 2 - 50, size[1] // 2, canvas)
center2, center_line = center1.new_line((size[0] // 2 + 50, size[1] // 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            pos = event.pos
            closest = canvas.get_closest(pos)
            valid = list(filter(lambda x: not canvas.would_cross([x.get_pos(), pos]), closest))
            if not canvas.point_exists(pos) and not canvas.is_in_any_triangle(pos) and not \
                    canvas.would_cross([valid[0].get_pos(), valid[1].get_pos()]):
                while len(valid) >= 2:
                    if not canvas.line_exists(set(valid[:2])):
                        valid.pop(1)
                    else:
                        new_point = Point(*pos, canvas)
                        old_line = canvas.get_line(valid[0], valid[1])
                        line1 = canvas.get_line(valid[0], new_point)
                        line2 = canvas.get_line(valid[1], new_point)
                        Shape((old_line, line1, line2), canvas)
                        break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            pos = event.pos
            if not canvas.point_exists(pos) and not canvas.is_in_any_triangle(pos):
                closest = canvas.get_closest(pos)
                valid = list(filter(lambda x: not canvas.would_cross([x.get_pos(), pos]), closest))
                while len(valid) >= 3:
                    test_lines = [
                        [valid[0].get_pos(), valid[1].get_pos()],
                        [valid[1].get_pos(), valid[2].get_pos()],
                        [valid[0].get_pos(), valid[1].get_pos()]
                    ]
                    skip = False
                    for i in range(3):
                        if canvas.would_cross_lines([valid[i].get_pos(), pos], test_lines):
                            valid.pop(i)
                            skip = True
                            break
                    if not skip and not canvas.is_inside(pos, map(lambda x: x.get_pos(), valid[:3])):
                        valid.pop(2)
                        skip = True
                    if not skip:
                        line1 = canvas.get_line(valid[0], valid[1])
                        line2 = canvas.get_line(valid[1], valid[2])
                        line3 = canvas.get_line(valid[0], valid[2])
                        Shape((line1, line2, line3), canvas)
                        break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            canvas.clear()
            Point(size[0] // 2 - 50, size[1] // 2, canvas).new_line((size[0] // 2 + 50, size[1] // 2))

    canvas.display.fill(colors['white'])
    for shape in canvas['shapes']:
        points = list(map(lambda x: x.get_pos(), shape.get_points()))
        gfxdraw.aapolygon(canvas.display, points, shape.get_color())
        gfxdraw.filled_polygon(canvas.display, points, shape.get_color())
    for line in canvas['lines']:
        points = list(map(lambda x: x.get_pos(), line.get_points()))
        pygame.draw.aaline(canvas.display, colors['black'], *points, 1)
    for point in canvas['points']:
        gfxdraw.aacircle(canvas.display, *point.get_pos(), 3, colors['red'])
        gfxdraw.filled_circle(canvas.display, *point.get_pos(), 3, colors['red'])

    pygame.display.update()
