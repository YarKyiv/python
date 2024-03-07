import pyglet
from pyglet import shapes


# logig_____________________________

def step_color(s, e):
    return int((s - e) / rec_num)


def new_color_set():
    global step_list

    step_list.append(step_color(start_color[0], end_color[0]))
    step_list.append(step_color(start_color[1], end_color[1]))
    step_list.append(step_color(start_color[2], end_color[2]))


# variables___________________________
rec_num = 12  # количество ходов к цвету
rec_high = 25
rec_with = 100
window_x = rec_with * 4
window_y = rec_num * rec_high + 20
start_color = []
end_color = []
rec_list = []
step_list = []  # 0-шаг по r 1-шаг по g 2-шаг по b
print_list = ["r", "g", "b"]

# control __________________________________
for i in range(3):
    start_color.append(int(input("input " + print_list[i] + " in GRB for 1st color")))
print(start_color)
for i in range(3):
    end_color.append(int(input("input " + print_list[i] + " in GRB for 2nd color")))
print(end_color)


def set_rec():
    global rec_list
    new_color_set()
    for i in rec_list:
        start_color[0] -= step_list[0]
        start_color[1] -= step_list[1]
        start_color[2] -= step_list[2]
        i.color = (start_color[0], start_color[1], start_color[2])
        print(i.color)


# 255, 92, 254
# 152, 224, 174
# graphic __________________________________
window = pyglet.window.Window(window_x, window_y)
batch = pyglet.graphics.Batch()
for i in range(rec_num + 1):
    rec_list.append(shapes.Rectangle(window_x / 2 - rec_with / 2, window_y - rec_high * i, rec_with, rec_high,
                                     color=(100, 100, 100), batch=batch))
set_rec()


@window.event
def on_draw():
    window.clear()
    batch.draw()


##################################################################
pyglet.app.run()
