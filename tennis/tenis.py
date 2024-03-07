import math

import pyglet
from pyglet import clock
from pyglet import shapes

########################### cnfg ##################################

win_x = 800
win_y = 600

angle = [0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi]  # 0-0, 1-90, 2-180, 3-270, 4-360
angle_2 = [math.pi / 12, math.pi / 6, math.pi / 4, math.pi * 2 / 3, math.pi * 5 / 12]  # 15° 30° 45° 60° 75°

text_size = 40
text_y = win_y - text_size - 10
text_x_p = win_x / 2 - win_x / 10
text_x_c = win_x / 2 + win_x / 10

player_y = win_y / 2
player_x = 10
comp_y = win_y / 2
comp_x = 780
racket_speed = 10
racket_with = 10
racket_high = 50

comp_error = int(racket_high / 2)
ball_speed = 10
ball_angle = 3 * math.pi / 2 - 0.2
ball_x = win_x / 2
ball_y = win_y / 2
ball_rad = 15
left_border = player_x + racket_with + ball_rad + 5
right_border = comp_x - ball_rad - 5

win_cond = 2

score = [0, 0]


########################### logical ##################################

def set_pl_y(y):
    global player_y
    player_y = y


def set_comp_y():
    global comp_y
    comp_y = ball_y - comp_error  # + random.randint(-comp_error, comp_error)


def ball_move():
    d_x = ball_speed * math.cos(ball_angle)
    d_y = ball_speed * math.sin(ball_angle)
    return [d_x, d_y]


def ball_cal(dc):  # 0-0, 1-90, 2-180, 3-270, 4-360
    global ball_angle, player_y
    new_x = ball_x + dc[0]
    new_y = ball_y + dc[1]
    if new_y >= win_y - ball_rad:
        if angle[0] < ball_angle < angle[1]:
            ball_angle = angle[4] - ball_angle
            # print(ball_angle)
        if angle[1] < ball_angle < angle[2]:
            ball_angle = angle[4] - ball_angle
            # print(ball_angle)
    if new_y <= 0 + ball_rad:
        if angle[3] < ball_angle < angle[4]:
            ball_angle = angle[4] - ball_angle
            # print(ball_angle)
        if angle[2] < ball_angle < angle[3]:
            ball_angle = angle[4] - ball_angle
            # print(ball_angle)
    d_y = (player_y - new_y + racket_high / 2)
    if left_border - 15 <= new_x <= left_border and abs(d_y) < (racket_high + ball_rad) / 2:
        # print("dy=", d_y, "ball_angle", ball_angle)
        if angle[2] < ball_angle < angle[3]:  # 15° 30° 45° 60° 75°
            ball_angle = angle[4] - ball_angle
        if angle[1] < ball_angle < angle[2]:
            ball_angle = angle[2] - ball_angle
            # ball_angle = angle[2]-ball_angle
        ball_angle -= (angle_2[4] * d_y / racket_high / 2) % angle[4]
        if ball_angle < 0: ball_angle = angle[4] + ball_angle
        # print(ball_angle, math.degrees(angle_2[4] * d_y / racket_high / 2))

    d_y = (comp_y - new_y + racket_high / 2)
    if right_border <= new_x <= right_border + 15 and abs(d_y) < (racket_high + ball_rad) / 2:
        print('right-')
        if ball_angle > angle[4] or ball_angle < angle[0]:
            print('EXTRA ANGLE', ball_angle)
        # print("dy=", d_y, "ball_angle", math.degrees(ball_angle))
        if angle[0] <= ball_angle <= angle[1]:  # 15° 30° 45° 60° 75°
            ball_angle = angle[2] - ball_angle
        if angle[3] <= ball_angle <= angle[4]:
            ball_angle = angle[2] + angle[4] - ball_angle
            # ball_angle = angle[2]-ball_angle
        ball_angle -= angle_2[4] * d_y / racket_high / 2
        if ball_angle < 0: ball_angle = angle[4] + ball_angle
        # print(math.degrees(ball_angle), math.degrees(angle_2[4] * d_y / racket_high / 2))


########################### graph #################################


window = pyglet.window.Window(win_x, win_y)

back_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()

racket_p = shapes.Rectangle(10, player_y, racket_with, racket_high, color=(0, 255, 0),
                            batch=main_batch)
racket_c = shapes.Rectangle(780, player_y, racket_with, racket_high, color=(255, 0, 0),
                            batch=main_batch)

ball = shapes.Circle(ball_x, ball_y, ball_rad, color=(255, 225, 255), batch=main_batch)

lbl_result = []
lbl_result.append(
    pyglet.text.Label('0', font_name="Arial", font_size=text_size, x=text_x_p, y=text_y, anchor_x="left",
                      anchor_y="center",
                      batch=main_batch, color=(0, 255, 0, 255)))
lbl_result.append(
    pyglet.text.Label('0', font_name="Arial", font_size=text_size, x=text_x_c, y=text_y, anchor_x="left",
                      anchor_y="center",
                      batch=main_batch, color=(255, 0, 0, 255)))
lbl_result.append(
    pyglet.text.Label('', font_name="Arial", font_size=text_size, x=win_x / 2, y=win_y / 2, anchor_x="center",
                      anchor_y="center",
                      batch=main_batch, color=(255, 0, 0, 255)))


# back_sprite = pyglet.sprite.Sprite(pyglet.image.load("tenis/bg800x600.png"), x=0, y=0, batch=back_batch)

def show_pl():
    racket_p.y = player_y


def show_lbl():
    lbl_result[0].text = str(score[0])
    lbl_result[1].text = str(score[1])


def show_ball():
    ball.y = ball_y
    ball.x = ball_x


def show_racket():
    racket_c.y = comp_y


def set_goal(n):
    score[n] += 1
    print('goal player data', player_y + racket_high / 2, ball_y)
    print('goal. Comp data ', comp_y + racket_high / 2, ball_y)


def end_game():
    global ball_x
    clock.unschedule(one_step)
    ball_x = 1000
    show_ball()
    lbl_result[2].text = str(['player', 'comp'][score[0] < score[1]]) + ' win'


def goal_chek():
    if win_x < ball_x:
        set_goal(0)
        return True
    if ball_x < 0:
        set_goal(1)
        return True
    return False


def new_raund():
    global ball_x, ball_y, ball_angle
    ball_x = win_x / 2
    ball_y = win_y / 2
    ball_angle = (ball_angle + math.pi) % (math.pi * 2)


def one_step(t):
    global ball_x, ball_y
    # racket_p_move()
    d_coord = ball_move()
    ball_cal(d_coord)
    ball_x += d_coord[0]
    ball_y += d_coord[1]
    show_ball()
    set_comp_y()
    show_racket()
    show_pl()
    if goal_chek():
        show_lbl()
        new_raund()
        if max(score) >= win_cond:
            end_game()

    # racket_c_move()


clock.schedule_interval(one_step, 0.02)


@window.event
def on_draw():
    window.clear()
    back_batch.draw()
    main_batch.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    set_pl_y(y)


##################################################################
pyglet.app.run()
