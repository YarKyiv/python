import json

import pyglet
from pyglet import shapes
from pyglet.window import mouse

window = pyglet.window.Window(900, 600)


def test_shape(x, y):
    global selected_wall
    if bar_selected == 0:
        for i in range(11):
            for j in range(10):
                if test_zone(hor_zone[i][j], x, y):
                    horizontal_shape_list[i][j].color = selector_color_list[selected_wall]
                    print(f"colored horizontal! at x={j} y={i} in{selector_color_list[selected_wall]}")
                    hor_data[i][j] = selected_wall
                    return
        for i in range(10):
            for j in range(11):
                if test_zone(vert_zone[i][j], x, y):
                    vertical_shape_list[i][j].color = selector_color_list[selected_wall]
                    print(f"colored vertical! at x={j} y={i} in{selector_color_list[selected_wall]}")
                    vert_data[i][j] = selected_wall
                    return


def test_zone(a, x, y):
    return True if a[0] < x < a[2] and a[1] < y < a[3] else False


def load_map():
    print("attempt loading")
    with open('dungeon.txt') as f:
        d = json.load(f)
    # floor_data[i][j][bar_selected-1]
    # hor_data[i][j]
    # vert_data[i][j]
    print("loaded dungeon.txt")
    print(d)
    for i in range(10):
        for j in range(10):
            cells = d[i][j]  # [0, 0, 0, 0, 0, 0, 0]  r t l b floor roof content
            floor_data[i][j][0] = cells[4]
            floor_data[i][j][1] = cells[5]
            hor_data[i][j] = cells[3]
            hor_data[i + 1][j] = cells[1]
            horizontal_shape_list[i][j].color = selector_color_list[cells[3]]
            horizontal_shape_list[i + 1][j].color = selector_color_list[cells[1]]
            vert_data[i][j] = cells[2]
            vert_data[i][j + 1] = cells[0]
            vertical_shape_list[i][j].color = selector_color_list[cells[2]]
            vertical_shape_list[i][j + 1].color = selector_color_list[cells[0]]


def save_map():
    d = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append([0, 0, 0, 0, 0, 0, 0])
        d.append(row)
    for i in range(11):
        for j in range(10):
            c = hor_data[i][j]
            if 0 < i < 10:
                d[i - 1][j][1] = c
                d[i][j][3] = c
            if i == 0:
                d[i][j][3] = c
            if i == 10:
                d[i - 1][j][1] = c
    for i in range(10):
        for j in range(11):
            c = vert_data[i][j]
            if 0 < j < 10:
                d[i][j - 1][0] = c
                d[i][j][2] = c
            if j == 0:
                d[i][j][2] = c
            if j == 10:
                d[i][j - 1][0] = c

    for i in range(10):   # cell=[r, forward, l, back, roof, floor, content]  |  floor_data = []  # 0- потолки roof 1-floor 2 - content
        for j in range(10):
            d[i][j][4] = floor_data[i][j][0]
            d[i][j][5] = floor_data[i][j][1]

    print("saving d in dungeon.txt")
    f = open('dungeon.txt', 'w')
    json.dump(d, f)
    f.close()


def set_roof_flor(c):  # 0 - walls  1- потолки roof 2-floor    3-  content / bar_selected
    global cur_floors_roof
    for i in range(10):
        for j in range(10):

            floors_shapes[i][j].color = selector_color_list[floor_data[i][j][c - 1]]

    # button_fr_list[cur_floors_roof].opacity = 255
    # button_fr_list[1 - cur_floors_roof].opacity = 128


def test_floor(x, y):
    global cur_floors_roof
    if bar_selected:
        for i in range(10):
            for j in range(10):
                if test_zone(floor_zone[i][j], x, y):
                    floors_shapes[i][j].color = selector_color_list[selected_wall]
                    floor_data[i][j][bar_selected - 1] = selected_wall
                    return


def set_menu_bar(m):
    for i in bar_sprites:
        i.opacity = 0
    bar_sprites[m].opacity = 255
    for i in range(menu_tabs):
        for j in sprites_list[i]:
            j.opacity = 0
    print("bar_selected  in set_menu_bar =", bar_selected)
    sprites_list[bar_selected][selected_wall].opacity = 255


