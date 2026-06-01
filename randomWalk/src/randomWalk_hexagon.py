import random

print("*" * 4, "PASSEIO ALEATORIO - blocos hexagonais", "*" * 4)

# Desafio do professor:
#
#     "Refaca o codigo do passeio aleatorio, considerando que os blocos
#      nao sao quadrados e sim hexagonais, apresentando e comentando o codigo."
#
# No passeio original, a cidade era uma grade quadrada. De cada bloco era
# possivel caminhar para 4 vizinhos: norte, sul, leste e oeste.
#
# Em uma grade hexagonal, cada bloco encosta em 6 vizinhos. Portanto, cada
# passo aleatorio deve escolher uma entre 6 direcoes possiveis.
#
# Para modelar os hexagonos, usamos coordenadas axiais (q, r). Elas sao uma
# forma comum de representar uma malha hexagonal usando apenas dois numeros.
# O ponto inicial continua sendo a origem:
#
#     origem = (0, 0)
#
# Cada tupla abaixo representa o deslocamento para um hexagono vizinho.
HEX_DIRECTIONS = [
    (1, 0),    # leste
    (1, -1),   # nordeste
    (0, -1),   # noroeste
    (-1, 0),   # oeste
    (-1, 1),   # sudoeste
    (0, 1),    # sudeste
]


def randomwalk_hexagon(number_of_steps):
    """Retorna a coordenada final apos um passeio aleatorio hexagonal."""
    q, r = 0, 0

    for i in range(number_of_steps):
        dq, dr = random.choice(HEX_DIRECTIONS)
        q += dq
        r += dr

    return q, r


def hex_distance(q, r):
    """Retorna a menor quantidade de passos hexagonais ate a origem."""
    # Em uma grade quadrada, usavamos distancia Manhattan:
    #
    #     abs(x) + abs(y)
    #
    # Essa formula nao serve para hexagonos, porque a geometria tem 6 direcoes.
    # Nas coordenadas axiais (q, r), existe um terceiro eixo implicito:
    #
    #     s = -q - r
    #
    # A distancia hexagonal ate a origem e o maior valor absoluto entre os
    # tres eixos q, r e s.
    s = -q - r
    return max(abs(q), abs(r), abs(s))


def show_walk_examples(number_of_steps, number_of_walks):
    """Mostra varios passeios para visualizar o comportamento da simulacao."""
    for i in range(number_of_walks):
        q, r = randomwalk_hexagon(number_of_steps)
        distance = hex_distance(q, r)
        print(
            "Coordenada final =",
            (q, r),
            "Distancia da origem =",
            distance,
        )


def estimate_average_distance(number_of_steps, number_of_walks):
    """Estima a distancia media final depois de muitos passeios aleatorios."""
    total_distance = 0

    for i in range(number_of_walks):
        q, r = randomwalk_hexagon(number_of_steps)
        total_distance += hex_distance(q, r)

    return total_distance / number_of_walks


# Primeiro, apresentamos alguns passeios individuais de 10 passos.
print()
print("Exemplos de passeios hexagonais com 10 passos:")
show_walk_examples(number_of_steps=10, number_of_walks=10)

# Depois, usamos Monte Carlo para estimar a distancia media ate a origem
# para diferentes tamanhos de passeio.
print()
print("Estimativa por Monte Carlo:")

for walk_length in range(1, 31):
    average_distance = estimate_average_distance(
        number_of_steps=walk_length,
        number_of_walks=20000,
    )
    print(
        "Tamanho do passeio =",
        walk_length,
        "Distancia media hexagonal =",
        round(average_distance, 3),
    )

# Consideracoes ao comparar varias execucoes com a grade quadrada:
#
# 1. Os resultados continuam variando de uma execucao para outra.
#
#    Tanto na grade quadrada quanto na grade hexagonal, o metodo usado e uma
#    simulacao Monte Carlo. Isso significa que os resultados sao estimativas
#    produzidas por sorteios aleatorios. Se executarmos o programa varias vezes,
#    as distancias medias nao serao exatamente iguais.
#
#    Essa variacao diminui quando aumentamos number_of_walks. Com poucos
#    passeios, uma execucao pode ficar visivelmente diferente da outra. Com
#    muitos passeios, as medias tendem a se estabilizar em torno de um valor
#    esperado.
#
# 2. A grade hexagonal tem 6 direcoes, enquanto a quadrada tem 4.
#
#    Na grade quadrada, cada passo escolhe entre:
#
#        norte, sul, leste, oeste
#
#    Na grade hexagonal, cada passo escolhe entre seis vizinhos. Isso muda a
#    geometria do espalhamento. A pessoa tem mais direcoes locais possiveis,
#    mas essas direcoes nao devem ser comparadas diretamente com norte/sul/
#    leste/oeste, porque a malha e outra.
#
# 3. A distancia medida tambem muda.
#
#    Na grade quadrada, a distancia natural ate a origem era a distancia
#    Manhattan:
#
#        abs(x) + abs(y)
#
#    Na grade hexagonal, usamos a distancia hexagonal:
#
#        max(abs(q), abs(r), abs(s)), com s = -q - r
#
#    Portanto, os numeros das duas simulacoes nao medem exatamente a mesma
#    geometria. Eles medem "quantos blocos faltam para voltar" dentro da regra
#    de movimento de cada grade.
#
# 4. O padrao par/impar do caso quadrado fica diferente.
#
#    Na grade quadrada, a distancia Manhattan troca de paridade a cada passo:
#    depois de um numero par de passos, a distancia ate a origem e par; depois
#    de um numero impar de passos, a distancia e impar. Isso explicava por que
#    certos limites, como "4 blocos ou menos", favoreciam passeios pares.
#
#    Na grade hexagonal, ainda existem restricoes geometricas, mas a distancia
#    hexagonal nao produz o mesmo efeito par/impar simples observado com
#    abs(x) + abs(y). Por isso, ao comparar medias de distancia, a curva tende
#    a crescer de modo mais regular, sem a alternancia forte entre comprimentos
#    pares e impares que aparecia no criterio da grade quadrada.
#
# 5. O ponto em que a distancia media passa de um limite pode mudar.
#
#    No desafio anterior da grade quadrada, a distancia media ficava abaixo de
#    5 blocos ate aproximadamente 19 passos. Na grade hexagonal, executando a
#    simulacao varias vezes, esse corte costuma aparecer mais adiante, por
#    volta de 26 passos, embora possa variar um pouco por causa do sorteio.
#
#    Isso nao quer dizer simplesmente que "hexagonos deixam a pessoa mais perto"
#    em qualquer sentido absoluto. Quer dizer que, usando a metrica correta de
#    cada malha e o mesmo numero de simulacoes, o passeio hexagonal apresenta
#    outro ritmo de crescimento da distancia media.
#
# 6. Para comparar com rigor, mantenha os parametros iguais.
#
#    Uma comparacao justa deve usar o mesmo number_of_walks e a mesma faixa de
#    walk_length nas duas simulacoes. Tambem e recomendavel executar cada script
#    varias vezes ou aumentar number_of_walks para reduzir o ruido aleatorio.
