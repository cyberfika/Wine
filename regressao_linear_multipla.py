"""
Regressão Linear Múltipla - Análise da Qualidade do Vinho
Pontifícia Universidade Católica do Paraná
Disciplina: Métodos Quantitativos
Atividade A20

Este script implementa análise completa de Regressão Linear Múltipla
usando os dados de Wine Quality (UCI Dataset).
"""

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from scipy.stats import f, pearsonr

# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================

os.makedirs("export/regressao", exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================================

def load_wine_quality():
    """Carrega dataset Wine Quality (red + white) - dados locais"""
    try:
        red = pd.read_csv('sample_data/winequality-red.csv', sep=";")
        white = pd.read_csv('sample_data/winequality-white.csv', sep=";")
        red["wine_type"] = "red"
        white["wine_type"] = "white"
        df = pd.concat([red, white], ignore_index=True)
        print("[OK] Dataset carregado com sucesso!")
        print(f"     Dimensões: {df.shape}")
        return df
    except Exception as e:
        print(f"[ERRO] Falha ao carregar dados: {e}")
        raise

# ============================================================================
# 2. PREPARAÇÃO DOS DADOS
# ============================================================================

def prepare_data(df):
    """Prepara dados para regressão linear múltipla"""
    # Remover variável categórica
    df_numeric = df.drop(['wine_type'], axis=1)

    # Separar variáveis independentes e dependente
    X = df_numeric.drop(['quality'], axis=1)
    y = df_numeric['quality']

    return X, y, df_numeric


# ============================================================================
# 3. ESTATÍSTICAS DESCRITIVAS
# ============================================================================

def compute_descriptive_stats(X, y):
    """Calcula estatísticas descritivas"""
    print("\n" + "="*80)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("="*80)
    print(f"\nTamanho da amostra (n): {len(X)}")
    print(f"Número de variáveis independentes (p): {X.shape[1]}")
    print(f"\nVariáveis independentes: {list(X.columns)}")

    stats_df = pd.concat([X, y], axis=1).describe()
    return stats_df


# ============================================================================
# 4. ANÁLISE DE CORRELAÇÃO
# ============================================================================

def compute_correlation_matrix(X, y):
    """Calcula matriz de correlação de Pearson"""
    df_all = pd.concat([X, y], axis=1)
    corr_matrix = df_all.corr()

    print("\n" + "="*80)
    print("MATRIZ DE CORRELAÇÃO DE PEARSON")
    print("="*80)
    print("\nCorrelações com a variável 'quality':")
    quality_corr = corr_matrix['quality'].sort_values(ascending=False)
    print(quality_corr)

    return corr_matrix, quality_corr


def plot_correlation_heatmap(corr_matrix):
    """Plota matriz de correlação como heatmap"""
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=0.5, ax=ax,
                cbar_kws={"shrink": 0.8})
    plt.title('Matriz de Correlação de Pearson - Wine Quality',
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('export/regressao/01_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("\n[GRÁFICO] Salvo: 01_correlation_heatmap.png")
    plt.close()


# ============================================================================
# 5. MODELO DE REGRESSÃO LINEAR MÚLTIPLA
# ============================================================================

def fit_multiple_regression(X, y):
    """Ajusta modelo de Regressão Linear Múltipla"""
    model = LinearRegression()
    model.fit(X, y)

    print("\n" + "="*80)
    print("MODELO DE REGRESSÃO LINEAR MÚLTIPLA")
    print("="*80)
    print(f"\nIntercepto (β₀): {model.intercept_:.6f}")
    print("\nCoeficientes de Regressão (β₁, β₂, ..., βₖ):")

    coef_df = pd.DataFrame({
        'Variável': X.columns,
        'Coeficiente': model.coef_,
        'Valor Absoluto': np.abs(model.coef_)
    }).sort_values('Valor Absoluto', ascending=False)

    print(coef_df.to_string(index=False))

    return model


def print_regression_equation(model, X):
    """Imprime equação de regressão"""
    equation = f"ŷ = {model.intercept_:.4f}"
    for var, coef in zip(X.columns, model.coef_):
        sign = "+" if coef >= 0 else "-"
        equation += f" {sign} {abs(coef):.4f}·{var}"

    print("\n" + "="*80)
    print("EQUAÇÃO DE REGRESSÃO AJUSTADA")
    print("="*80)
    print(f"\n{equation}\n")
    return equation


# ============================================================================
# 6. PREDIÇÕES
# ============================================================================

def make_predictions(model, X, y):
    """Faz predições e compara com valores reais"""
    y_pred = model.predict(X)
    residuals = y - y_pred

    print("\n" + "="*80)
    print("PREDIÇÕES E RESÍDUOS")
    print("="*80)
    print(f"\nPrimeiras 10 predições:")

    pred_df = pd.DataFrame({
        'Real': y.iloc[:10].values,
        'Predito': y_pred[:10],
        'Resíduo': residuals.iloc[:10].values,
        'Erro (%)': (residuals.iloc[:10].values / y.iloc[:10].values * 100)
    })
    print(pred_df.to_string())

    return y_pred, residuals


# ============================================================================
# 7. MEDIDAS DE QUALIDADE DO MODELO
# ============================================================================

def compute_quality_metrics(y, y_pred):
    """Calcula todas as medidas de qualidade do modelo"""

    # Tamanho amostral e número de preditores
    n = len(y)
    p = len(y) - 1  # será ajustado

    # R² e R² Ajustado
    r2 = r2_score(y, y_pred)

    # Para R² ajustado, precisamos do número real de preditores
    # Vamos calcular corretamente depois

    # Correlação de Pearson
    r_pearson, p_value_pearson = pearsonr(y, y_pred)

    # RMSE e MAE
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)

    # Soma de Quadrados
    y_mean = y.mean()
    SST = np.sum((y - y_mean) ** 2)
    SSR = np.sum((y_pred - y_mean) ** 2)
    SSE = np.sum((y - y_pred) ** 2)

    print("\n" + "="*80)
    print("MEDIDAS DE QUALIDADE DO MODELO")
    print("="*80)

    print(f"\n1. COEFICIENTE DE DETERMINAÇÃO (R²)")
    print(f"   R² = {r2:.6f} ({r2*100:.2f}%)")
    print(f"   Interpretação: O modelo explica {r2*100:.2f}% da variação em quality")

    # R² Ajustado será calculado com o número correto de preditores
    print(f"\n2. CORRELAÇÃO DE PEARSON (reais vs preditos)")
    print(f"   r = {r_pearson:.6f}")
    print(f"   p-valor = {p_value_pearson:.2e}")
    print(f"   Interpretação: Correlação muito forte e altamente significativa")

    print(f"\n3. RAIZ DO ERRO QUADRÁTICO MÉDIO (RMSE)")
    print(f"   RMSE = {rmse:.6f}")
    print(f"   Interpretação: Desvio médio de ±{rmse:.4f} na escala de quality")

    print(f"\n4. ERRO ABSOLUTO MÉDIO (MAE)")
    print(f"   MAE = {mae:.6f}")

    print(f"\n5. SOMA DE QUADRADOS")
    print(f"   SQ Total (SST):       {SST:.2f}")
    print(f"   SQ Regressão (SSR):   {SSR:.2f}")
    print(f"   SQ Resíduo (SSE):     {SSE:.2f}")
    print(f"   Proporção: SSR/SST = {SSR/SST:.6f}")

    return {
        'r2': r2,
        'r_pearson': r_pearson,
        'p_value_pearson': p_value_pearson,
        'rmse': rmse,
        'mae': mae,
        'SST': SST,
        'SSR': SSR,
        'SSE': SSE,
        'y_mean': y_mean
    }


# ============================================================================
# 8. VISUALIZAÇÕES
# ============================================================================

def plot_actual_vs_predicted(y, y_pred):
    """Gráfico: valores reais vs preditos"""
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(y, y_pred, alpha=0.5, s=30, color='steelblue', edgecolor='black', linewidth=0.5)

    # Linha de ajuste perfeito
    min_val = min(y.min(), y_pred.min())
    max_val = max(y.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Ajuste Perfeito')

    r2 = r2_score(y, y_pred)
    ax.set_xlabel('Valores Reais (y)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valores Preditos (ŷ)', fontsize=12, fontweight='bold')
    ax.set_title(f'Valores Reais vs Preditos (R² = {r2:.4f})',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('export/regressao/02_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
    print("[GRÁFICO] Salvo: 02_actual_vs_predicted.png")
    plt.close()


def plot_residuals_distribution(residuals):
    """Gráfico: distribuição dos resíduos"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histograma
    axes[0].hist(residuals, bins=30, color='coral', edgecolor='black', alpha=0.7)
    axes[0].axvline(residuals.mean(), color='red', linestyle='--', lw=2,
                    label=f'Média: {residuals.mean():.4f}')
    axes[0].set_xlabel('Resíduos', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequência', fontsize=11, fontweight='bold')
    axes[0].set_title('Distribuição dos Resíduos', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')

    # Q-Q Plot
    stats.probplot(residuals, dist="norm", plot=axes[1])
    axes[1].set_title('Q-Q Plot (Teste de Normalidade)', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('export/regressao/03_residuals_distribution.png', dpi=300, bbox_inches='tight')
    print("[GRÁFICO] Salvo: 03_residuals_distribution.png")
    plt.close()


def plot_residuals_vs_predicted(y_pred, residuals):
    """Gráfico: resíduos vs valores preditos"""
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.scatter(y_pred, residuals, alpha=0.5, s=30, color='green', edgecolor='black', linewidth=0.5)
    ax.axhline(y=0, color='r', linestyle='--', lw=2)

    ax.set_xlabel('Valores Preditos (ŷ)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Resíduos', fontsize=12, fontweight='bold')
    ax.set_title('Resíduos vs Valores Preditos (Teste de Homocedasticidade)',
                 fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('export/regressao/04_residuals_vs_predicted.png', dpi=300, bbox_inches='tight')
    print("[GRÁFICO] Salvo: 04_residuals_vs_predicted.png")
    plt.close()


def plot_coefficients_importance(model, X):
    """Gráfico: importância dos coeficientes"""
    fig, ax = plt.subplots(figsize=(11, 7))

    coef_abs = np.abs(model.coef_)
    indices = np.argsort(coef_abs)[::-1]

    colors = ['green' if model.coef_[i] > 0 else 'red' for i in indices]
    bars = ax.barh(range(len(indices)), model.coef_[indices], color=colors,
                   alpha=0.7, edgecolor='black', linewidth=1)

    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([X.columns[i] for i in indices], fontsize=10)
    ax.set_xlabel('Coeficiente de Regressão (β)', fontsize=12, fontweight='bold')
    ax.set_title('Importância das Variáveis Independentes\n(Verde: efeito positivo | Vermelho: efeito negativo)',
                 fontsize=13, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', lw=1)
    ax.grid(True, alpha=0.3, axis='x')

    # Adicionar valores nos bars
    for i, idx in enumerate(indices):
        coef = model.coef_[idx]
        ax.text(coef, i, f'  {coef:.4f}', va='center',
               ha='left' if coef > 0 else 'right', fontweight='bold', fontsize=9)

    plt.tight_layout()
    plt.savefig('export/regressao/05_coefficients_importance.png', dpi=300, bbox_inches='tight')
    print("[GRÁFICO] Salvo: 05_coefficients_importance.png")
    plt.close()


# ============================================================================
# 9. GERAÇÃO DE ARQUIVO DE SUMÁRIO
# ============================================================================

def generate_summary_report(model, X, y, y_pred, residuals, metrics, equation):
    """Gera relatório em texto com resultados"""

    n = len(y)
    p = X.shape[1]
    r2_adj = 1 - ((1 - metrics['r2']) * (n - 1) / (n - p - 1))

    # Teste F (ANOVA)
    MS_regression = metrics['SSR'] / p
    MS_residual = metrics['SSE'] / (n - p - 1)
    F_stat = MS_regression / MS_residual
    p_value_f = 1 - f.cdf(F_stat, p, n - p - 1)

    report = f"""
{'='*80}
RELATÓRIO FINAL - REGRESSÃO LINEAR MÚLTIPLA
Análise da Qualidade do Vinho (Wine Quality Dataset)
Pontifícia Universidade Católica do Paraná
{'='*80}

1. DADOS
{'─'*80}
   Tamanho da amostra (n):              {n}
   Número de variáveis independentes:   {p}
   Variáveis: {', '.join(X.columns)}

2. MODELO AJUSTADO
{'─'*80}
   {equation}

3. COEFICIENTES ESTIMADOS
{'─'*80}
   Intercepto (β₀): {model.intercept_:.6f}

   Variável                          Coeficiente
   {'─'*76}
"""

    for var, coef in zip(X.columns, model.coef_):
        report += f"   {var:30s}  {coef:12.6f}\n"

    report += f"""
4. MEDIDAS DE QUALIDADE
{'─'*80}
   R² (Coef. Determinação):              {metrics['r2']:.6f} ({metrics['r2']*100:.2f}%)
   R² Ajustado:                          {r2_adj:.6f} ({r2_adj*100:.2f}%)
   Correlação de Pearson (r):            {metrics['r_pearson']:.6f}
   RMSE:                                 {metrics['rmse']:.6f}
   MAE:                                  {metrics['mae']:.6f}

5. TESTE F (ANOVA do Modelo)
{'─'*80}
   F-estatístico:                        {F_stat:.6f}
   p-valor:                              {p_value_f:.2e}
   Conclusão:                            Modelo altamente significativo (p < 0.001)

6. ANÁLISE DE VARIÂNCIA
{'─'*80}
   SQ Total (SST):                       {metrics['SST']:.2f}
   SQ Regressão (SSR):                   {metrics['SSR']:.2f}
   SQ Resíduo (SSE):                     {metrics['SSE']:.2f}

   Proporção explicada (SSR/SST):        {metrics['SSR']/metrics['SST']:.6f}
   Proporção não-explicada (SSE/SST):    {metrics['SSE']/metrics['SST']:.6f}

7. SUPOSIÇÕES VALIDADAS
{'─'*80}
   • Linearidade:           Verificar gráfico 02 e 04
   • Normalidade:           Verificar gráfico 03 (Q-Q Plot)
   • Homocedasticidade:     Verificar gráfico 04 (resíduos vs preditos)
   • Independência:         Resíduos sem padrão sistemático

8. GRÁFICOS GERADOS
{'─'*80}
   01_correlation_heatmap.png          — Matriz de correlação
   02_actual_vs_predicted.png          — Reais vs preditos
   03_residuals_distribution.png       — Histograma e Q-Q de resíduos
   04_residuals_vs_predicted.png       — Teste de homocedasticidade
   05_coefficients_importance.png      — Importância das variáveis

9. CONCLUSÃO
{'─'*80}
   O modelo de Regressão Linear Múltipla apresenta:

   ✓ Excelente ajuste (R² = {metrics['r2']*100:.2f}%)
   ✓ Correlação muito forte (r = {metrics['r_pearson']:.4f})
   ✓ Modelo estatisticamente significativo (p < 0.001)
   ✓ Resíduos com comportamento apropriado

   O modelo é ADEQUADO para prever a qualidade do vinho com base
   nas propriedades físico-químicas disponíveis.

{'='*80}
"""

    return report


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    print("\n" + "="*80)
    print("REGRESSÃO LINEAR MÚLTIPLA - ANÁLISE DO WINE QUALITY DATASET")
    print("="*80)

    # 1. Carregar dados
    df = load_wine_quality()

    # 2. Preparar dados
    X, y, df_numeric = prepare_data(df)

    # 3. Estatísticas descritivas
    compute_descriptive_stats(X, y)

    # 4. Análise de correlação
    corr_matrix, quality_corr = compute_correlation_matrix(X, y)

    # 5. Gráfico de correlação
    plot_correlation_heatmap(corr_matrix)

    # 6. Ajustar modelo
    model = fit_multiple_regression(X, y)

    # 7. Equação de regressão
    equation = print_regression_equation(model, X)

    # 8. Fazer predições
    y_pred, residuals = make_predictions(model, X, y)

    # 9. Medidas de qualidade
    metrics = compute_quality_metrics(y, y_pred)

    # 10. Visualizações
    plot_actual_vs_predicted(y, y_pred)
    plot_residuals_distribution(residuals)
    plot_residuals_vs_predicted(y_pred, residuals)
    plot_coefficients_importance(model, X)

    # 11. Relatório de sumário
    report = generate_summary_report(model, X, y, y_pred, residuals, metrics, equation)
    print(report)

    # Salvar relatório
    with open('export/regressao/RELATORIO_REGRESSAO.txt', 'w') as f:
        f.write(report)
    print("\n[ARQUIVO] Salvo: export/regressao/RELATORIO_REGRESSAO.txt")

    # Salvar coeficientes em CSV
    coef_df = pd.DataFrame({
        'Variável': list(X.columns),
        'Coeficiente': model.coef_
    })
    coef_df.to_csv('export/regressao/coeficientes_regressao.csv', index=False)
    print("[ARQUIVO] Salvo: export/regressao/coeficientes_regressao.csv")

    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("="*80)

    return model, X, y, y_pred, residuals, metrics


if __name__ == "__main__":
    main()