def set_label(v):
    print("bar selected= "+str(v))
    lbl_txt=["SET WALL", "SET ROOF", "SET FLOOR", "SET CONTENT"]
    label_floor_roof.text = lbl_txt[v]
    print(v)



def click_analysis(x, y):
    global selected_wall, cur_floors_roof, bar_selected

    if test_zone(zone_list[0], x, y):  #
        print("click in map")
        test_shape(x, y)
        test_floor(x, y)

    for i in range(menu_tabs):

        if test_zone(menu_bar_zone[i], x, y):
            print("click on bar"+str(i))
            bar_selected = i
            set_label(i)
            set_menu_bar(i)
            if bar_selected:
                set_roof_flor(bar_selected)

    s = -1
    for i in selector_zone:
        s += 1
        if test_zone(i, x, y):
            selected_wall = s
            arrow_wall.y = y_arrow - (selected_wall) * 50 + 10
            for j in sprites_list[bar_selected]:
                j.opacity = 0
            sprites_list[bar_selected][selected_wall].opacity = 255

            print(arrow_wall.y)
    if test_zone(service_zone_list[0], x, y):
        save_map()
    if test_zone(service_zone_list[1], x, y):
        load_map()


# ___________________________________________________________________________

bar_selected = 0  # 0- wall  1 - roof   2 floor
dx_map = 20
dy_map = 20
main_map = [dx_map - 5, dy_map - 5, dx_map + 400 + 5, dy_map + 400 + 5]
zone_list = [main_map]

# _____________________________________________________________


# __________________________________________


# ______________________________________

batch = pyglet.graphics.Batch()
batchdown = pyglet.graphics.Batch()
horizontal_shape_list = []
vertical_shape_list = []

vert_zone = []
hor_zone = []
vert_data = []
hor_data = []

selector_shape_list = []
selector_color_list = [(255, 255, 255), (255, 0, 0), (80, 80, 80), (200, 80, 80), (180, 180, 180), (255, 128, 200)]
selected_wall = 0

selector_zone = []
wall_preview_list = []

floors_shapes = []
bar_sprites = []

floor_data = []  # 0- потолки roof 1-floor

cur_floors_roof = 0  # 0- потолки roof 1-floor

service_zone_list = []
service_sprite_list = []
service_img_name = ["save", "load"]
roof_srites_list = []
floor_srites_list = []
cont_sprite_list=[]

x_arrow = 480
y_arrow = 305

menu_bar_zone = []

menu_tabs=4

# 0 пусто   1  сундук   2 гоблин   3 мимик  4 орк   5 тролль
# menu bar
for i in range(menu_tabs):
    bar_sprites.append(pyglet.sprite.Sprite(pyglet.image.load(f"editor/panel{i}.png"), x=450, y=-150, batch=batchdown))
    menu_bar_zone.append([450 + 100 * i, 350, 550 + 100 * i, 416])

for i in range(6):
    selector_shape_list.append(
        shapes.Rectangle(500, 50 + 50 * (5 - i), 70, 30, color=selector_color_list[i], batch=batch))
    # selector_shape_list[i].z = i
    selector_zone.append([500, 50 + 50 * (5 - i), 570, 50 + 50 * (5 - i) + 30])
    wall_preview = pyglet.image.load("editor/wall_c_" + str(i) + ".png")
    wall_preview_list.append(pyglet.sprite.Sprite(wall_preview, x=580, y=200))
    wall_preview_list[i].scale = 0.4
    roof_srites_list.append(pyglet.sprite.Sprite(pyglet.image.load(f"editor/fr_{i}.png"), x=580, y=180, batch=batch))
    floor_srites_list.append(pyglet.sprite.Sprite(pyglet.image.load(f"editor/fr_{i}.png"), x=580, y=180, batch=batch))
    cont_sprite_list.append(pyglet.sprite.Sprite(pyglet.image.load(f"editor/cont_{i}.png"), x=580, y=140, batch=batch))

sprites_list = [wall_preview_list, roof_srites_list, floor_srites_list, cont_sprite_list]
arrow_wall = shapes.Circle(x_arrow, 315, 10, segments=None, color=(255, 255, 255), batch=batch)

