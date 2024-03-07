import pyglet
import random
import math

from pyglet import clock
from pyglet import shapes
from pyglet.window import mouse

# ---------------------[ config ] -----------------------------------------

# hero_shape = shapes.Circle(hero_x, hero_y, radius=10, color=(0, 255, 0), batch=batch)
worm_shape_list = []
long = 10  # worm_size
size = 10  # worm shape size
speed = 10
start_x = 300
start_y = 300
interval = 0.1
cord_list = []
angle = 0
food_numb = 10
food_numb_max = 10
food_size = 5
food_cord_list = []
food_shape_list = []
windows_x = 600
windows_y = 650
food_color = [(0, 255, 0), (255, 255, 0), (128, 128, 0)]
food_satiety_start = 100
food_satiety = food_satiety_start
food_pending = 1
food_volume = [100, 300, 200]
food = []
font_size = 12
mause_click_max = 19
mause_click_current = 0
interface_y = 70
font_name = 'Times New Roman'
food_unit_eaten = 0
new_round_on = 1
lvl_curr = 1
lvl_eaten_food = 0

window = pyglet.window.Window(windows_x, windows_y + interface_y)
batch = pyglet.graphics.Batch()
bg_batch = pyglet.graphics.Batch()


# ---------------------[ Vizual ] -----------------------------------------
class my_button_shape:
    def __init__(self, name, x, y, dx, dy, color_bg, color_txt):
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.click_zone = [x, y, x + dx, y + dy]
        self.color_bg = color_bg
        self.color_txt = color_txt
        self.shape = shapes.Rectangle(x, y, dx, dy, color=color_bg, batch=bg_batch)
        self.label_button = pyglet.text.Label(name,
                                              font_name=font_name,
                                              font_size=font_size,
                                              color=color_txt,
                                              x=x + dx // 2, y=y + dy // 2,
                                              anchor_x='center', anchor_y='center',
                                              batch=batch)


def show_info():
    click_l = mause_click_max - mause_click_current + 1
    label_satiety.text = f'satiety: {food_satiety} '
    label_click.text = f'clicks: {click_l}'
    label_eaten.text = f'food eaten: {food_unit_eaten}'
    label_curr_lvl.text = f'lvl: {lvl_curr}'


def test_zone(x, y, obg):
    return obg.click_zone[0] < x < obg.click_zone[2] and obg.click_zone[1] < y < obg.click_zone[3]


label_satiety = pyglet.text.Label(f'satiety: {food_satiety} ',
                                  font_name=font_name,
                                  font_size=font_size,
                                  color=(255, 255, 255, 255),
                                  x=20, y=window.height - font_size * 2,
                                  anchor_x='left', anchor_y='center',
                                  batch=batch)
label_click = pyglet.text.Label(f'clicks: {mause_click_max - mause_click_current + 1}',
                                font_name=font_name,
                                font_size=font_size,
                                color=(255, 255, 255, 255),
                                x=20, y=window.height - font_size * 4,
                                anchor_x='left', anchor_y='center',
                                batch=batch)
label_game_over = pyglet.text.Label('satiety = 1000',
                                    font_name='Times New Roman',
                                    font_size=font_size,
                                    color=(255, 255, 255, 255),
                                    x=window.width // 2, y=- font_size * 2,
                                    anchor_x='center', anchor_y='center',
                                    batch=batch)
label_eaten = pyglet.text.Label(f'food eaten: {food_unit_eaten}',
                                font_name=font_name,
                                font_size=font_size,
                                color=(255, 255, 255, 255),
                                x=120, y=window.height - font_size * 4,
                                anchor_x='left', anchor_y='center',
                                batch=batch)

label_curr_lvl = pyglet.text.Label(f'lvl: {lvl_curr} ',
                                   font_name=font_name,
                                   font_size=font_size,
                                   color=(255, 255, 255, 255),
                                   x=120, y=window.height - font_size * 2,
                                   anchor_x='left', anchor_y='center',
                                   batch=batch)


def food_create():
    global food_numb
    for i in range(food_numb):
        x = random.randint(0, windows_x)
        y = random.randint(0, windows_y)
        food_cord_list.append([x, y])
        food.append(random.randint(0, 2))
        food_shape_list.append(
            shapes.Circle(x, y, radius=food_size + 5 * (2 - food[i]), color=food_color[food[i]], batch=batch)
        )


def worm_create():
    for i in range(long):
        x = start_x - size * i
        y = start_y
        cord_list.append([x, y])  # [x,y]
        worm_shape_list.append(
            shapes.Circle(x, y, radius=size, color=(255 - i * 20, 0 + i * 25, 0), batch=batch)
        )


shapes_bg = shapes.Rectangle(0, 0, windows_x, windows_y, color=(0, 64, 0), batch=bg_batch)
new_round_button = my_button_shape("restart round", windows_x // 2, windows_y + 10, 100, 40, (0, 128, 0),
                                   (255, 255, 255, 255))

