"""
Pontifícia Universidade Católica do Paraná
Escola Politécnica
Curso: Ciência da Computação
Disciplina: Métodos Quantitativos

Atividade A15 – 16/março/2026 – Cálculo de Probabilidade por Simulação
Aluno: JAFTE CARNEIRO FAGUNDES DA SILVA

Este programa simula o sorteio de palavras sem sentido de 4 letras
baseadas em regras de formação específicas (Exercício 2 da Atividade A2)
e compara a frequência de ocorrência empírica com a probabilidade teórica.
Os resultados também são exportados para um arquivo CSV na pasta /data.
"""

import random
import itertools
import csv
import os

# Definição dos conjuntos de letras para cada posição da palavra
LETRA_1 = ['q', 'w', 'x', 'z'] # 1ª letra: consoantes (4 opções)
LETRA_2 = ['a', 'i', 'u']      # 2ª letra: vogais (3 opções)
LETRA_3 = ['c', 'f', 'p']      # 3ª letra: consoantes (3 opções)
LETRA_4 = ['e', 'o']           # 4ª letra: vogais (2 opções)

def gerar_todas_palavras_possiveis():
    """Gera todas as 72 combinações possíveis de palavras."""
    combinacoes = itertools.product(LETRA_1, LETRA_2, LETRA_3, LETRA_4)
    return [''.join(letras) for letras in combinacoes]

def sortear_palavra():
    """Sorteia aleatoriamente uma palavra de 4 letras seguindo as regras."""
    return random.choice(LETRA_1) + random.choice(LETRA_2) + random.choice(LETRA_3) + random.choice(LETRA_4)

def main():
    todas_palavras = gerar_todas_palavras_possiveis()
    total_palavras = len(todas_palavras)
    quantidades_sorteios = [72, 216, 720, 2160, 7200, 72000]
    
    # Inicialização do dicionário de resultados
    resultados = {palavra: [0] * len(quantidades_sorteios) for palavra in todas_palavras}

    print("Iniciando as simulações...")

    # Realização dos sorteios para cada coluna
    for indice_coluna, qtd in enumerate(quantidades_sorteios):
        for _ in range(qtd):
            palavra_sorteada = sortear_palavra()
            resultados[palavra_sorteada][indice_coluna] += 1
            
    probabilidade_teorica = (1.0 / total_palavras) * 100

    # --- Exportação para CSV ---
    # Caminho do arquivo: ../data/resultados_simulacao.csv (assumindo que o script está em /src)
    # Usamos os.path.join para garantir compatibilidade entre sistemas operacionais.
    diretorio_data = os.path.join("..", "data")
    if not os.path.exists(diretorio_data):
        os.makedirs(diretorio_data)
        
    caminho_csv = os.path.join(diretorio_data, "resultados_simulacao.csv")
    
    try:
        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            # Cabeçalho do CSV
            cabecalho_csv = ["Palavra"] + [f"{q}_sorteios" for q in quantidades_sorteios] + ["Esperado_Percentual"]
            escritor.writerow(cabecalho_csv)
            
            # Dados das palavras
            for palavra in todas_palavras:
                linha_csv = [palavra] + resultados[palavra] + [f"{probabilidade_teorica:.4f}"]
                escritor.writerow(linha_csv)
        print(f"Dados exportados com sucesso para: {caminho_csv}")
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")

    # --- Impressão da Tabela no Terminal ---
    print("\n" + "=" * 115)
    print(f"{'Tabela 01 - Frequência de Ocorrências das Palavras':^115}")
    print("=" * 115)
    
    cabecalho_tab = f"| {'Palavra':^9} "
    for qtd in quantidades_sorteios:
        cabecalho_tab += f"| {qtd:>10} "
    cabecalho_tab += f"| Esperado (%) |"
    
    print(cabecalho_tab)
    print("-" * 115)

    for palavra in todas_palavras:
        linha = f"| {palavra:^9} "
        for contagem in resultados[palavra]:
            linha += f"| {contagem:>10} "
        linha += f"| {probabilidade_teorica:>11.4f}% |"
        print(linha)
        
    print("-" * 115)

    # Respostas das questões
    print("\n" + "=" * 115)
    print(f"{'Respostas das Questões (Itens 6 a 9)':^115}")
    print("=" * 115)
    print("6. O número de vezes que cada palavra sorteada foi igual em cada conjunto de sorteios?")
    print("   Resposta: Não. O processo é aleatório, logo as frequências variam.")
    print("\n7. Em todas as colunas os números são iguais percentualmente? Por quê?")
    print("   Resposta: Não. Amostras pequenas apresentam maior variabilidade estatística.")
    print("\n8. Há alguma tendência à medida que se realizam mais sorteios? Em caso positivo, qual?")
    print("   Resposta: Sim. Convergência para a probabilidade teórica (Lei dos Grandes Números).")
    print("\n9. O que se pode concluir deste experimento?")
    print("   Resposta: Frequências empíricas tendem à probabilidade teórica com o aumento da amostra.")
    print("=" * 115 + "\n")

if __name__ == "__main__":
    main()
