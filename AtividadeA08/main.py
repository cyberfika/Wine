"""
PONTIFÍCIA UNIVERSIDADE CATÓLICA DO PARANÁ
Escola Politécnica
Curso: Ciência da Computação
Disciplina: Métodos Quantitativos

Atividade A6 - Teorema do Limite Central
Ponto de Entrada Principal (Menu)
"""

import sys
import os

# Adiciona o diretório src ao path para permitir importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import simulacao_a15
import gerar_histogramas

def mostrar_menu():
    print("\n" + "=" * 50)
    print(f"{'MENU DE ATIVIDADES - MÉTODOS QUANTITATIVOS':^50}")
    print("=" * 50)
    print("1. Executar Simulação Completa (Atividade A15)")
    print("   [Gera Tabela, CSV e Respostas Teóricas]")
    print("-" * 50)
    print("2. Gerar Histogramas (Atividade A6)")
    print("   [Análise do Teorema do Limite Central]")
    print("-" * 50)
    print("0. Sair")
    print("=" * 50)

def main():
    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            print("\n>>> Iniciando Atividade A15...")
            simulacao_a15.main()
            input("\nPressione Enter para voltar ao menu...")
        
        elif opcao == '2':
            print("\n>>> Iniciando Atividade A6 (Geração de Gráficos)...")
            gerar_histogramas.main()
            input("\nPressione Enter para voltar ao menu...")
            
        elif opcao == '0':
            print("\nEncerrando o programa. Até logo!")
            break
        
        else:
            print("\n[ERRO] Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