label_walls = pyglet.text.Label("WALLS",
                                font_name="Arial",
                                font_size=15,
                                x=500, y=400,
                                anchor_x="center", anchor_y="center", batch=batch)

label_roof = pyglet.text.Label("ROOF",
                               font_name="Arial",
                               font_size=15,
                               x=600, y=400,
                               anchor_x="center", anchor_y="center", batch=batch)

label_floor = pyglet.text.Label("FLOOR",
                                font_name="Arial",
                                font_size=15,
                                x=700, y=400,
                                anchor_x="center", anchor_y="center", batch=batch)

label_cont = pyglet.text.Label("CONT",
                                font_name="Arial",
                                font_size=15,
                                x=800, y=400,
                                anchor_x="center", anchor_y="center", batch=batch)

label_floor_roof = pyglet.text.Label("...",
                                     font_name="Arial",
                                     font_size=20,
                                     x=300, y=450,
                                     anchor_x="center", anchor_y="center", batch=batch)

# image_floor_button = pyglet.image.load("editor/Floor_wath.png")
# image_roof_button = pyglet.image.load("editor/Roof_wath.png")
# floor_button = pyglet.sprite.Sprite(image_floor_button, x=0, y=550)
# roof_button = pyglet.sprite.Sprite(image_roof_button, x=200, y=550)


# button_fr_list = [roof_button, floor_button]

floor_zone = []

for i in range(2):
    service_sprite_list.append(
        pyglet.sprite.Sprite(pyglet.image.load("editor/" + service_img_name[i] + ".png"), x=dx_map, y=500 - i * 50))
    service_zone_list.append([dx_map, 500 - i * 50, dx_map + 160, 500 - i * 50 + 46])

for i in range(10):
    floor_row = []
    floor_row_data = []
    floor_z_row = []
    for j in range(10):
        x1 = 7 + j * 40 + dx_map
        y1 = 7 + i * 40 + dy_map
        dx = 26
        dy = 26
        x2 = x1 + dx
        y2 = y1 + dy
        floor_row.append(
            shapes.Rectangle(x1, y1, dx, dy, color=(255, 255, 255), batch=batch))
        floor_row_data.append([0, 0,0])  # 0- потолки roof 1-floor  2 - content
        floor_z_row.append([x1, y1, x2, y2])
    floors_shapes.append(floor_row)
    floor_data.append(floor_row_data)
    floor_zone.append(floor_z_row)

for i in range(11):
    row = []
    row_z = []
    row_d = []
    for j in range(10):
        x1 = 10 + j * 40 + dx_map
        y1 = -5 + i * 40 + dy_map
        x2 = x1 + 20
        y2 = y1 + 10
        row.append(
            shapes.Rectangle(x1, y1, 20, 10, color=(255, 255, 255), batch=batch))
        row_z.append([x1, y1 - 5, x2, y2 + 5])
        row_d.append(0)
    horizontal_shape_list.append(row)
    hor_zone.append(row_z)
    hor_data.append(row_d)

for i in range(10):
    row = []
    row_z = []
    row_d = []
    for j in range(11):
        x1 = -5 + j * 40 + dx_map
        y1 = 10 + i * 40 + dy_map
        x2 = x1 + 10
        y2 = y1 + 20
        row.append(
            shapes.Rectangle(x1, y1, 10, 20, color=(255, 255, 255), batch=batch))
        row_z.append([x1 - 5, y1, x2 + 5, y2])
        row_d.append(0)
    vertical_shape_list.append(row)
    vert_zone.append(row_z)
    vert_data.append(row_d)

# horezontal_shape_list[3][5].color = (255, 0, 0)
all_shape_list = [horizontal_shape_list, vertical_shape_list]

set_menu_bar(0)


# ______________________________________________-


@window.event
def on_draw():
    window.clear()
    # image.blit(0, 0)
    # floor_button.draw()
    # roof_button.draw()
    # sprite_arrow.draw()
    batchdown.draw()
    batch.draw()

    for i in wall_preview_list:
        i.draw()
    for i in service_sprite_list:
        i.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed. x= ' + str(x), "y=", y)
        click_analysis(x, y)


@window.event
def on_key_release(symbol, modifiers):
    print(symbol)


pyglet.app.run()
