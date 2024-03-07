import math
import random


def roll_dice(d):
    return random.randint(0, int(d))


def shot_analys(x, y, r0):
    # r0 = math.sqrt(x ** 2 + y ** 2)
    a = roll_dice(360)
    r = r0 - math.sqrt(roll_dice(r0 ** 2))
    x1 = r * math.cos(a) + x
    y1 = r * math.sin(a) + y
    return [x1, y1]
