"""
Script para gerar histogramas das frequências dos sorteios.
Este módulo foca exclusivamente na geração e exportação de gráficos (SRP),
importando os dados e lógica do simulador existente (Baixo Acoplamento).
"""

import os
import matplotlib.pyplot as plt
from simulacao_a15 import gerar_todas_palavras_possiveis, executar_simulacoes

def plotar_histogramas(resultados, quantidades_sorteios, diretorio_saida="data"):
    """
    Plota e salva um histograma para cada conjunto de sorteios.
    O histograma mostra a distribuição das frequências absolutas das palavras.
    """
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)

    for indice_coluna, qtd in enumerate(quantidades_sorteios):
        # Coleta as frequências de todas as palavras para o tamanho de sorteio atual
        frequencias = [resultados[palavra][indice_coluna] for palavra in resultados]
        
        plt.figure(figsize=(10, 6))
        
        # Criação do Histograma
        plt.hist(frequencias, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)
        
        plt.title(f"Distribuição das Frequências - {qtd} Sorteios\nTeorema do Limite Central", fontsize=14)
        plt.xlabel("Frequência Absoluta (Vezes que uma palavra foi sorteada)", fontsize=12)
        plt.ylabel("Quantidade de Palavras", fontsize=12)
        
        # Adiciona a linha da média esperada
        media_esperada = qtd / len(resultados)
        plt.axvline(media_esperada, color='red', linestyle='dashed', linewidth=2, 
                    label=f'Frequência Média Esperada: {media_esperada:.2f}')
        plt.legend()
        plt.grid(axis='y', alpha=0.75)
        
        # Salva o arquivo na pasta definida
        caminho_arquivo = os.path.join(diretorio_saida, f"histograma_{qtd}_sorteios.png")
        plt.savefig(caminho_arquivo, bbox_inches='tight')
        plt.close()
        print(f"Histograma salvo com sucesso: {caminho_arquivo}")

def main():
    print("Preparando dados para geração dos histogramas (Atividade A6)...")
    
    # 1. Obtenção dos dados utilizando o módulo do simulador (Baixo Acoplamento)
    todas_palavras = gerar_todas_palavras_possiveis()
    quantidades_sorteios = [72, 216, 720, 2160, 7200, 72000]
    
    print("Executando a simulação (isso pode levar alguns segundos)...")
    resultados = executar_simulacoes(quantidades_sorteios, todas_palavras)
    
    # 2. Definição do diretório de saída
    diretorio_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    
    # 3. Geração dos gráficos (SRP)
    print("Gerando e salvando os histogramas na pasta 'data'...")
    plotar_histogramas(resultados, quantidades_sorteios, diretorio_saida)
    
    print("\nProcesso concluído! Os histogramas estão prontos para análise do Teorema do Limite Central.")

if __name__ == "__main__":
    main()
