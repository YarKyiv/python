import json

import pyglet
from pyglet.window import mouse

window = pyglet.window.Window(800, 700)

batch = pyglet.graphics.Batch()
batchdown = pyglet.graphics.Batch()
front_batch= pyglet.graphics.Batch()

# ------------------------------------------
# cell=[r, forward, l, back, roof, floor, content]

dungeon_array = []


def load_map():
    global dungeon_array
    with open('dungeon.txt') as f:
        dungeon_array = json.load(f)


def turn(d):
    global curr_view
    curr_view = (curr_view + d + 4) % 4


def clearWalls():
    global walls

    for i in range(len(walls)):
        for j in range(numb_wall):
            # print(f"i={i}, j={j}")
            walls[i][j].x = -410
            walls[i][j].y = -500
            floor_w[i].x = -800
            roof[i].x = -800
            floor_w[i].y = -500
            roof[i].y = -500

    for j in range(numb_wall):
        front_wall_far[j].x = -400
        front_wall_far[j].y = -400
        right_wall_far[j].x = -400
        right_wall_far[j].y = -400
        left_wall_far[j].x = -400
        left_wall_far[j].y = -400


def motion_forward(direct):
    global hero_x, hero_y
    curr_f = dungeon_array[hero_y][hero_x][(1 + curr_view) % 4]  # will be  modified
    curr_b = dungeon_array[hero_y][hero_x][(3 + curr_view) % 4]
    temp_dir = [curr_f, curr_b]

    if temp_dir[direct] == 0:
        if curr_view == 0:  # 0 - nord, 1 - west  2 - south 3 - ost
            hero_y += 1 - 2 * direct
        if curr_view == 1:  # 0 - nord, 1 - west  2 - south 3 - ost
            hero_x -= 1 - 2 * direct
        if curr_view == 2:  # 0 - nord, 1 - west  2 - south 3 - ost
            hero_y -= 1 - 2 * direct
        if curr_view == 3:  # 0 - nord, 1 - west  2 - south 3 - ost
            hero_x += 1 - 2 * direct
    else:
        print("i can’t move")
    print("coord:", hero_x, hero_y, dungeon_array[hero_y][hero_x])


def show_room():   # curr_view   0 - nord, 1 - west  2 - south 3 - ost

    curr_r = dungeon_array[hero_y][hero_x][(0 + curr_view) % 4]
    curr_f = dungeon_array[hero_y][hero_x][(1 + curr_view) % 4]
    curr_l = dungeon_array[hero_y][hero_x][(2 + curr_view) % 4]
    curr_fl = dungeon_array[hero_y][hero_x][4]
    curr_rf = dungeon_array[hero_y][hero_x][5]
    current_side = [curr_r, curr_f, curr_l, curr_fl, curr_rf]

    # дальний прямо пол
    shift_x = curr_view%2*(curr_view-2)
    shift_y = (curr_view+1)%2*(1-curr_view)
    curr_fl_front = dungeon_array[hero_y + shift_y][hero_x + shift_x][4]
    print("far away", curr_fl_front)
    #  справа  пол
    shift_x_R = (curr_view+1)%2 *(1-curr_view)
    shift_y_R = curr_view%2 *(2-curr_view)
    curr_fl_right = dungeon_array[hero_y + shift_y_R][hero_x + shift_x_R][4]

    #  слева  пол
    shift_x_L = (curr_view + 1) % 2 * (curr_view-1)
    shift_y_L = curr_view % 2 * (curr_view-2)
    curr_fl_left = dungeon_array[hero_y + shift_y_L][hero_x + shift_x_L][4]

    clearWalls()
    for i in range(len(walls)):  # r  593,0    f 208,156  l 0,0
        walls[i][current_side[i]].x = 0 + modif[i][0]
        walls[i][current_side[i]].y = 0 + modif[i][1]



    front_wall_far[curr_fl_front].x = 0 + mod_2[1][0]
    front_wall_far[curr_fl_front].y = 0 + mod_2[1][1]

    right_wall_far[curr_fl_right].x = 0 + mod_2[0][0]
    right_wall_far[curr_fl_right].y = 0 + mod_2[0][1]

    left_wall_far[curr_fl_left].x = 0 + mod_2[2][0]
    left_wall_far[curr_fl_left].y = 0 + mod_2[2][1]


def print_label(x, y, curr):
    label_x_y.text = "your x = " + str(int(x)) + "|" "your y = " + str(int(y)) + "|"
    if curr == 0:
        label_curr.text = "N"
    if curr == 1:
        label_curr.text = "W"
    if curr == 2:
        label_curr.text = "S"
    if curr == 3:
        label_curr.text = "O"


load_map()
# cell=[r, forward, l, back, roof, floor, content]


modif = [[600, 0], [200, 150], [0, 0], [0, 0], [0, 450]] # r c l b t cont

mod_2 = [[600, 0], [200, 150], [-800, 0]]   # for other rooms

