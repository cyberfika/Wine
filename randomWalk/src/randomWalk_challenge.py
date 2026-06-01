import random

print("*" * 4, "PASSEIO ALEATORIO - desafio Monte Carlo", "*" * 4)


def randomwalk(n):
    """Retorna coordenadas apos 'n' blocos de passeio aleatorio."""
    x, y = 0, 0
    for i in range(n):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        x += dx
        y += dy
    return x, y


def manhattan_distance(x, y):
    """Retorna a distancia ate a origem em uma grade."""
    return abs(x) + abs(y)


def average_distance(walk_length, number_of_walks):
    """Estima a distancia media ate a origem para um tamanho de passeio."""
    total_distance = 0

    for i in range(number_of_walks):
        x, y = randomwalk(walk_length)
        total_distance += manhattan_distance(x, y)

    return total_distance / number_of_walks


number_of_walks = 20000
max_walk_length = 30
distance_limit = 5
longest_walk_under_limit = 0

# Desafio do video:
#
#     "try to find the longest random walk which will on average leave
#      you less than five blocks from home"
#
# Aqui o criterio e diferente do exemplo anterior. Antes, o script media a
# porcentagem de passeios que terminavam a 4 blocos ou menos da origem.
# Neste desafio, a frase "on average" sera tratada literalmente: para cada
# tamanho de passeio, rodamos muitas simulacoes e calculamos a distancia media
# final ate a origem. O maior tamanho aceito e aquele cuja media fica abaixo
# de 5 blocos.
#
# A distancia usada continua sendo a distancia Manhattan:
#
#     distancia = abs(x) + abs(y)
#
# Como a simulacao usa sorteio aleatorio, os valores podem variar um pouco a
# cada execucao. Aumentar number_of_walks reduz essa variacao.
for walk_length in range(1, max_walk_length + 1):
    mean_distance = average_distance(walk_length, number_of_walks)

    if mean_distance < distance_limit:
        longest_walk_under_limit = walk_length

    print(
        "Tamanho do passeio = ",
        walk_length,
        "Distancia media = ",
        round(mean_distance, 3),
    )

print()
print(
    "Maior passeio com distancia media menor que",
    distance_limit,
    "blocos =",
    longest_walk_under_limit,
)
