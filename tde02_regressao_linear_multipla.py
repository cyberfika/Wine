from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "export" / "wine_quality_original.csv"
EXPORT_DIR = BASE_DIR / "export" / "tde02_regressao_linear_multipla"
DOCS_DIR = BASE_DIR / "docs"

TARGET = "quality"

VARIABLE_DESCRIPTIONS = {
    "fixed acidity": "Acidez fixa do vinho, formada principalmente por acidos nao volateis.",
    "volatile acidity": "Acidez volatil, associada principalmente ao acido acetico.",
    "citric acid": "Quantidade de acido citrico, relacionada ao frescor do vinho.",
    "residual sugar": "Acucar residual que permanece apos a fermentacao.",
    "chlorides": "Concentracao de cloretos, relacionada ao teor de sais.",
    "free sulfur dioxide": "Dioxido de enxofre livre, usado para reduzir oxidacao e crescimento microbiano.",
    "total sulfur dioxide": "Dioxido de enxofre total, incluindo a parte livre e a combinada.",
    "density": "Densidade do vinho, influenciada por alcool, acucar e compostos dissolvidos.",
    "pH": "Medida de acidez ou basicidade do vinho.",
    "sulphates": "Sulfatos presentes no vinho, associados a conservacao e estabilidade.",
    "alcohol": "Teor alcoolico do vinho.",
    "quality": "Nota de qualidade atribuida por avaliadores, usada como variavel dependente.",
    "wine_type": "Tipo do vinho, tinto ou branco. Coluna categorica ignorada nesta TDE.",
}


def load_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    red_path = BASE_DIR / "sample_data" / "winequality-red.csv"
    white_path = BASE_DIR / "sample_data" / "winequality-white.csv"
    red = pd.read_csv(red_path, sep=";")
    white = pd.read_csv(white_path, sep=";")
    red["wine_type"] = "red"
    white["wine_type"] = "white"
    return pd.concat([red, white], ignore_index=True)