new_game_button = my_button_shape("new_game", windows_x // 2 + 110, windows_y + 10, 100, 40, (128, 0, 0),
                                  (255, 255, 255, 255))


# --------------------------------[  Logic  ]-------------------------------------------------------------

def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return (dx ** 2 + dy ** 2) ** .5


def food_collision():
    global food_satiety, food_unit_eaten, lvl_eaten_food
    for i in range(food_numb):
        xh = cord_list[0][0]
        yh = cord_list[0][1]
        xf = food_cord_list[i][0]
        yf = food_cord_list[i][1]
        d = distance(xh, yh, xf, yf)
        if d <= size + food_size + 5 * (2 - food[i]):
            food_satiety += food_volume[food[i]]
            food_shape_list[i].x = -20
            food_shape_list[i].y = -20
            food_cord_list[i][0] = -20
            food_cord_list[i][1] = -20
            food_unit_eaten += 1
            lvl_eaten_food += 1


def set_head_new_step():
    global angle
    angle += random.random() * math.pi / 3 - math.pi / 6
    x = cord_list[0][0] + speed * math.cos(angle)
    y = cord_list[0][1] + speed * math.sin(angle)
    if x > windows_x:
        x -= windows_x
    if y > windows_y:
        y -= windows_y
    if y < 0:
        y += windows_y
    if x < 0:
        x += windows_x
    cord_list.insert(0, [int(x), int(y)])
    cord_list.pop()


def show_worm():
    for i in range(long):
        worm_shape_list[i].x = cord_list[i][0]
        worm_shape_list[i].y = cord_list[i][1]


def one_step(d):
    global food_satiety, food_pending
    food_satiety -= food_pending
    if mause_click_current > mause_click_max and lvl_eaten_food < food_numb:
        end_round()
    if food_satiety >= 0:
        set_head_new_step()
        show_worm()
        food_collision()

        show_info()
    else:
        end_round()
    if lvl_eaten_food >= food_numb:
        next_round()


def end_round():
    global new_round_on
    clock.unschedule(one_step)
    click_l = mause_click_max - mause_click_current + 1
    label_game_over.text = f'Round over. Clicks:{click_l}, satiety: {food_satiety}'
    label_game_over.y = windows_y // 2
    new_round_on = 1


def new_round():
    global mause_click_current, mause_click_max, food_satiety, new_round_on, lvl_eaten_food, food_unit_eaten
    print('new_round')
    food_unit_eaten -= lvl_eaten_food
    lvl_eaten_food = 0
    clock.unschedule(one_step)
    label_game_over.y = - font_size
    mause_click_current = 0
    food_satiety = food_satiety_start
    worm_shape_list.clear()
    food.clear()
    food_shape_list.clear()
    food_cord_list.clear()
    food_create()
    worm_create()
    clock.schedule_interval(one_step, interval)
    new_round_on = 0


def new_game():
    global mause_click_current, mause_click_max, food_satiety, new_round_on, food_numb, food_unit_eaten, lvl_curr, lvl_eaten_food
    clock.unschedule(one_step)
    food_numb = food_numb_max
    label_game_over.y = - font_size
    mause_click_current = 0
    food_satiety = food_satiety_start
    food_unit_eaten = 0
    lvl_eaten_food = 0
    cord_list.clear()
    worm_shape_list.clear()
    food.clear()
    food_shape_list.clear()
    food_cord_list.clear()
    food_create()
    worm_create()
    clock.schedule_interval(one_step, interval)
    new_round_on = 0
    lvl_curr = 1


def next_round():
    global food_numb , lvl_eaten_food ,  food_numb , lvl_curr , mause_click_current
    clock.unschedule(one_step)
    food_numb = food_numb_max - lvl_curr  + 1
    mause_click_current = mause_click_max - 1 * lvl_curr
    lvl_curr += 1
    lvl_eaten_food = 0
    cord_list.clear()
    worm_shape_list.clear()
    food.clear()
    food_shape_list.clear()
    food_cord_list.clear()
    food_create()
    worm_create()
    clock.schedule_interval(one_step, interval)




worm_create()

# ---------------------------------[ control ]---------------------------------
@window.event
def on_draw():
    window.clear()
    bg_batch.draw()
    batch.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global angle, mause_click_current, cord_list
    if button == mouse.LEFT and mause_click_current <= mause_click_max:
        print(f' x {x} y {y}')
        dx = x - cord_list[0][0]
        dy = y - cord_list[0][1]
        angle = math.atan2(dy, dx)
        mause_click_current += 1
        show_info()
    if button == mouse.LEFT and test_zone(x, y, new_round_button) and new_round_on == 1:
        new_round()
    if button == mouse.LEFT and test_zone(x, y, new_game_button):
        new_game()


pyglet.app.run()