op1=200 # прозрачность дальних стен и пола  transparency of distant walls and floors


# ------------------------------------------
# hero data
curr_view = 0  # 0 - nord, 1 - west  2 - south 3 - ost
hero_x = 1
hero_y = 0
numb_wall = 6
# ------------------------------------------
left_wall = []  # list of  left walls  sprites
right_wall = []
front_wall = []
floor_w = []
roof = []
front_wall_far = []
right_wall_far = []
left_wall_far = []

walls = [right_wall, front_wall, left_wall, floor_w, roof]

# _________________________________________
# ------------------------------------------ картинки монстров  monsters / content images

content_img_mod_x=[280, 320, 280, 265,190]#  0  сундук chest   1 гоблин goblin   2 мимик mimic  3 орк orc   4 тролль  troll
content_img_mod_y=75
content_quantity=[0,0,0,0,0] # TODO количество монстров  monsters quantity   NOT relized

content_img_name=["240x240px_chest","160x190px_goblin", "240x240px_mimic", "270x350px_orc","420x460px_troll"]
# спрайты монстров

chest_sprite=[]
goblin_sprite=[]
mimic_sprite=[]
orc_sprite=[]
troll_sprite=[]
content_sprite=[chest_sprite,goblin_sprite,mimic_sprite,orc_sprite, troll_sprite]

for m in range(len(content_quantity)):
    for q in range(0,content_quantity[m]):
        print(f"m={m}, q={q} , {content_img_name[m]}{q+1}.png")
        img_content = pyglet.image.load("dragone_png/"+ content_img_name[m] + str(q+1) + ".png")
        content_sprite[m].append(pyglet.sprite.Sprite(img_content, x=content_img_mod_x[m], y=content_img_mod_y, batch=front_batch))




for i in range(numb_wall):
    img_left_wall = pyglet.image.load("dragone_png/wall_l_" + str(int(i)) + ".png")
    left_wall.append(pyglet.sprite.Sprite(img_left_wall, x=-200, y=0, batch=batch))
    img_right_wall = pyglet.image.load("dragone_png/wall_r_" + str(int(i)) + ".png")
    right_wall.append(pyglet.sprite.Sprite(img_right_wall, x=-200, y=0, batch=batch))
    img_c_wall = pyglet.image.load("dragone_png/wall_c_" + str(int(i)) + ".png")
    front_wall.append(pyglet.sprite.Sprite(img_c_wall, x=-400, y=0, batch=batch))

    img_floor = pyglet.image.load("dragone_png/floor_" + str(int(i)) + ".png")
    floor_w.append(pyglet.sprite.Sprite(img_floor, x=-800, y=0, batch=batch))
    img_roof = pyglet.image.load("dragone_png/roof_" + str(int(i)) + ".png")
    roof.append(pyglet.sprite.Sprite(img_roof, x=-800, y=0, batch=batch))

    img_floor_r = pyglet.image.load("dragone_png/r_fl_" + str(i) + ".png")
    right_wall_far.append(pyglet.sprite.Sprite(img_floor_r, x=-1000, y=-150, batch=batchdown))
    right_wall_far[i].opacity=op1
    img_floor_l = pyglet.image.load("dragone_png/l_fl_" + str(i) + ".png")
    left_wall_far.append(pyglet.sprite.Sprite(img_floor_l, x=-1000, y=-150, batch=batchdown))
    left_wall_far[i].opacity=op1
    img_floor_far = pyglet.image.load("dragone_png/small_floor_" + str(i) + ".png")
    front_wall_far.append(pyglet.sprite.Sprite(img_floor_far, x=-800, y=0, batch=batchdown))
    front_wall_far[i].opacity=op1


# ___________________________________________________________________________
label_x_y = pyglet.text.Label('waiting to command',
                              font_name='Arial',
                              font_size=12,
                              x=0, y=700,
                              anchor_x='center', anchor_y='center', batch=batch)
label_curr = pyglet.text.Label('waiting to command',
                               font_name='Arial',
                               font_size=12,
                               x=790, y=700,
                               anchor_x='center', anchor_y='center', batch=batch)

# _______________________________________________________________

show_room()


@window.event
def on_draw():
    window.clear()
    batchdown.draw()
    batch.draw()
    front_batch.draw()
    #for i in range(numb_wall):
       # left_wall[i].draw()
       # right_wall[i].draw()
       # front_wall[i].draw()
       # floor_w[i].draw()
       # roof[i].draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed. x= ' + str(x), "y=", y)


@window.event
def on_key_release(symbol, modifiers):
    print(symbol)
    if symbol == 119:
        print("W")
        motion_forward(0)
    if symbol == 97:
        print("A")
        turn(1)
    if symbol == 115:
        print("s")
        motion_forward(1)
    if symbol == 100:
        print("d")
        turn(-1)
    if symbol == 119 or symbol == 97 or symbol == 115 or symbol == 100:
        show_room()


pyglet.app.run()
