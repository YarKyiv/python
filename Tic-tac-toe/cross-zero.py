import pyglet
import random

# from pyglet import shapes
from pyglet.window import mouse

# ---------------------[ config ] -----------------------------------------
windows_x = 600
windows_y = 600
cell_size = windows_x // 3
cross_numb = 0
zeros_numb = 0
now_cross = 1  # 0 - нолики Zero   1 - крестики Cross
map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 0 - none , 1 - cross , 2 - zero
# ---------------------[ Vizual ] -----------------------------------------

window = pyglet.window.Window(windows_x, windows_y)
batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()
list_sprite_zero = []
list_sprite_cross = []
zero_image = pyglet.image.load('zero.png')
cross_image = pyglet.image.load('cross.png')
for i in range(6):
    list_sprite_zero.append(pyglet.sprite.Sprite(zero_image, -cell_size, -cell_size, batch=batch))
    list_sprite_cross.append(pyglet.sprite.Sprite(cross_image, -cell_size, --cell_size, batch=batch))


def set_cross(xl, yl):
    list_sprite_cross[cross_numb].x = xl * cell_size
    list_sprite_cross[cross_numb].y = yl * cell_size


def set_zero(xl, yl):
    list_sprite_zero[zeros_numb].x = xl * cell_size
    list_sprite_zero[zeros_numb].y = yl * cell_size


# --------------------------------[  Logic  ]-------------------------------------------------------------
def set_cross_l(xl, yl):
    map[yl][xl] = 1


def set_zero_l(xl, yl):
    map[yl][xl] = 2


def test_win(p):  #  1 - cross , 2 - zero
    signum = ['cross', 'zero']
    vertical = ['left','centre','right']
    horizontal = ['down', 'middle', 'top']
    digonal = ['sunrise', 'sunset']
    for xl in range(3):
        cur_counter = 0
        for yl in range(3):
            if map[yl][xl] == p:  # 0 0 , 0 1 , 0 2
                cur_counter += 1
        if cur_counter == 3:
            print(f'{vertical[xl]} vertical {signum[p-1]} line')

    for yl in range(3):
        cur_counter = 0
        for xl in range(3):
            if map[yl][xl] == p:  # 0 0 , 0 1 , 0 2
                cur_counter += 1
        if cur_counter == 3:
            print(f'{horizontal[yl]} horizontal {signum[p-1]} line')

    cur_counter = 0
    for n in range(3):
        if map[n][n] == p:  # 0 0 , 0 1 , 0 2
            cur_counter += 1
    if cur_counter == 3:
        print(f'{digonal[0]} diagonal {signum[p-1]} line')

    cur_counter = 0
    for n in range(3):#  0  1  2   =>    2  1  0   y= -x+2
        if map[n][2-n] == p:  # 0 0 , 0 1 , 0 2
            cur_counter += 1
    if cur_counter == 3:
        print(f'{digonal[1]} diagonal {signum[p-1]} line')



def comp_step():
    global now_cross, zeros_numb
    if zeros_numb + cross_numb == 9:
        print('no steps')
    else:
        zero_relized = 0
        error_count = 0
        while zero_relized == 0:
            xl = random.randint(0, 2)
            yl = random.randint(0, 2)
            if map[yl][xl] == 0:
                set_zero(xl, yl)
                set_zero_l(xl, yl)
                zero_relized = 1
                zeros_numb += 1
                error_count = 0
                now_cross = 1 - now_cross
                print(f'{xl, yl} ok')

            else:
                error_count += 1
                zero_relized = 0
                print(f'{xl, yl} error {error_count}')
                # if error_count > 10:


# ---------------------------------[ control ]---------------------------------
@window.event
def on_draw():
    window.clear()
    bg_batch.draw()
    batch.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global cross_numb, now_cross, zeros_numb
    xl = int(x / cell_size)
    yl = int(y / cell_size)
    if now_cross == 1:
        if button == mouse.LEFT and map[yl][xl] == 0:
            set_cross(xl, yl)
            set_cross_l(xl, yl)
            print(xl, yl)
            cross_numb += 1
            now_cross = 1 - now_cross
            test_win(1) #  1 - cross  2 - zero
            comp_step()
            test_win(2)


pyglet.app.run()
