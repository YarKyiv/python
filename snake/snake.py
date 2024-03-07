import pyglet
from pyglet import clock
from pyglet import shapes
from pyglet.window import key

import snake_config
import snake_logick

# from pyglet.window import mouse

color_head = snake_config.snake_head_color
color_body = snake_config.snake_tal_color
food_color = snake_config.food_color
hedg_color = snake_config.hedg_color
food_list = snake_logick.food_list
snake_body = snake_logick.snakeBody
hadge_list = snake_logick.hadge_list
tile_size = snake_config.tile_size
snake_shape_list = []
food_shape_list = []
hedge_shape_list = []

window = pyglet.window.Window(snake_config.win_x, snake_config.win_y)

back_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()


# snake_body_cords = [[35, 35], [34, 35], [33, 35]]
# food_cords = [[50, 38], [23, 45], [13, 65]]
# hedge_cords = [[34, 52], [12, 32], [42, 52]]


def show_snake():
    snake_head_shape.x = snake_body[0][0] * tile_size
    snake_head_shape.y = snake_body[0][1] * tile_size
    for i in range(1, len(snake_body)):
        snake_shape_list[i].x = snake_body[i][0] * tile_size
        snake_shape_list[i].y = snake_body[i][1] * tile_size
    # snake_head.x = snake_head[0]
    # snake_head.y = snake_head[1]


def show_food():
    for i in range(len(food_list)):
        food_shape_list[i].x = food_list[i][0] * tile_size
        food_shape_list[i].y = food_list[i][1] * tile_size


def show_edge():
    print("hadge_list=", hadge_list)
    for i in range(len(hadge_list)):
        hedge_shape_list[i].x = hadge_list[i][0] * tile_size
        hedge_shape_list[i].y = hadge_list[i][1] * tile_size


snake_head_shape = shapes.Rectangle(10, 10, tile_size, tile_size, color=color_head, batch=back_batch)

max_snake_tiled = snake_config.food_per_lvl[9] * snake_config.diff_lvl * snake_config.satiety_per_lvl[9]
for x in range(max_snake_tiled):
    snake_shape_list.append(
        shapes.Rectangle(-snake_config.tile_size, -snake_config.tile_size, tile_size, tile_size, color=color_body,
                         batch=main_batch))

for x in range(snake_config.food_per_lvl[9]):
    food_shape_list.append(
        shapes.Rectangle(-snake_config.tile_size, -snake_config.tile_size, tile_size, tile_size, color=food_color,
                         batch=main_batch))

for x in range(snake_config.hedg_per_lvl[9]):
    hedge_shape_list.append(
        shapes.Rectangle(-snake_config.tile_size, -snake_config.tile_size, tile_size, tile_size, color=hedg_color,
                         batch=main_batch))


def end_game():
    pass


def restart_lvl():
    global food_list, hadge_list
    hadge_list = snake_logick.food_hadge_list_fill(hadge_list, snake_config.hedg_per_lvl)
    food_list = snake_logick.food_hadge_list_fill(food_list, snake_config.food_per_lvl)
    snake_logick.snake_list_fill()
    show_snake()
    show_food()
    show_edge()
    clock.schedule_interval(one_step, 0.5)


def one_step(i):
    # print(i)
    snake_logick.snake_move()
    snake_logick.test_collision()
    show_snake()
    if snake_config.food_eated:
        snake_config.food_eated = 0
        show_food()
        snake_config.curr_satiety = snake_config.satiety_per_lvl[snake_config.curr_lvl] * snake_config.diff_lvl
    if snake_config.final_dead == 1:
        end_game()
        # clock.unschedule(one_step)
    # if snake_config.small_dead == 1:
    # restart_lvl()
    # clock.unschedule(one_step)


# key_code = [key.W, key.A, key.S,key.D]
restart_lvl()


@window.event
def on_draw():
    window.clear()
    # label1.draw()
    back_batch.draw()
    main_batch.draw()


# clock.unschedule(one_step)


@window.event
def on_key_press(symbol, modifiers):  # 0-up 1-left 2-down 3-right
    print(symbol)
    for i in range(4):
        if symbol == snake_config.key_code[i]:
            print(symbol)
            snake_config.last_pereset = i


pyglet.app.run()