def fit_multiple_linear_regression(x: pd.DataFrame, y: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    x_design = np.column_stack([np.ones(len(x)), x.to_numpy(dtype=float)])
    beta, *_ = np.linalg.lstsq(x_design, y.to_numpy(dtype=float), rcond=None)
    y_pred = x_design @ beta
    return beta, y_pred


def build_tex(
    df: pd.DataFrame,
    numeric_columns: list[str],
    independent_columns: list[str],
    correlations: pd.DataFrame,
    selected_features: list[str],
    beta: np.ndarray,
    r2: float,
    mae: float,
    mse: float,
    rmse: float,
) -> str:
    corr_rows = "\n".join(
        f"{row.variavel} & {row.correlacao:.4f} \\\\"
        for row in correlations.itertuples(index=False)
    )
    var_rows = "\n".join(
        f"{col} & {VARIABLE_DESCRIPTIONS.get(col, '')} \\\\" for col in df.columns
    )

    return rf"""\documentclass[12pt,a4paper]{{article}}

\usepackage{{iftex}}
\ifPDFTeX
  \usepackage[T1]{{fontenc}}
  \usepackage[utf8]{{inputenc}}
  \usepackage{{newtxtext}}
  \usepackage{{newtxmath}}
\else
  \usepackage{{fontspec}}
  \setmainfont{{Times New Roman}}
\fi

\usepackage[brazil]{{babel}}
\usepackage{{geometry}}
\usepackage{{setspace}}
\usepackage{{indentfirst}}
\usepackage{{microtype}}
\usepackage{{amsmath,amssymb}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{listings}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}

\geometry{{a4paper,left=3cm,top=3cm,right=2cm,bottom=2cm}}
\onehalfspacing
\setlength{{\parindent}}{{1.25cm}}
\setlength{{\parskip}}{{0pt}}
\hypersetup{{colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black}}

\lstdefinestyle{{pythonstyle}}{{
  language=Python,
  basicstyle=\ttfamily\small,
  keywordstyle=\color{{blue!60!black}},
  commentstyle=\color{{green!40!black}},
  stringstyle=\color{{red!50!black}},
  showstringspaces=false,
  breaklines=true,
  frame=single,
  tabsize=4
}}
\lstset{{style=pythonstyle}}

\newcommand{{\aluno}}{{Nome Completo do Aluno}}
\newcommand{{\disciplina}}{{Metodos Quantitativos em Computacao}}
\newcommand{{\professor}}{{Julio Cesar Nievola}}
\newcommand{{\curso}}{{Bacharelado em Ciencia da Computacao}}
\newcommand{{\turma}}{{Turma U}}
\newcommand{{\instituicao}}{{Pontificia Universidade Catolica do Parana}}
\newcommand{{\titulo}}{{TDE 02 -- Regressao Linear Multipla com a Base Wine Quality}}
\newcommand{{\descricao}}{{Aplicacao de regressao linear multipla para previsao da qualidade de vinhos}}

\begin{{document}}

\begin{{titlepage}}
\begin{{center}}
\instituicao

Escola Politecnica

\curso

\vfill
{{\bfseries\Large \titulo\par}}
\vspace{{1cm}}
{{\large \descricao\par}}
\vfill
\begin{{flushleft}}
\textbf{{Aluno:}} \aluno

\textbf{{Disciplina:}} \disciplina

\textbf{{Professor:}} \professor

\textbf{{Turma:}} \turma

\textbf{{Periodo:}} 2026/01
\end{{flushleft}}
\vfill
Curitiba

2026
\end{{center}}
\end{{titlepage}}

\newpage
\section*{{Resumo}}
\addcontentsline{{toc}}{{section}}{{Resumo}}

Este trabalho apresenta a aplicacao de Regressao Linear Multipla na base Wine Quality. A variavel dependente escolhida foi \texttt{{quality}}, que representa a nota de qualidade do vinho. Como variaveis explicativas, foram selecionadas as duas variaveis independentes com maior correlacao absoluta com a variavel alvo: \texttt{{{selected_features[0]}}} e \texttt{{{selected_features[1]}}}. O modelo obtido apresentou coeficiente de determinacao $R^2={r2:.4f}$, indicando que essas duas variaveis explicam aproximadamente {r2 * 100:.2f}\% da variacao observada na qualidade dos vinhos.

\textbf{{Palavras-chave:}} regressao linear multipla; correlacao; Wine Quality; coeficiente de determinacao.

\newpage
\tableofcontents

\newpage
\section{{Base de Dados}}

A base Wine Quality contem {len(df)} observacoes. Para esta atividade, foram consideradas somente as variaveis numericas. A coluna \texttt{{wine\_type}}, quando presente, e categorica e foi ignorada no ajuste do modelo.

\begin{{longtable}}{{p{{4cm}}p{{10cm}}}}
\toprule
\textbf{{Variavel}} & \textbf{{Representacao}} \\
\midrule
{var_rows}
\bottomrule
\end{{longtable}}

\section{{Variavel Dependente e Variaveis Independentes}}

A variavel dependente escolhida foi:

\[
Y = quality
\]

As variaveis independentes numericas consideradas inicialmente foram:

\[
{', '.join(independent_columns)}
\]

\section{{Correlacao com a Variavel Dependente}}

Foi calculado o coeficiente de correlacao de Pearson entre cada variavel independente e \texttt{{quality}}.

\begin{{table}}[h]
\centering
\begin{{tabular}}{{lr}}
\toprule
\textbf{{Variavel independente}} & \textbf{{Correlacao com quality}} \\
\midrule
{corr_rows}
\bottomrule
\end{{tabular}}
\end{{table}}

As duas maiores correlacoes em valor absoluto foram obtidas pelas variaveis \texttt{{{selected_features[0]}}} e \texttt{{{selected_features[1]}}}.

\section{{Obtencao da Equacao de Regressao}}

A forma geral da Regressao Linear Multipla com duas variaveis explicativas e:

\[
Y = b_0 + b_1X_1 + b_2X_2
\]

Neste trabalho:

\[
X_1 = {selected_features[0]}
\]

\[
X_2 = {selected_features[1]}
\]

Logo:

\[
quality = b_0 + b_1 \cdot {selected_features[0]} + b_2 \cdot {selected_features[1]}
\]

Os coeficientes estimados pelo metodo dos minimos quadrados foram:

\[
b_0 = {beta[0]:.4f}
\]

\[
b_1 = {beta[1]:.4f}
\]

\[
b_2 = {beta[2]:.4f}
\]

Assim, a equacao final do modelo e:

\[
quality = {beta[0]:.4f} + {beta[1]:.4f} \cdot {selected_features[0]} {beta[2]:+.4f} \cdot {selected_features[1]}
\]

\section{{Avaliacao da Qualidade das Previsoes}}

A qualidade das previsoes foi avaliada pelo coeficiente de determinacao, $R^2$:

\[
R^2 = 1 - \frac{{SQ_{{res}}}}{{SQ_{{tot}}}}
\]

O valor encontrado foi:

\[
R^2 = {r2:.4f}
\]

Portanto, o modelo explica aproximadamente {r2 * 100:.2f}\% da variacao de \texttt{{quality}}. Esse resultado indica baixo poder explicativo quando se usam apenas as duas variaveis selecionadas, embora elas sejam as mais correlacionadas individualmente com a qualidade do vinho.

Tambem foram calculadas as seguintes medidas de erro:

\begin{{table}}[h]
\centering
\begin{{tabular}}{{lr}}
\toprule
\textbf{{Metrica}} & \textbf{{Valor}} \\
\midrule
MAE & {mae:.4f} \\
MSE & {mse:.4f} \\
RMSE & {rmse:.4f} \\
\bottomrule
\end{{tabular}}
\end{{table}}

\section{{Codigo Fonte}}

Os calculos foram realizados pelo arquivo \texttt{{tde02\_regressao\_linear\_multipla.py}}, presente na raiz do repositorio.

\begin{{lstlisting}}
python tde02_regressao_linear_multipla.py
\end{{lstlisting}}

\end{{document}}
"""


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()
    numeric_df = df.select_dtypes(include="number").copy()
    numeric_columns = list(numeric_df.columns)
    independent_columns = [col for col in numeric_columns if col != TARGET]

    correlations = (
        numeric_df[independent_columns]
        .corrwith(numeric_df[TARGET])
        .rename("correlacao")
        .reset_index()
        .rename(columns={"index": "variavel"})
    )
    correlations["correlacao_absoluta"] = correlations["correlacao"].abs()
    correlations = correlations.sort_values("correlacao_absoluta", ascending=False)

    selected_features = correlations.head(2)["variavel"].tolist()
    x = numeric_df[selected_features]
    y = numeric_df[TARGET]
    beta, y_pred = fit_multiple_linear_regression(x, y)

    residuals = y.to_numpy(dtype=float) - y_pred
    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((y.to_numpy(dtype=float) - float(y.mean())) ** 2))
    r2 = 1 - ss_res / ss_tot
    mae = float(np.mean(np.abs(residuals)))
    mse = float(np.mean(residuals**2))
    rmse = float(np.sqrt(mse))

    correlations.to_csv(EXPORT_DIR / "correlacoes_quality.csv", index=False)
    predictions = pd.DataFrame(
        {
            "quality_real": y,
            "quality_prevista": y_pred,
            "residuo": residuals,
            selected_features[0]: x[selected_features[0]],
            selected_features[1]: x[selected_features[1]],
        }
    )
    predictions.to_csv(EXPORT_DIR / "previsoes_regressao.csv", index=False)
    metrics = pd.DataFrame(
        [
            {"metrica": "intercepto", "valor": beta[0]},
            {"metrica": f"coeficiente_{selected_features[0]}", "valor": beta[1]},
            {"metrica": f"coeficiente_{selected_features[1]}", "valor": beta[2]},
            {"metrica": "r2", "valor": r2},
            {"metrica": "mae", "valor": mae},
            {"metrica": "mse", "valor": mse},
            {"metrica": "rmse", "valor": rmse},
            {"metrica": "n_observacoes", "valor": len(df)},
        ]
    )
    metrics.to_csv(EXPORT_DIR / "metricas_modelo.csv", index=False)

    tex = build_tex(
        df=df,
        numeric_columns=numeric_columns,
        independent_columns=independent_columns,
        correlations=correlations,
        selected_features=selected_features,
        beta=beta,
        r2=r2,
        mae=mae,
        mse=mse,
        rmse=rmse,
    )
    tex_path = DOCS_DIR / "trabalho_tde02_regressao_linear_multipla.tex"
    tex_path.write_text(tex, encoding="utf-8")

    print("TDE 02 - Regressao Linear Multipla")
    print(f"Base: {DATA_PATH if DATA_PATH.exists() else 'sample_data/*.csv'}")
    print(f"Observacoes: {len(df)}")
    print(f"Variavel dependente: {TARGET}")
    print("Correlacoes com quality:")
    print(correlations[["variavel", "correlacao"]].to_string(index=False))
    print()
    print(f"Variaveis selecionadas: {selected_features[0]}, {selected_features[1]}")
    print(
        "Equacao: "
        f"quality = {beta[0]:.4f} + {beta[1]:.4f} * {selected_features[0]} "
        f"{beta[2]:+.4f} * {selected_features[1]}"
    )
    print(f"R2: {r2:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Arquivos gerados em: {EXPORT_DIR}")
    print(f"Arquivo TeX gerado: {tex_path}")


if __name__ == "__main__":
    main()
