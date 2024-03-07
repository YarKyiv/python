import random

import pyglet
from pyglet import shapes
from pyglet.window import mouse
import math

boom_range_max = 75
boom_range_min = 25


# from pyglet import clock

def callback(dt):
    print(f"{dt} seconds since last callback")


# clock.schedule_interval(callback, 1)


class Ships:
    # area_active
    def __init__(self, name, x, y, hp, armor, shoot_numb, move, velocity, alef, prec, r, burn, hp_bar_x, hp_bar_y,
                 color_boom, sprite_name, lbl_x, boom_numb, area_numb, enemy_no=0):
        self.name = name  # энергия	урон	физ. атака	reload	агро	тип допа	время допа	величина эффекта
        self.x = x + shift_x
        self.y = y + shift_y
        self.x_old = self.x
        self.y_old = self.y
        self.hp = hp
        self.hp_max = hp
        self.armor = armor
        self.armor_max = armor
        self.shoot_numb = shoot_numb
        self.curr_shoot_numb = shoot_numb
        self.move = move  # my ship can move
        self.velocity = velocity
        self.vel_mod = 0
        self.alef = alef
        self.prec = prec  # точность
        self.range = r  # дальность стрельбы
        self.burn = 1
        self.boom_numb = boom_numb
        self.boom_active = 0
        self.area_active = 0
        self.hp_bar_x = hp_bar_x
        self.hp_bar_y = hp_bar_y
        self.area_numb = area_numb
        self.enemy_no = enemy_no
        self.shoot_result = []
        for j in range(self.shoot_numb):
            self.row =[]
            for i in range(enemy_numb):
                self.row.append(0)
            self.shoot_result.append(self.row)  #shoot_result j i     j - номер выстрела   i  номер враж корабля


        self.hp_bar = shapes.Rectangle(x=hp_bar_x, y=hp_bar_y, width=100, height=10, color=(225, 0, 0),
                                       batch=main_batch)
        self.arm_bar = shapes.Rectangle(x=hp_bar_x, y=hp_bar_y - 15, width=100, height=10, color=(0, 0, 255),
                                        batch=main_batch)
        self.hp_bar_back = shapes.Rectangle(x=hp_bar_x, y=hp_bar_y, width=100, height=10, color=(255, 128, 0),
                                            batch=back_batch)
        self.arm_bar_back = shapes.Rectangle(x=hp_bar_x, y=hp_bar_y - 15, width=100, height=10, color=(49, 60, 72),
                                             batch=back_batch)

        self.blust_img = pyglet.image.load("marine/blust.png")
        self.blust_img.anchor_x = self.blust_img.width // 2
        self.blust_img.anchor_y = self.blust_img.height // 2
        self.blust = pyglet.sprite.Sprite(self.blust_img, x=-200, y=-200,
                                          batch=back_batch)

        self.blust.scale = .3

        self.sprite_img = pyglet.image.load(sprite_name)
        self.sprite_img.anchor_x = self.sprite_img.width // 2
        self.sprite_img.anchor_y = self.sprite_img.height // 2

        self.sprite_ship = pyglet.sprite.Sprite(self.sprite_img, x=self.x, y=self.y,
                                                batch=main_batch)
        self.sprite_ship.scale = .4

        self.boom_sprite_list = []
        self.boom_place_list = []
        self.lbl_result = []
        for i in range(self.shoot_numb):
            self.boom_sprite_list.append(
                shapes.Circle(x=-150, y=-150, radius=boom_range_max, color=color_boom, batch=main_batch))
            self.boom_sprite_list[i].opacity = 100
            self.boom_place_list.append([-150, -150])
            if self.enemy_no == -1:
                self.lbl_result.append(pyglet.text.Label(f'shoot{i}:',
                                                         font_name="Arial",
                                                         font_size=14,
                                                         x=lbl_x, y=750 - i * 20,
                                                         anchor_x="left", anchor_y="center", batch=back_batch))  #
            else:
                self.lbl_result.append(pyglet.text.Label(f'shoot{i}:',
                                                         font_name="Arial",
                                                         font_size=14,
                                                         x=lbl_x, y=850 - i * 20 - self.enemy_no * 100,
                                                         anchor_x="left", anchor_y="center", batch=back_batch))

        # тут поставить подключение спрайта корабля

    def show_boom(self):
        print("area_active", self.area_active)
        for i in range(self.shoot_numb):
            self.boom_sprite_list[i].x = self.boom_place_list[i][0]
            self.boom_sprite_list[i].y = self.boom_place_list[i][1]
            self.boom_sprite_list[i].radius = boom_range_max * (1 + .5 * self.area_active)


