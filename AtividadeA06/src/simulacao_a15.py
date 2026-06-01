"""
Pontifícia Universidade Católica do Paraná
Escola Politécnica
Curso: Ciência da Computação
Disciplina: Métodos Quantitativos

Atividade A15 – 16/março/2026 – Cálculo de Probabilidade por Simulação
Aluno: JAFTE CARNEIRO FAGUNDES DA SILVA

Este programa simula o sorteio de palavras sem sentido de 4 letras
baseadas em regras de formação específicas e exporta os resultados.
Refatorado para seguir o Princípio da Responsabilidade Única (SRP).
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

def executar_simulacoes(quantidades_sorteios, todas_palavras):
    """
    Executa os sorteios e retorna as frequências de cada palavra.
    Responsabilidade: Apenas simular e processar os dados.
    """
    resultados = {palavra: [0] * len(quantidades_sorteios) for palavra in todas_palavras}
    for indice_coluna, qtd in enumerate(quantidades_sorteios):
        for _ in range(qtd):
            palavra_sorteada = sortear_palavra()
            resultados[palavra_sorteada][indice_coluna] += 1
    return resultados

def exportar_para_csv(resultados, quantidades_sorteios, todas_palavras, probabilidade_teorica, diretorio="data"):
    """Exporta os resultados da simulação para um arquivo CSV."""
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        
    caminho_csv = os.path.join(diretorio, "resultados_simulacao.csv")
    
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

def imprimir_resultados(resultados, quantidades_sorteios, todas_palavras, probabilidade_teorica):
    """Imprime a tabela formatada com os resultados no terminal."""
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

def imprimir_respostas_questoes():
    """Imprime as respostas das questões teóricas da Atividade A15."""
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

def main():
    todas_palavras = gerar_todas_palavras_possiveis()
    total_palavras = len(todas_palavras)
    quantidades_sorteios = [72, 216, 720, 2160, 7200, 72000]
    probabilidade_teorica = (1.0 / total_palavras) * 100

    print("Iniciando as simulações...")
    resultados = executar_simulacoes(quantidades_sorteios, todas_palavras)

    # Diretório data relativo ao arquivo atual
    diretorio_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    
    exportar_para_csv(resultados, quantidades_sorteios, todas_palavras, probabilidade_teorica, diretorio_data)
    imprimir_resultados(resultados, quantidades_sorteios, todas_palavras, probabilidade_teorica)
    imprimir_respostas_questoes()

if __name__ == "__main__":
    main()
