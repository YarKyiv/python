import random

import snake_config


def roll_dice(n):
    return random.randint(0, n)


def food_hadge_list_fill(list, list_per_lvl):
    list.clear()
    for j in range(list_per_lvl[snake_config.curr_lvl]):
        element_x = random.randint(0, snake_config.win_x / snake_config.tile_size - 1)
        element_y = random.randint(0, snake_config.win_y / snake_config.tile_size - 1)
        list.append([element_x, element_y])
    print("food list = ", food_list)
    return list


def snake_list_fill():
    new_snake_x = snake_config.win_x / 2 / snake_config.tile_size
    new_snake_y = snake_config.win_y / 2 / snake_config.tile_size
    for i in snakeBody:
        i[0] = new_snake_x
        i[1] = new_snake_y
        new_snake_x -= 1


def snake_move():
    global snakeBody, new_x, new_y
    new_x = snakeBody[0][0] + dir_list[snake_config.last_pereset][0]
    new_y = snakeBody[0][1] + dir_list[snake_config.last_pereset][1]
    print(new_x, new_y)

    if new_x == border_x:
        new_x=0

    if new_y == border_y:
        new_y = 0

    if new_x<0:
        new_x=border_x

    if new_y<0:
        new_y=border_y

    snakeBody.insert(0, [new_x, new_y])

    if snake_config.curr_satiety == 0:
        snakeBody.pop()
    else:
        print("satiety = ", snake_config.curr_satiety)
        snake_config.curr_satiety -= 1
        print("satiety = ", snake_config.curr_satiety)


def sed_start_snake():
    global snakeBody
    for i in range(snake_config.start_b_size[snake_config.curr_lvl]):
        snakeBody.append([int((snake_config.win_x / snake_config.tile_size) / 2 + i),
                          int((snake_config.win_y / snake_config.tile_size) / 2)])


def body_call():
    for i in range(1, len(snakeBody)):
        if snakeBody[0][0] == snakeBody[i][0] and snakeBody[0][1] == snakeBody[i][1]:
            return True  # dead
    return False


def list_call(list):
    for i in list:
        if snakeBody[0][0] == i[0] and snakeBody[0][1] == i[1]:
            return True  # dead
    return False


def test_collision():
    if body_call() or list_call(hadge_list):
        snake_config.curr_hp -= 1
        snake_config.small_dead = 1
    if list_call(food_list):
        # snake_config.curr_satiety += snake_config.satiety_per_lvl[snake_config.curr_lvl] * snake_config.diff_lvl
        snake_config.food_eated = 1
        food_list.remove(snakeBody[0])
        print("food list=", food_list)
    if snake_config.curr_hp <= 0:
        snake_config.final_dead = 1


# variables______________
snakeBody = []
sed_start_snake()
last_prest = 1
dir_list = [[0, 1], [-1, 0], [0, -1], [1, 0]]
food_list = []
hadge_list = []

border_x = int(snake_config.win_x / snake_config.tile_size)
border_y = int(snake_config.win_y / snake_config.tile_size)

new_x = 0
new_y = 0