def get_angle(x, y):
    # global alef
    dx = x - my_ship.x
    dy = y - my_ship.y
    my_ship.alef = math.atan2(dy, dx)


def move_obj():
    # global  my_x, my_y
    my_ship.x = min(max(my_ship.x + (my_ship.velocity + my_ship.vel_mod) * math.cos(my_ship.alef), shift_x),
                    shift_x + marine_w)
    my_ship.y = min(max(my_ship.y + (my_ship.velocity + my_ship.vel_mod) * math.sin(my_ship.alef), shift_y),
                    shift_y + marine_h)
    circle.x = my_ship.x
    circle.y = my_ship.y
    my_ship.sprite_ship.x = my_ship.x
    my_ship.sprite_ship.y = my_ship.y
    my_ship.sprite_ship.rotation = 90 - math.degrees(my_ship.alef)
    # print('my_ship.alef-',90-math.degrees(my_ship.alef))


def action(x, y):
    print('The left mouse button was pressed. x= ' + str(x), "y=", y)
    get_angle(x, y)
    move_obj()


def show_boom(ship):
    ship.show_boom()


def enemy_move(z, es):
    if not z:
        ship_list[es].alef + math.pi - math.pi * (1 / 4 - random.random() / 2)

    if z == 1:
        ship_list[es].alef + math.pi - math.pi * (1 / 2 - random.random())

    if z == 2:
        ship_list[es].alef - math.pi * (1 / 2 - random.random())

    if z == 3:
        ship_list[es].alef - math.pi * (1 / 4 - random.random() / 2)

    ship_list[es].x = min(max(ship_list[es].x + ship_list[es].velocity * math.cos(ship_list[es].alef), shift_x),
                          shift_x + marine_w)
    ship_list[es].y = min(max(ship_list[es].y + ship_list[es].velocity * math.sin(ship_list[es].alef), shift_y),
                          shift_y + marine_h)
    enemy_circle.x = ship_list[es].x
    enemy_circle.y = ship_list[es].y
    ship_list[es].sprite_ship.x = ship_list[es].x
    ship_list[es].sprite_ship.y = ship_list[es].y
    ship_list[es].sprite_ship.rotation = math.degrees(ship_list[es].alef)


def burning():
    my_ship.vel_mod = my_ship.velocity
    my_ship.burn = 0
    label_burn.text = str(my_ship.burn)
    burn_button.opacity = 128


def heavy_boom():
    my_ship.boom_numb -= 1
    label_boom.text = str(my_ship.boom_numb)
    my_ship.boom_active = 1
    boom_button.opacity = 128


# large_area

def large_area():
    my_ship.area_numb -= 1
    label_area.text = str(my_ship.area_numb)
    my_ship.area_active = 1
    area_button.opacity = 128


def enemy_shoot(z, es):
    print("z=", z)
    target_points = []
    for i in range(6):
        target_points.append(ship_list[es].alef - math.pi / 3 + i * math.pi / 3)
        print(f" углы обстрела {math.degrees(target_points[i])}")

    if not z:
        for i in range(ship_list[es].shoot_numb):
            ship_list[es].boom_place_list[i][0] = min(
                max(my_ship.x_old + my_ship.velocity * math.cos(target_points[i % 3]), shift_x), shift_x + marine_w)
            ship_list[es].boom_place_list[i][1] = min(
                max(my_ship.y_old + my_ship.velocity * math.sin(target_points[i % 3]), shift_y), shift_y + marine_h)

    if z == 1:
        for i in range(enemy_ship.shoot_numb):

            if random.random() < 0.5:

                ship_list[es].boom_place_list[i][0] = min(
                    max(my_ship.x_old + my_ship.velocity * math.cos(target_points[i % 3]), shift_x), shift_x + marine_w)
                ship_list[es].boom_place_list[i][1] = min(
                    max(my_ship.y_old + my_ship.velocity * math.sin(target_points[i % 3]), shift_y), shift_y + marine_h)
            else:
                ship_list[es].boom_place_list[i][0] = min(
                    max(my_ship.x_old + my_ship.velocity * math.cos(target_points[i % 6]), shift_x), shift_x + marine_w)
                ship_list[es].boom_place_list[i][1] = min(
                    max(my_ship.y_old + my_ship.velocity * math.sin(target_points[i % 6]), shift_y), shift_y + marine_h)
    if z == 2:
        for i in range(ship_list[es].shoot_numb):
            if random.random() < 0.5:

                ship_list[es].boom_place_list[i][0] = min(
                    max(my_ship.x_old + my_ship.velocity * math.cos(target_points[3 + i % 3]), shift_x),
                    shift_x + marine_w)
                ship_list[es].boom_place_list[i][1] = min(
                    max(my_ship.y_old + my_ship.velocity * math.sin(target_points[3 + i % 3]), shift_y),
                    shift_y + marine_h)
            else:
                ship_list[es].boom_place_list[i][0] = min(
                    max(my_ship.x_old + my_ship.velocity * math.cos(target_points[i % 6]), shift_x), shift_x + marine_w)
                ship_list[es].boom_place_list[i][1] = min(
                    max(my_ship.y_old + my_ship.velocity * math.sin(target_points[i % 6]), shift_y), shift_y + marine_h)
    if z == 3:
        for i in range(ship_list[es].shoot_numb):
            ship_list[es].boom_place_list[i][0] = min(
                max(my_ship.x_old + my_ship.velocity * math.cos(target_points[3 + i % 3]), shift_x), shift_x + marine_w)
            ship_list[es].boom_place_list[i][1] = min(
                max(my_ship.y_old + my_ship.velocity * math.sin(target_points[3 + i % 3]), shift_y), shift_y + marine_h)
    for p in range(ship_list[es].shoot_numb):
        print(ship_list[es].boom_place_list[p][0], ship_list[es].boom_place_list[p][1])

    show_boom(ship_list[es])


