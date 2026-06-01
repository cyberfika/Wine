import random

print("*"*4, "PASSEIO ALEATÓRIO - versão Monte Carlo", "*"*4)

def randomwalk_mcarlo(n):
    """ Retorna coordenadas após 'n' blocos de passeio aleatório"""
    x, y = 0, 0
    for i in range(n):
        (dx, dy) = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        x += dx
        y += dy
    return (x, y)

number_of_walks = 20000

# Por que passeios com numero par de blocos tendem a deixar a pessoa
# mais perto da origem do que passeios com numero impar imediatamente menor?
# (comentario entre os instantes 6’48” e 6’58”. Por que que isto acontece?)
#
# A resposta esta na paridade da distancia Manhattan:
#
#     distancia = abs(x) + abs(y)
#
# Distancia Manhattan e a distancia medida andando em uma grade, como ruas
# que se cruzam em angulos retos. Em vez de medir a linha reta entre dois
# pontos, somamos quantos blocos seriam percorridos na horizontal e na vertical.
# Por exemplo, se a pessoa termina em (3, -2), ela esta 3 blocos para um lado
# e 2 blocos para o outro, entao a distancia ate a origem e:
#
#     abs(3) + abs(-2) = 5
#
# O passeio comeca em (0, 0), entao a distancia inicial e 0, que e par.
# A cada passo, a pessoa anda exatamente 1 bloco para norte, sul, leste
# ou oeste. Isso altera uma unica coordenada em 1 unidade. Como consequencia,
# a distancia Manhattan sempre troca de paridade a cada passo:
#
#     0 passos -> distancia par
#     1 passo  -> distancia impar
#     2 passos -> distancia par
#     3 passos -> distancia impar
#     ...
#
# Portanto, depois de um numero par de passos, a pessoa so pode terminar
# em uma distancia par da origem: 0, 2, 4, 6, ...
# Depois de um numero impar de passos, so pode terminar em uma distancia
# impar da origem: 1, 3, 5, 7, ...
#
# Neste problema, consideramos que a pessoa nao precisa de transporte se
# terminar a 4 blocos ou menos da origem. Isso cria uma diferenca importante:
#
#     passeios pares:   distancias favoraveis = 0, 2, 4
#     passeios impares: distancias favoraveis = 1, 3
#
# Ou seja, os passeios pares podem aproveitar tambem a camada de distancia 4,
# que esta exatamente no limite aceito. Ja os passeios impares nao podem
# terminar a distancia 4; eles saltam de 3 para 5. Como 5 ja exige transporte,
# muitos resultados que ficam "logo depois" do limite contam contra os passeios
# impares.
#
# Por isso a simulacao costuma mostrar um padrao aparentemente estranho:
# um passeio de 22 blocos pode ter chance maior de terminar perto de casa
# do que um passeio de 21 blocos. Nao e porque andar mais sempre ajuda;
# e porque o criterio "distancia <= 4" favorece comprimentos pares neste caso.
for walk_length in range(1, 31):
    no_transported_walks = 0 # contador de passeios sem transporte
    for i in range(number_of_walks):
        (x,y) = (randomwalk_mcarlo(walk_length))
        distance = abs(x) + abs(y)
        if distance <= 4:
            no_transported_walks += 1
        not_transported_percentage = float(no_transported_walks) / number_of_walks
    print("Tamanho do passeio = ", walk_length, "Percentual sem transporte = ", 100 * not_transported_percentage)