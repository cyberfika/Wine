from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils import format_number, r2_interpretation


def markdown_table(df: pd.DataFrame, digits: int = 4) -> str:
    formatted = df.copy()
    for column in formatted.columns:
        if pd.api.types.is_numeric_dtype(formatted[column]):
            formatted[column] = formatted[column].map(lambda value: format_number(float(value), digits))

    columns = [str(column) for column in formatted.columns]
    rows = [
        [str(value) for value in row]
        for row in formatted.itertuples(index=False, name=None)
    ]
    widths = [
        max(len(columns[index]), *(len(row[index]) for row in rows))
        for index in range(len(columns))
    ]

    header = "| " + " | ".join(
        columns[index].ljust(widths[index]) for index in range(len(columns))
    ) + " |"
    separator = "| " + " | ".join("-" * widths[index] for index in range(len(columns))) + " |"
    body = [
        "| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(columns))) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def latex_escape(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text


def latex_texttt(value: object) -> str:
    return r"\texttt{" + latex_escape(value) + "}"


def generate_markdown_report(
    output_path: Path,
    dataset_path: Path,
    all_dataset_files: list[Path],
    ignored_columns: list[str],
    variable_summary: pd.DataFrame,
    target: str,
    target_auto_selected: bool,
    correlations: pd.DataFrame,
    features: list[str],
    equation: str,
    intercept: float,
    coefficients: dict[str, float],
    r2: float,
    mae: float,
    rmse: float,
) -> None:
    ignored_text = (
        "Não foram encontradas colunas não numéricas."
        if not ignored_columns
        else "As seguintes colunas não numéricas foram ignoradas: "
        + ", ".join(f"`{col}`" for col in ignored_columns)
        + "."
    )
    multiple_files_text = ""
    if len(all_dataset_files) > 1:
        multiple_files_text = (
            f"\n\nForam encontrados {len(all_dataset_files)} arquivos em `data/raw/`. "
            f"O arquivo usado foi `{dataset_path.name}`, por ser o primeiro em ordem alfabética."
        )

    target_selection_text = (
        "A variável dependente foi escolhida automaticamente por ser a última coluna numérica da base."
        if target_auto_selected
        else "A variável dependente foi definida por argumento de linha de comando."
    )

    quality = r2_interpretation(r2)
    content = f"""# TDE 02 - Regressão Linear Múltipla

## Introdução

Este trabalho aplica Regressão Linear Múltipla a uma base de dados numérica. A base utilizada foi `{dataset_path.name}`. O objetivo é prever uma variável dependente a partir de duas variáveis independentes escolhidas por maior correlação absoluta com a variável que se deseja prever.{multiple_files_text}

{ignored_text}

## 1. Variáveis presentes na base

A tabela a seguir apresenta as variáveis numéricas identificadas na base.

{markdown_table(variable_summary)}

## 2. Variável dependente escolhida

A variável dependente escolhida foi `{target}`.

{target_selection_text}

Essa variável será prevista a partir das demais variáveis numéricas presentes na base.

## 3. Correlação entre variáveis independentes e dependente

Foi calculado o coeficiente de correlação de Pearson entre cada variável independente e `{target}`. A interpretação adotada foi: próxima de 0, correlação fraca; entre 0,3 e 0,7, correlação moderada; acima de 0,7, correlação forte.

{markdown_table(correlations)}

As duas variáveis independentes escolhidas foram:

- x1 = `{features[0]}`
- x2 = `{features[1]}`

Elas foram escolhidas por apresentarem maior associação linear absoluta com a variável dependente.

## 4. Obtenção da equação de Regressão Linear Múltipla

A forma geral da Regressão Linear Múltipla com duas variáveis explicativas é:

```text
y = b0 + b1*x1 + b2*x2
```

Nessa equação:

- y representa a variável dependente;
- x1 e x2 representam as variáveis independentes;
- b0 representa o intercepto;
- b1 e b2 representam os coeficientes angulares.

Neste trabalho:

```text
y = {target}
x1 = {features[0]}
x2 = {features[1]}
```

A matriz de entrada X foi formada pelas duas colunas `{features[0]}` e `{features[1]}`. O vetor y foi formado pela coluna `{target}`. O método de mínimos quadrados procura os coeficientes que minimizam a soma dos quadrados das diferenças entre os valores reais e os valores previstos.

A fórmula conceitual dos coeficientes é:

```text
beta = (X^T X)^(-1) X^T y
```

Os coeficientes calculados foram:

- b0 = {intercept:.4f}
- b1 = {coefficients[features[0]]:.4f}
- b2 = {coefficients[features[1]]:.4f}

A equação final encontrada foi:

```text
{equation}
```

## 5. Avaliação da qualidade das previsões

O principal coeficiente de qualidade usado foi o coeficiente de determinação R². Ele indica quanto da variação da variável dependente é explicada pelo modelo.

O valor encontrado foi:

```text
R2 = {r2:.4f}
```

Isso significa que aproximadamente {r2 * 100:.2f}% da variação da variável dependente `{target}` é explicada pelas duas variáveis independentes escolhidas. Como o R² está mais próximo de 0 do que de 1, o modelo apresenta qualidade {quality} de explicação.

Também foram calculadas medidas auxiliares:

- MAE = {mae:.4f}
- RMSE = {rmse:.4f}

Foram gerados dois gráficos:

- `outputs/figures/real_vs_previsto.png`
- `outputs/figures/residuos.png`

## Conclusão

Neste trabalho, a variável prevista foi `{target}`. As variáveis independentes usadas no modelo final foram `{features[0]}` e `{features[1]}`. A equação encontrada foi `{equation}`. O coeficiente de determinação foi R² = {r2:.4f}, indicando qualidade {quality} para as previsões quando se usam apenas essas duas variáveis explicativas.
"""
    output_path.write_text(content, encoding="utf-8")


def generate_tex_report(
    output_path: Path,
    dataset_path: Path,
    all_dataset_files: list[Path],
    ignored_columns: list[str],
    variable_summary: pd.DataFrame,
    target: str,
    target_auto_selected: bool,
    features: list[str],
    correlations: pd.DataFrame,
    equation: str,
    intercept: float,
    coefficients: dict[str, float],
    r2: float,
    mae: float,
    rmse: float,
) -> None:
    ignored_text = (
        "Não foram encontradas colunas não numéricas."
        if not ignored_columns
        else "As seguintes colunas não numéricas foram ignoradas: "
        + ", ".join(latex_texttt(col) for col in ignored_columns)
        + "."
    )
    multiple_files_text = ""
    if len(all_dataset_files) > 1:
        multiple_files_text = (
            f"\n\nForam encontrados {len(all_dataset_files)} arquivos em "
            f"{latex_texttt('data/raw/')}. O arquivo usado foi "
            f"{latex_texttt(dataset_path.name)}, por ser o primeiro em ordem alfabética."
        )

    target_selection_text = (
        "A variável dependente foi escolhida automaticamente por ser a última coluna numérica da base."
        if target_auto_selected
        else "A variável dependente foi definida por argumento de linha de comando."
    )
    quality = r2_interpretation(r2)

    summary_rows = "\n".join(
        (
            f"{latex_escape(row.variavel)} & {latex_escape(row.tipo_dado)} & "
            f"{float(row.valores_validos):.0f} & {float(row.media):.4f} & "
            f"{float(row.desvio_padrao):.4f} & {float(row.minimo):.4f} & "
            f"{float(row.maximo):.4f} \\\\"
        )
        for row in variable_summary.itertuples(index=False)
    )
    corr_rows = "\n".join(
        (
            f"{latex_escape(row.variavel_independente)} & "
            f"{row.coeficiente_correlacao:.4f} & "
            f"{row.correlacao_absoluta:.4f} & "
            f"{latex_escape(row.interpretacao)} \\\\"
        )
        for row in correlations.itertuples(index=False)
    )

    target_tt = latex_texttt(target)
    feature_1_tt = latex_texttt(features[0])
    feature_2_tt = latex_texttt(features[1])

    content = rf"""\documentclass[12pt,a4paper]{{article}}

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
\usepackage{{graphicx}}
\usepackage{{float}}
\usepackage{{array}}
\usepackage[bottom]{{footmisc}}
\usepackage{{hyperref}}

\geometry{{a4paper,left=3cm,top=3cm,right=2cm,bottom=2cm}}
\onehalfspacing
\setlength{{\parindent}}{{1.25cm}}
\setlength{{\parskip}}{{0pt}}
\setcounter{{secnumdepth}}{{0}}
\hypersetup{{colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black}}

\newcommand{{\aluno}}{{Nome Completo do Aluno}}
\newcommand{{\disciplina}}{{Métodos Quantitativos em Computação}}
\newcommand{{\professor}}{{Júlio Cesar Nievola}}
\newcommand{{\curso}}{{Bacharelado em Ciência da Computação}}
\newcommand{{\turma}}{{Turma U}}
\newcommand{{\instituicao}}{{Pontifícia Universidade Católica do Paraná}}
\newcommand{{\titulo}}{{TDE 02 -- Regressão Linear Múltipla}}
\newcommand{{\descricao}}{{Regressão Linear Múltipla aplicada à base Wine Quality}}

\begin{{document}}
\begin{{titlepage}}
\begin{{center}}
\instituicao

Escola Politécnica

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

\textbf{{Período:}} 2026/01
\end{{flushleft}}
\vfill
Curitiba

2026
\end{{center}}
\end{{titlepage}}

\newpage
\section*{{Resumo}}
\addcontentsline{{toc}}{{section}}{{Resumo}}

Este trabalho aplica Regressão Linear Múltipla a uma base de dados numérica. A base utilizada foi {latex_texttt(dataset_path.name)}. O objetivo é prever uma variável dependente a partir de duas variáveis independentes escolhidas por maior correlação absoluta com a variável que se deseja prever. A variável dependente escolhida foi {target_tt}; as variáveis explicativas selecionadas foram {feature_1_tt} e {feature_2_tt}. O modelo obteve $R^2={r2:.4f}$.

\newpage
\tableofcontents
\newpage

\section{{Introdução}}

Este trabalho aplica Regressão Linear Múltipla a uma base de dados numérica. A base utilizada foi {latex_texttt(dataset_path.name)}. O objetivo é prever uma variável dependente a partir de duas variáveis independentes escolhidas por maior correlação absoluta com a variável que se deseja prever.{multiple_files_text}

{ignored_text}

\section{{1. Variáveis presentes na base}}

A tabela a seguir apresenta as variáveis numéricas identificadas na base.

\scriptsize
\begin{{longtable}}{{p{{4.8cm}}p{{1.6cm}}rrrrr}}
\toprule
Variável & Tipo & Válidos & Média & Desvio & Mínimo & Máximo \\
\midrule
{summary_rows}
\bottomrule
\end{{longtable}}
\normalsize

\section{{2. Variável dependente escolhida}}

A variável dependente escolhida foi {target_tt}.

{target_selection_text}

Essa variável será prevista a partir das demais variáveis numéricas presentes na base.

\section{{3. Correlação entre variáveis independentes e dependente}}

Foi calculado o coeficiente de correlação de Pearson\footnote{{Foi usado o coeficiente de Pearson por ser a medida de correlação linear mais comum em aplicações de Regressão Linear quando as variáveis analisadas são numéricas.}} entre cada variável independente e {target_tt}. A interpretação adotada foi: próxima de 0, correlação fraca; entre 0,3 e 0,7, correlação moderada; acima de 0,7, correlação forte.

\begin{{longtable}}{{p{{4.8cm}}rrl}}
\toprule
Variável independente & Correlação & Absoluta & Interpretação \\
\midrule
{corr_rows}
\bottomrule
\end{{longtable}}

As duas variáveis independentes escolhidas foram:

\begin{{itemize}}
  \item $x_1$ = {feature_1_tt}
  \item $x_2$ = {feature_2_tt}
\end{{itemize}}

Elas foram escolhidas por apresentarem maior associação linear absoluta com a variável dependente.

\section{{4. Obtenção da equação de Regressão Linear Múltipla}}

A forma geral da Regressão Linear Múltipla com duas variáveis explicativas é:
\[
y = b_0 + b_1x_1 + b_2x_2
\]

Nessa equação, $y$ representa a variável dependente; $x_1$ e $x_2$ representam as variáveis independentes; $b_0$ representa o intercepto; e $b_1$ e $b_2$ representam os coeficientes angulares.

Neste trabalho:

\begin{{verbatim}}
y = {target}
x1 = {features[0]}
x2 = {features[1]}
\end{{verbatim}}

A matriz de entrada X foi formada pelas duas colunas {feature_1_tt} e {feature_2_tt}. O vetor y foi formado pela coluna {target_tt}. O método de mínimos quadrados procura os coeficientes que minimizam a soma dos quadrados das diferenças entre os valores reais e os valores previstos.

A organização matricial usada na regressão vem diretamente da base de dados. Cada linha da matriz \(X\) representa uma observação da base, isto é, um vinho analisado. Cada coluna de \(X\) representa uma variável independente escolhida para o modelo. Como foram selecionadas duas variáveis explicativas, a matriz \(X\) contém os valores de {feature_1_tt} e {feature_2_tt}. O vetor \(y\), por sua vez, contém os valores reais da variável dependente {target_tt}, na mesma ordem das observações de \(X\).

O vetor de coeficientes \(\boldsymbol{{\beta}}\) reúne os valores que o modelo precisa estimar. Neste caso, ele contém o intercepto \(b_0\), o coeficiente \(b_1\) associado a {feature_1_tt} e o coeficiente \(b_2\) associado a {feature_2_tt}. Na prática, a regressão procura os valores de \(\boldsymbol{{\beta}}\) que fazem as previsões ficarem o mais próximas possível dos valores reais de \(y\).

Na expressão matricial, \(X^{{\mathsf{{T}}}}\) é a transposta da matriz \(X\), usada para combinar as informações das observações e das variáveis. O termo \(\left(X^{{\mathsf{{T}}}}X\right)^{{-1}}\) representa a inversa da matriz \(X^{{\mathsf{{T}}}}X\), quando essa inversa existe. Essa forma é a solução clássica dos mínimos quadrados para estimar os coeficientes da regressão linear.

A fórmula conceitual dos coeficientes é:
\[
\boldsymbol{{\beta}} = \left(X^{{\mathsf{{T}}}}X\right)^{{-1}}X^{{\mathsf{{T}}}}y
\]

Assim, a fórmula mostra que os coeficientes são calculados a partir da matriz das variáveis independentes e do vetor da variável dependente.

Os coeficientes calculados foram:

\begin{{itemize}}
  \item $b_0 = {intercept:.4f}$
  \item $b_1 = {coefficients[features[0]]:.4f}$
  \item $b_2 = {coefficients[features[1]]:.4f}$
\end{{itemize}}

A equação final encontrada foi:

\begin{{verbatim}}
{equation}
\end{{verbatim}}

\section{{5. Avaliação da qualidade das previsões}}

O principal coeficiente de qualidade usado foi o coeficiente de determinação $R^2$. Ele indica quanto da variação da variável dependente é explicada pelo modelo.

O valor encontrado foi:
\[
R^2 = {r2:.4f}
\]

Isso significa que aproximadamente {r2 * 100:.2f}\% da variação da variável dependente {target_tt} é explicada pelas duas variáveis independentes escolhidas. Como o $R^2$ está mais próximo de 0 do que de 1, o modelo apresenta qualidade {latex_escape(quality)} de explicação.

Também foram calculadas medidas auxiliares\footnote{{A inclusão de MAE e RMSE é opcional nesta atividade. O aluno optou por apresentá-las como complemento ao coeficiente de determinação $R^2$, pois essas métricas indicam o tamanho médio do erro das previsões. A avaliação principal do modelo, entretanto, permanece baseada no $R^2$, conforme solicitado no enunciado.}}:

\begin{{itemize}}
  \item MAE = {mae:.4f}
  \item RMSE = {rmse:.4f}
\end{{itemize}}

Foram gerados dois gráficos:

\begin{{itemize}}
  \item {latex_texttt("outputs/figures/real_vs_previsto.png")}
  \item {latex_texttt("outputs/figures/residuos.png")}
\end{{itemize}}

\section{{Gráficos}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.82\textwidth]{{figures/real_vs_previsto.png}}
\caption{{Valores reais versus valores previstos pelo modelo de regressão.}}
\end{{figure}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.82\textwidth]{{figures/residuos.png}}
\caption{{Distribuição dos resíduos em função dos valores previstos.}}
\end{{figure}}

\section{{Conclusão}}

Neste trabalho, a variável prevista foi {target_tt}. As variáveis independentes usadas no modelo final foram {feature_1_tt} e {feature_2_tt}. A equação encontrada foi {latex_texttt(equation)}. O coeficiente de determinação foi $R^2 = {r2:.4f}$, indicando qualidade {latex_escape(quality)} para as previsões quando se usam apenas essas duas variáveis explicativas.

\end{{document}}
"""
    output_path.write_text(content, encoding="utf-8")