def enemy_step():
    for i in range(1, len(ship_list)):
        if ship_list[i].hp > 0:
            dx = ship_list[i].x - my_ship.x_old
            dy = ship_list[i].y - my_ship.y_old
            ship_list[i].alef = math.atan2(dy, dx) - math.pi  # - math.pi*(1/2-random.random())
            distance = (dx ** 2 + dy ** 2) ** .5
            # enemy_ship.alef=random.random()*math.pi*2

            if distance <= my_ship.velocity:
                enemy_move(0, i)
                enemy_shoot(0, i)

            if my_ship.velocity < distance < ship_list[i].range / 2:
                enemy_move(1, i)
                enemy_shoot(1, i)

            if ship_list[i].range / 2 <= distance < ship_list[i].range * .9:
                enemy_move(2, i)
                enemy_shoot(2, i)

            if ship_list[i].range * .9 <= distance <= ship_list[i].range:
                enemy_move(3, i)
                enemy_shoot(3, i)


def dmg_u(a, d):
    for i in range(a.shoot_numb):
        curr_damage = 0
        xd = ((a.boom_place_list[i][0] - d.x) ** 2 + (
                a.boom_place_list[i][1] - d.y) ** 2) ** 0.5
        range_min_t = boom_range_min * (1 + 0.5 * my_ship.area_active)
        range_max_t = boom_range_max * (1 + 0.5 * my_ship.area_active)
        if xd <= range_min_t:
            curr_damage = damage_max
        if range_min_t < xd <= range_max_t / 2:
            curr_damage = (damage_max - damage_min)
        if range_max_t / 2 < xd <= range_max_t:
            curr_damage = damage_min

        curr_damage = curr_damage * (1 + 1 * my_ship.boom_active)
        if a.name == "hero" and d.name != "hero":
            a.shoot_result[i][d.enemy_no]=curr_damage   #shoot_result j i     j - номер выстрела   i  номер враж корабля
        if a == d:
            a.lbl_result[i].text += f'| {curr_damage} '  # shoot{i}
        else:
            a.lbl_result[i].text = f'shoot{i}:{curr_damage} |'  #

        d.armor -= curr_damage
        if d.armor <= 0:
            d.hp += d.armor
            d.armor = 0
        print(f" enemy hp ={d.hp}, enemy armor={d.armor} | damage = {curr_damage} boom No = {i}")
        d.hp_bar.width = max(0, 100 * d.hp / d.hp_max)
        d.arm_bar.width = max(0, 100 * d.armor / d.armor_max)


def set_damage():
    # global enemy_hp, enemy_armor
    dmg_u(my_ship, my_ship)
    for i in range(1, len(ship_list)):
        dmg_u(my_ship, ship_list[i])
        dmg_u(ship_list[i], my_ship)
        for j in range(1, len(ship_list)):
            dmg_u(ship_list[i], ship_list[j])

    for i in ship_list:
        if i.hp <= 0:
            i.blust.x = i.x
            i.blust.y = i.y
            i.sprite_ship.opacity = 0


