import sys
from random import randint

import pygame
from pygame import gfxdraw

from geometry import *


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
            if len(valid) >= 2 and not canvas.point_exists(pos) and not canvas.is_in_any_triangle(pos) and not \
                    canvas.would_cross([valid[0].get_pos(), valid[1].get_pos()]):
                new_point = Point(*pos, canvas)
                old_line = canvas.get_line(valid[0], valid[1])
                line1 = valid[0].new_line(new_point)[1]
                line2 = valid[1].new_line(new_point)[1]
                Shape((old_line, line1, line2), canvas)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            pos = event.pos
            closest = canvas.get_closest(pos)
            valid = list(filter(lambda x: not canvas.would_cross([x.get_pos(), pos]), closest))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            canvas.clear()
            Point(size[0] // 2 - 50, size[1] // 2, canvas).new_line((size[0] // 2 + 50, size[1] // 2))

    canvas.display.fill(colors['white'])
    for shape in canvas['shapes']:
        points = list(map(lambda x: x.get_pos(), shape.get_points()))
        gfxdraw.aapolygon(canvas.display, points, colors['green'])
        gfxdraw.filled_polygon(canvas.display, points, colors['green'])
    for line in canvas['lines']:
        points = list(map(lambda x: x.get_pos(), line.get_points()))
        pygame.draw.aaline(canvas.display, colors['black'], *points, 1)
    for point in canvas['points']:
        gfxdraw.aacircle(canvas.display, *point.get_pos(), 3, colors['red'])
        gfxdraw.filled_circle(canvas.display, *point.get_pos(), 3, colors['red'])

    pygame.display.update()
