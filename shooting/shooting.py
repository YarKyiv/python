

import pyglet
from pyglet import shapes
from pyglet import clock

import math
import shooting_logic



#  logic
def distanse(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def one_step(i):
    r = optical_sight_sprite.radius
    optical_sight_sprite.radius = max(r - r0_reduction, r0)


def reduction_r0():
    clock.schedule_interval(one_step, 0.5)

# config data
r0 = 100  # радиус круга разброса
r0_max = 2*r0
r0_op = 50  # прозрачность круга разброса
cells = 10  # кол-во выстрело
cells_r = 3  # радиус выстрелов
wind_x = 800  # размер экрана
wind_y = 800
motion_shift = 1  # увеличение радиуса круга разброса при движении мыши   1 пикс на 1 пикс
r0_reduction = 0.1  # скорость сведение  пикс/секунду

# circle_r = 50

# pyglet

window = pyglet.window.Window(wind_x, wind_y)

back_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()

optical_sight_sprite = shapes.Circle(x=-2 * r0, y=-2 * r0, radius=r0, color=(50, 225, 30), batch=main_batch)
optical_sight_sprite.opacity = r0_op

# создание  шейпов выстрелов
shot_shape_list = []
for i in range(cells):
    shot_shape_list.append(
        shapes.Circle(x=-2 * cells_r, y=-2 * cells_r, radius=cells_r, color=(255, 50, 50), batch=back_batch))
    shot_shape_list[i].opacity = 100


# water_back = pyglet.sprite.Sprite(pyglet.image.load("marine/900_back_marine.png"), x=shift_x, y=shift_y, batch=back_batch)


@window.event
def on_draw():
    window.clear()
    # label1.draw()
    back_batch.draw()
    main_batch.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    # print(x, y)

    dr = min(math.sqrt(dx ** 2 + dy ** 2) * motion_shift, r0_max)
    optical_sight_sprite.x = x
    optical_sight_sprite.y = y
    optical_sight_sprite.radius = max(r0 + dr, optical_sight_sprite.radius)
    reduction_r0()
    # ctrl + /  (numpad)


@window.event
def on_mouse_press(x, y, button, modifiers):
    # print(x, y)
    for i in range(cells):
        coord = shooting_logic.shot_analys(x, y, optical_sight_sprite.radius)
        shot_shape_list[i].x = coord[0]
        shot_shape_list[i].y = coord[1]
        #print(coord)

        if distanse(x, y, coord[0], coord[1]) < 5:
            print("+1!")


pyglet.app.run()