def clear_status():
    global counter_round
    # shoot_result j i     j - номер выстрела   i  номер враж корабля
    for j in range(my_ship.shoot_numb):
        res_str=""
        for i in range(enemy_numb):
            res_str+= str(my_ship.shoot_result[j][i]) +" | "
        my_ship.lbl_result[j].text=res_str


    my_ship.x_old = my_ship.x
    my_ship.y_old = my_ship.y
    my_ship.move = 1
    my_ship.curr_shoot_numb = my_ship.shoot_numb
    for i in range(my_ship.shoot_numb):
        my_ship.boom_place_list[i] = [-150, -150]
        my_ship.boom_sprite_list[i].x = my_ship.boom_place_list[i][0]
        my_ship.boom_sprite_list[i].y = my_ship.boom_place_list[i][1]
    counter_round += 1
    label_round.text = f"r: {counter_round}"
    my_ship.burn = min(5, my_ship.burn + 1)
    label_burn.text = str(my_ship.burn)

    my_ship.boom_active = 0
    boom_button.opacity = 255
    my_ship.area_active = 0
    area_button.opacity = 255

    my_ship.vel_mod = 0
    if my_ship.burn >= 5:
        burn_button.opacity = 255

    if my_ship.boom_numb == 0:
        boom_button.opacity = 128

    for j in  range(my_ship.shoot_numb): #shoot_result j i     j - номер выстрела   i  номер враж корабля
        for i in range(enemy_numb):
            my_ship.shoot_result[j][i] = 0


def test_next_round():
    if not my_ship.move and not my_ship.curr_shoot_numb:
        enemy_step()
        set_damage()
        clear_status()


def test_in_zone(x, y, n):  # x1 y1 x2 y2
    x1 = zone_list[n][0]
    x2 = zone_list[n][2]
    y1 = zone_list[n][1]
    y2 = zone_list[n][3]
    if x1 <= x <= x2 and y1 <= y <= y2:
        return True
    else:
        return False


window = pyglet.window.Window(1600, 900)

back_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()
front_batch = pyglet.graphics.Batch()

counter_round = 0
shift_x = 350
shift_y = 0
marine_w = 900
marine_h = 900

burn_x = 20
burn_y = 755

boom_x = 110
boom_y = 760

area_x = 200
area_y = 760

# ship creating
enemy_numb = 2

my_ship = Ships("hero", 50, 50, 100, 100, 3, 1, 100, 0, 5, 800, 5, 20, 880, (255, 50, 255), "marine/smallorange.png",
                20, 5, 5, -1)
enemy_ship = Ships("enemy", 850, 850, 100, 100, 3, 1, 100, 0, 5, 800, 3, shift_x + marine_w + 20, 880, (0, 50, 255),
                   "marine/alien4.png", 1270, 5, 5, 0)
enemy_ship2 = Ships("enemy", 850, 650, 100, 100, 3, 1, 100, 0, 5, 800, 3, shift_x + marine_w + 20, 780, (0, 50, 255),
                    "marine/alien4.png", 1270, 5, 5, 1)
ship_list = [my_ship, enemy_ship, enemy_ship2]
# ship_param=[my_hp, my_armor, shoot_numb, curr_shoot_numb, velocity, alef prec, r, burn, hp_bar_x, hp_bar_y,
#                  color_boom, sprite_name, lbl_x]

enemy_boom_place_list = []
for i in range(enemy_ship.shoot_numb):
    enemy_boom_place_list.append([-150, -150])

boom_place_list = []
for i in range(my_ship.shoot_numb):
    boom_place_list.append([-150, -150])

boom_sprite_list = []
# [-150, -150]
enemy_boom_sprite_list = []

# boom param
damage_max = 30
damage_min = 10
boom_range_max = 75
boom_range_min = 25

sea = [shift_x, shift_y, shift_x + marine_w, shift_y + marine_h]
button_burn = [burn_x, burn_y, burn_x + 1024 / 20, burn_y + 1024 / 20]
button_boom = [boom_x, boom_y, boom_x + 800 / 20, boom_y + 800 / 20]
button_area = [area_x, area_y, area_x + 800 / 20, area_y + 800 / 20]
zone_list = [sea, button_burn, button_boom, button_area]

circle = shapes.Circle(x=my_ship.x, y=my_ship.y, radius=10, color=(50, 225, 30), batch=main_batch)
circle.opacity = 0

enemy_circle = shapes.Circle(x=enemy_ship.x, y=enemy_ship.y, radius=10, color=(255, 50, 30), batch=main_batch)
enemy_circle.opacity = 0

lbl_result = []
lbl_result_en = []

label_shoot_numb = pyglet.text.Label(str(my_ship.curr_shoot_numb),
                                     font_name="Arial",
                                     font_size=20,
                                     x=20, y=850,
                                     anchor_x="left", anchor_y="center", batch=back_batch)

