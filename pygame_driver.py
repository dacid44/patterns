import sys

import pygame
from pygame import gfxdraw
import easygui

from driver import Driver


settings = easygui.multenterbox(msg='Leave starting color blank for a random starting color.', title='Settings',
                                fields=['Width', 'Height',
                                        'Background color', 'Line color', 'Point color',
                                        'Starting color', 'Color weight'],
                                values=[800, 600, '#FFFFFF', '#000000', '#FF0000', '', 2.5])
if settings is None:
    sys.exit()
size = (int(settings[0]), int(settings[1]))
colors = {
    'background': tuple(int(settings[2].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)),  # default white
    'lines': tuple(int(settings[3].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)),       # default black
    'points': tuple(int(settings[4].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))       # default red
}
print(colors)
first_color = None if settings[5] == '' else tuple(int(settings[5].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
color_weight = float(settings[6])  # default 2.5

def setup(canvas, types):
    types['point'](size[0] // 2 - 50, size[1] // 2, canvas).new_line((size[0] // 2 + 50, size[1] // 2))

driver = Driver(setup, color_weight=color_weight)
pygame.init()
display = pygame.display.set_mode(size)
pygame.display.set_caption('Triangles')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            driver.new_triangle(event.pos, color=first_color)
            if first_color is not None:
                first_color = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            driver.fill_triangle(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            driver.clear()

    display.fill(colors['background'])
    for shape in driver['shapes']:
        points = list(map(lambda x: x.get_pos(), shape.get_points()))
        gfxdraw.aapolygon(display, points, shape.get_color())
        gfxdraw.filled_polygon(display, points, shape.get_color())
    for line in driver['lines']:
        points = list(map(lambda x: x.get_pos(), line.get_points()))
        pygame.draw.aaline(display, colors['lines'], *points, 1)
    for point in driver['points']:
        gfxdraw.aacircle(display, *point.get_pos(), 3, colors['points'])
        gfxdraw.filled_circle(display, *point.get_pos(), 3, colors['points'])

    pygame.display.update()
