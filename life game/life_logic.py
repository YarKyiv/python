import life_data

g_x = life_data.g_x
g_y = life_data.g_y


life = []
next_life = []


template_space_ship=[[0, -0], [-1, 0], [-2, 0], [-3, -0], [-4, -0] , [-5, -0], [-0, -1], [-0, -2], [-1, -3], [-3, -4], [-4, -4], [-6, -3], [-6, -1]]
template_planer=[[0, -0], [1, -1], [1, -2], [0, -2], [-1, -2]]
template_list=[template_planer,template_space_ship]


for y in range(g_y):
    for x in range(g_x):
        life.append(0)  # y*g_x+x
        next_life.append(0)


def getLife(x, y):
    return life[y * g_x + x]


def setLife(x, y, s):
    life[y * g_x + x] = s


def chek_s(x, y):
    shift = [[-1, -1], [1, -1], [1, 1], [-1, 1], [1, 0], [-1, 0], [0, 1], [0, -1]]
    susid = 0
    for s in shift:
        xt = x + s[0]
        yt = y + s[1]
        if xt < 0: xt = g_x - 1
        if yt < 0: yt = g_y - 1
        if xt >= g_x: xt = 0
        if yt >= g_y: yt = 0

        susid += getLife(xt, yt)
    return susid


def clear_field():
    for y in range(g_y):
        for x in range(g_x):
            setLife(x,y, 0)







def nextStep():
    for y in range(g_y):
        for x in range(g_x):
            s = chek_s(x, y)  # вот тут мы пощитали соседий

            if getLife(x,y) and (s == 2 or s ==3):
                next_life[y * g_x + x] = 1
            else:
                next_life[y * g_x + x] = 0
            if s == 3:
                next_life[y * g_x + x] = 1
    for y in range(g_y):
        for x in range(g_x):
            setLife(x,y, next_life[y * g_x + x])
            next_life[y * g_x + x] = 0

# в пустой (мёртвой) клетке, с которой соседствуют три живые клетки, зарождается жизнь;
# если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
# в противном случае (если живых соседей меньше двух или больше трёх) клетка умирает («от одиночества» или «от перенаселённости»).