label_distance = pyglet.text.Label("0",
                                   font_name="Arial",
                                   font_size=20,
                                   x=20, y=820,
                                   anchor_x="left", anchor_y="center", batch=back_batch)
label_round = pyglet.text.Label("r:0",
                                font_name="Arial",
                                font_size=20,
                                x=800, y=870,
                                anchor_x="center", anchor_y="top", batch=front_batch, color=(0, 0, 0, 255))

label_burn = pyglet.text.Label("5",
                               font_name="Arial",
                               font_size=20,
                               x=burn_x + 60, y=burn_y,
                               anchor_x="left", anchor_y="bottom", batch=front_batch, color=(255, 255, 255, 255))

label_boom = pyglet.text.Label("5",
                               font_name="Arial",
                               font_size=20,
                               x=boom_x + 60, y=boom_y - 5,
                               anchor_x="left", anchor_y="bottom", batch=front_batch, color=(255, 255, 255, 255))

label_area = pyglet.text.Label("5",
                               font_name="Arial",
                               font_size=20,
                               x=area_x + 60, y=area_y - 5,
                               anchor_x="left", anchor_y="bottom", batch=front_batch, color=(255, 255, 255, 255))

water_back = pyglet.sprite.Sprite(pyglet.image.load("marine/900_back_marine.png"), x=shift_x, y=shift_y,
                                  batch=back_batch)

burn_button = pyglet.sprite.Sprite(pyglet.image.load("marine/burn.png"), x=burn_x, y=burn_y,
                                   batch=back_batch)
burn_button.scale =1 # .05

boom_button = pyglet.sprite.Sprite(pyglet.image.load("marine/boom.png"), x=boom_x, y=boom_y,
                                   batch=back_batch)
boom_button.scale = .05

area_button = pyglet.sprite.Sprite(pyglet.image.load("marine/area.png"), x=area_x, y=area_y,
                                   batch=back_batch)
area_button.scale = .05

round_back = shapes.Rectangle(x=label_round.x - 20, y=label_round.y - 33, width=50, height=34, color=(225, 225, 225),
                              batch=main_batch)
round_back.opacity = 175


@window.event
def on_draw():
    window.clear()
    # label1.draw()
    circle.draw()
    back_batch.draw()
    main_batch.draw()
    front_batch.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    if test_in_zone(x, y, 0):
        dx = my_ship.x - x
        dy = my_ship.y - y
        d = (dx ** 2 + dy ** 2) ** 0.5
        label_distance.text = str(int(d))
        if d > my_ship.range:
            label_distance.color = (255, 0, 0, 255)
        else:
            label_distance.color = (255, 255, 255, 255)


@window.event
def on_mouse_press(x, y, button, modifiers):
    # global velocity, my_move, curr_shoot_numb
    if button == mouse.LEFT and test_in_zone(x, y,
                                             2) and my_ship.boom_numb and not my_ship.boom_active:  # and my_ship.burn >= 5

        print("go to heavy_boom()")
        heavy_boom()

    if button == mouse.LEFT and test_in_zone(x, y, 1):  # and my_ship.burn >= 5
        print("go to burning()")
        burning()

    if button == mouse.LEFT and test_in_zone(x, y,
                                             3) and my_ship.area_numb and not my_ship.area_active:  # and my_ship.area >= 5
        print("go to area()")
        large_area()

    if button == mouse.LEFT and my_ship.move and test_in_zone(x, y, 0) and my_ship.hp > 0:
        my_ship.move = 0
        action(x, y)
        test_next_round()

    if button == mouse.RIGHT and my_ship.curr_shoot_numb and my_ship.hp > 0:
        dx = my_ship.x - x
        dy = my_ship.y - y
        d = (dx ** 2 + dy ** 2) ** 0.5
        if d <= my_ship.range and test_in_zone(x, y, 0):
            my_ship.curr_shoot_numb -= 1
            label_shoot_numb.text = str(my_ship.curr_shoot_numb)
            d = ((x - my_ship.x) ** 2 + (y - my_ship.y) ** 2) ** 0.5
            x_shift = int(my_ship.prec * d / 100)
            y_shift = int(my_ship.prec * d / 100)
            my_ship.boom_place_list[my_ship.curr_shoot_numb][0] = x - x_shift + random.randint(0,
                                                                                               x_shift) + random.randint(
                0,
                x_shift)
            my_ship.boom_place_list[my_ship.curr_shoot_numb][1] = y - y_shift + random.randint(0,
                                                                                               y_shift) + random.randint(
                0,
                y_shift)
            show_boom(my_ship)
            test_next_round()


pyglet.app.run()
