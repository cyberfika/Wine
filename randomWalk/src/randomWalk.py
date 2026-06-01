import random

print("*"*4, "PASSEIO ALEATÓRIO - versão estendida", "*"*4)

def randomwalk(n):
    """ Retorna coordenadas após 'n' blocos de passeio aleatório"""
    x = 0
    y = 0
    for i in range(n):
        step = random.choice(['N','S','E','W'])
        if step == 'N':
            y = y + 1
        elif step == 'S':
            y = y - 1
        elif step == 'E':
            x = x + 1
        else:
            x = x - 1
    return (x, y)

for i in range(25):
    walk = randomwalk(10)
    print(walk, "Distância da origem = ", abs(walk[0]) + abs(walk[1]))

print("*"*4, "PASSEIO ALEATÓRIO - versão compacta", "*"*4)

def randomwalk_compact(n):
    """ Retorna coordenadas após 'n' blocos de passeio aleatório"""
    x, y = 0, 0
    for i in range(n):
        (dx, dy) = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        x += dx
        y += dy
    return (x, y)

for i in range(25):
    walk = randomwalk_compact(10)
    print(walk, "Distância da origem = ", abs(walk[0]) + abs(walk[1]))
