import pyglet
import life_data
import life_logic

from pyglet import clock

from pyglet import shapes
from pyglet.window import mouse

g_x = life_data.g_x
g_y = life_data.g_y
sq = life_data.sq


def set_template(x, y, n):  # n - number of template
    # life_logic.template_list
    for i in life_logic.template_list[n]:  # for i in range(len(life_logic.template_list[n])):
        # template_planer=[[0, -0], [1, -1], [1, -2], [0, -2], [-1, -2]]
        life_logic.setLife(x + i[0], y + i[1], 1)
    show_life()


def check_region(x, y, r):
    xl = region[r][0]
    xr = region[r][2]
    yl = region[r][1]
    yr = region[r][3]
    return (xl < x < xr and yl < y < yr)


def setColor(x, y, s):
    shape_rect[y * g_x + x].color = life_color[s]


def show_life():
    for y in range(g_y):
        for x in range(g_x):
            setColor(x, y, life_logic.getLife(x, y))


def one_step(i=1):
    life_logic.nextStep()
    show_life()
    #print(int(i))


def life_time():
    clock.schedule_interval(one_step, 0.5)


def clear():
    life_logic.clear_field()
    show_life()

# загрузить имидж по "пути" (1)
# указать координаты левого нижнего угла х,у (2,3)
# батч (4)
# массив с зонами (5)

def set_button(path, x, y, batch, reg_list, sprt_list):
    temp_img = pyglet.image.load(path)
    reg_w = temp_img.width
    reg_h = temp_img.height

    temp_sprite = pyglet.sprite.Sprite(temp_img, x=x, y=y, batch=batch)
    reg_list.append([x,y, x+reg_w, y+reg_h])
    sprt_list.append(temp_sprite)

def set_opacity(n, op):
    sprite_list[n].opacity = op



window = pyglet.window.Window(g_x * (sq + 1) + 100, g_y * (sq + 1))
batch = pyglet.graphics.Batch()
last_life = [0, 0]
set_temp = 0
temp_numb = 0
time_flag = 0

life_color = [(80, 80, 80), (80, 255, 80)]

shape_rect = []
for y in range(g_y):
    for x in range(g_x):
        shape_rect.append(
            shapes.Rectangle(x=x * (sq + 1), y=y * (sq + 1), width=sq, height=sq, color=life_color[0], batch=batch))

r0 = [0, 0, g_x * (sq + 1), g_y * (sq + 1)]

region = [r0]

sprite_list=[]





# загрузить имидж по "пути" (1)
# указать координаты левого нижнего угла х,у (2,3)
# батч (4)
# массив с зонами (5)
set_button('life/button_next_step.png', g_x * (sq + 1), g_y * (sq + 1) - 100, batch, region, sprite_list)
set_button('life/button.png', g_x * (sq + 1), g_y * (sq + 1) - 200, batch, region, sprite_list)
set_button('life/button_clear.png', g_x * (sq + 1), g_y * (sq + 1) - 300, batch, region, sprite_list)
set_button('life/temp_planer-50.png', g_x * (sq + 1), g_y * (sq + 1) - 400, batch, region, sprite_list)
set_button('life/temp_spaceship-50.png', g_x * (sq + 1), g_y * (sq + 1) - 500, batch, region, sprite_list)



@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global set_temp, temp_numb, time_flag

    if button == mouse.LEFT and check_region(x, y, 0):
        xl = int(x / (sq + 1))
        yl = int(y / (sq + 1))
        setColor(xl, yl, 1 - life_logic.getLife(xl, yl))
        life_logic.setLife(xl, yl, 1 - life_logic.getLife(xl, yl))
        # last_life[0]=xl
        # last_life[1]=yl
        if set_temp:
            set_template(xl, yl, temp_numb)
            set_temp = 0

    if button == mouse.LEFT and check_region(x, y, 1):
        one_step()
    if button == mouse.LEFT and check_region(x, y, 2):
        if not time_flag:
            life_time()
            time_flag = 1
            set_opacity(1, 128)

        else:
            time_flag = 0
            clock.unschedule(one_step)
            set_opacity(1, 255)

    if button == mouse.LEFT and check_region(x, y, 3):
        clear()

    if button == mouse.LEFT and check_region(x, y, 4):
        set_temp = 1
        temp_numb = 0

    if button == mouse.LEFT and check_region(x, y, 5):
        set_temp = 1
        temp_numb = 1
    # set_template(last_life[0],last_life[1],0)


pyglet.app.run()
