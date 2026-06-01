from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib_cache"))

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from PIL import Image

EXPORT_DIR = BASE_DIR / "export"
GRAPH_DIR = EXPORT_DIR / "a12_graficos"
SUMMARY_PATH = EXPORT_DIR / "a12_resumo_medidas_wine_quality.csv"
PDF_PATH = EXPORT_DIR / "Relatorio_Final_A12_WineQuality.pdf"

PAGE_W_CM = 21.0
PAGE_H_CM = 29.7
CM_PER_IN = 2.54
PAGE_W_IN = PAGE_W_CM / CM_PER_IN
PAGE_H_IN = PAGE_H_CM / CM_PER_IN
A4 = (PAGE_W_IN, PAGE_H_IN)

LEFT = 3.0 / PAGE_W_CM
RIGHT = 1.0 - (2.0 / PAGE_W_CM)
TOP = 1.0 - (3.0 / PAGE_H_CM)
BOTTOM = 2.0 / PAGE_H_CM
CONTENT_W = RIGHT - LEFT
CONTENT_H = TOP - BOTTOM

FONT = "Times New Roman"
BODY_SIZE = 12
LINE_HEIGHT_PT = 17
CAPTION_SIZE = 12


@lru_cache(maxsize=4096)
def text_width_pt(text: str, size: float = BODY_SIZE, weight: str = "normal") -> float:
    if not text:
        return 0.0
    if text.isspace():
        return size * 0.25 * len(text)
    prop = FontProperties(family=FONT, size=size, weight=weight)
    return float(TextPath((0, 0), text, prop=prop).get_extents().width)


def draw_text(
    fig: plt.Figure,
    text: str,
    x: float,
    y: float,
    size: float = BODY_SIZE,
    weight: str = "normal",
    ha: str = "left",
) -> None:
    fig.text(
        x,
        y,
        text,
        ha=ha,
        va="top",
        fontsize=size,
        fontfamily=FONT,
        fontweight=weight,
    )


def draw_justified_paragraph(
    fig: plt.Figure,
    text: str,
    x: float,
    y: float,
    max_width_frac: float = CONTENT_W,
    size: float = BODY_SIZE,
    weight: str = "normal",
    first_line_indent_cm: float = 1.25,
    line_height_pt: float = LINE_HEIGHT_PT,
) -> float:
    max_width_pt = max_width_frac * PAGE_W_IN * 72
    indent_frac = first_line_indent_cm / PAGE_W_CM
    line_height_frac = (line_height_pt / 72) / PAGE_H_IN

    words = text.split()
    if not words:
        return y - line_height_frac

    lines: list[list[str]] = []
    current: list[str] = []
    available_pt = max_width_pt - (indent_frac * PAGE_W_IN * 72)
    for word in words:
        candidate = current + [word]
        if current and text_width_pt(" ".join(candidate), size=size, weight=weight) > available_pt:
            lines.append(current)
            current = [word]
            available_pt = max_width_pt
        else:
            current = candidate
        if lines:
            available_pt = max_width_pt
    if current:
        lines.append(current)

    for index, line_words in enumerate(lines):
        is_last = index == len(lines) - 1
        line_x = x + (indent_frac if index == 0 else 0.0)
        if is_last or len(line_words) == 1:
            draw_text(fig, " ".join(line_words), line_x, y, size=size, weight=weight)
        else:
            words_width_pt = sum(text_width_pt(word, size=size, weight=weight) for word in line_words)
            line_width_pt = max_width_pt - (indent_frac * PAGE_W_IN * 72 if index == 0 else 0.0)
            gap_pt = max(
                (line_width_pt - words_width_pt) / (len(line_words) - 1),
                text_width_pt(" ", size=size, weight=weight),
            )
            cursor = line_x
            for word in line_words:
                draw_text(fig, word, cursor, y, size=size, weight=weight)
                cursor += (text_width_pt(word, size=size, weight=weight) + gap_pt) / (72 * PAGE_W_IN)
        y -= line_height_frac
    return y - (6 / 72 / PAGE_H_IN)


def draw_justified_block(fig: plt.Figure, paragraphs: list[str], x: float, y: float) -> float:
    for paragraph in paragraphs:
        y = draw_justified_paragraph(fig, paragraph, x, y)
    return y


def new_page(title: str | None = None) -> plt.Figure:
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor("white")
    if title:
        draw_text(fig, title.upper(), 0.5, TOP, size=BODY_SIZE, weight="bold", ha="center")
    return fig


def finish_page(pdf: PdfPages, fig: plt.Figure, page_number: int) -> None:
    draw_text(fig, str(page_number), 0.5, BOTTOM / 2, size=BODY_SIZE, ha="center")
    pdf.savefig(fig)
    plt.close(fig)


def fmt(value: object, digits: int = 3) -> str:
    if pd.isna(value):
        return "-"
    if isinstance(value, str):
        return value
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def add_abnt_figure(
    fig: plt.Figure,
    image_path: Path,
    number: int,
    title: str,
    source: str,
    x: float,
    y: float,
    w: float,
    h: float,
) -> None:
    draw_text(fig, f"Figura {number} - {title}", x, y + h + 0.035, size=CAPTION_SIZE)
    image = Image.open(image_path)
    image_ax = fig.add_axes([x, y, w, h])
    image_ax.imshow(image)
    image_ax.axis("off")
    draw_text(fig, f"Fonte: {source}", x, y - 0.012, size=CAPTION_SIZE)


def build_pdf() -> None:
    summary = pd.read_csv(SUMMARY_PATH)
    numeric = summary[summary["tipo"].isin(["continua", "ordinal"])].copy()

    with PdfPages(PDF_PATH) as pdf:
        fig = new_page()
        y = TOP
        draw_text(fig, "PONTIFICIA UNIVERSIDADE CATOLICA DO PARANA", 0.5, y, ha="center")
        y -= 0.035
        draw_text(fig, "Escola Politecnica - Curso de Ciencia da Computacao", 0.5, y, ha="center")
        y -= 0.035
        draw_text(fig, "Disciplina: Metodos Quantitativos", 0.5, y, ha="center")
        y -= 0.105
        draw_text(fig, "RELATORIO FINAL DA ATIVIDADE A12", 0.5, y, weight="bold", ha="center")
        y -= 0.035
        draw_text(fig, "Analise descritiva da base Wine Quality", 0.5, y, ha="center")
        y -= 0.075
        y = draw_justified_block(
            fig,
            [
                "Resumo. Este relatorio apresenta uma analise quantitativa descritiva da base Wine Quality, composta por amostras de vinhos tintos e brancos do tipo Vinho Verde. O experimento calcula, para cada variavel de entrada e para a variavel alvo quality, medidas de tendencia central, dispersao, assimetria e o percentual de observacoes alem de um desvio padrao da media. A variavel nominal wine_type e analisada apenas por frequencia, pois nao possui escala numerica.",
                "Base de dados. Foram combinados os arquivos locais winequality-red.csv e winequality-white.csv, totalizando 6.497 observacoes, 11 variaveis fisico-quimicas, a variavel ordinal quality e a variavel nominal wine_type. A base nao apresentou valores ausentes.",
                "Metodologia. Para variaveis numericas foram calculadas media, mediana, moda, desvio absoluto medio, variancia amostral, desvio padrao amostral e percentual de valores fora do intervalo [media - 1 desvio padrao, media + 1 desvio padrao]. A direcao da assimetria foi justificada pela comparacao entre media, mediana e moda principal.",
            ],
            LEFT,
            y,
        )
        draw_text(fig, "Palavras-chave: estatistica descritiva; assimetria; dispersao; Wine Quality.", LEFT, y)
        finish_page(pdf, fig, 1)

        fig = new_page("Resultados Descritivos")
        table_data = [
            [
                row["variavel"],
                fmt(row["media"]),
                fmt(row["mediana"]),
                str(row["moda"])[:12],
                fmt(row["desvio_padrao_amostral"]),
                fmt(row["percentual_alem_1_dp"], 2),
                row["distribuicao"].replace("Assimetrica ", "Ass. "),
            ]
            for _, row in numeric.iterrows()
        ]
        ax = fig.add_axes([LEFT, BOTTOM + 0.13, CONTENT_W, CONTENT_H - 0.22])
        ax.axis("off")
        table = ax.table(
            cellText=table_data,
            colLabels=["Variavel", "Media", "Mediana", "Moda", "DP", "% > 1 DP", "Distribuicao"],
            loc="center",
            cellLoc="center",
            bbox=[0, 0, 1, 1],
            colWidths=[0.25, 0.09, 0.10, 0.12, 0.09, 0.11, 0.20],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7.2)
        for (row_index, _), cell in table.get_celld().items():
            cell.set_linewidth(0.35)
            cell.set_text_props(fontfamily=FONT)
            if row_index == 0:
                cell.set_text_props(weight="bold", fontfamily=FONT)
                cell.set_facecolor("#E8ECEF")
        draw_text(fig, "Tabela 1 - Medidas descritivas das variaveis numericas.", LEFT, BOTTOM + 0.09)
        draw_text(fig, "Fonte: Elaborado pelo autor (2026), com base nos arquivos locais do dataset Wine Quality.", LEFT, BOTTOM + 0.055)
        finish_page(pdf, fig, 2)

        fig = new_page("Evidencias Graficas")
        add_abnt_figure(fig, GRAPH_DIR / "hist_quality.png", 1, "Distribuicao da variavel alvo quality", "Elaborado pelo autor (2026), a partir do dataset Wine Quality.", LEFT, 0.57, CONTENT_W, 0.23)
        add_abnt_figure(fig, GRAPH_DIR / "hist_alcohol.png", 2, "Distribuicao da variavel alcohol", "Elaborado pelo autor (2026), a partir do dataset Wine Quality.", LEFT, 0.24, CONTENT_W, 0.23)
        draw_justified_paragraph(fig, "Parecer. A variavel quality concentra observacoes nas notas 5 e 6, evidenciando desbalanceamento e baixa frequencia de notas extremas. A variavel alcohol apresenta media superior a mediana e maior concentracao entre aproximadamente 9 e 11,5, indicando cauda a direita e dispersao moderada.", LEFT, 0.165)
        finish_page(pdf, fig, 3)

        fig = new_page("Distribuicoes das Variaveis")
        add_abnt_figure(fig, GRAPH_DIR / "histogramas_variaveis_numericas.png", 3, "Histogramas das variaveis numericas com media e mediana", "Elaborado pelo autor (2026), a partir do dataset Wine Quality.", LEFT, 0.25, CONTENT_W, 0.55)
        draw_justified_paragraph(fig, "A leitura conjunta dos histogramas mostra que a maior parte das variaveis fisico-quimicas nao segue distribuicao simetrica perfeita. Residual sugar, chlorides, volatile acidity e sulphates apresentam caudas a direita mais evidentes; total sulfur dioxide, density e quality foram classificadas com assimetria a esquerda pelo criterio comparativo adotado.", LEFT, 0.17)
        finish_page(pdf, fig, 4)

        fig = new_page("Analise Final e Referencias")
        y = TOP - 0.07
        y = draw_justified_block(
            fig,
            [
                "Analise dos dados. O conjunto apresenta estrutura adequada para analise descritiva, pois nao ha valores ausentes e todas as variaveis fisico-quimicas sao numericas. Entretanto, os resultados mostram que a base nao e homogenea: diversas variaveis possuem dispersao relevante e assimetria, o que recomenda cautela no uso exclusivo da media como medida representativa. Nesses casos, mediana, moda e representacao grafica complementam a interpretacao.",
                "A variavel alvo quality e ordinal e apresenta concentracao nas categorias intermediarias, principalmente notas 5 e 6. Essa concentracao sugere que, em modelagens futuras, a base tende a favorecer previsoes de qualidade media e pode exigir tratamento para classes raras. A variavel wine_type, por ser nominal, nao permite media, mediana, variancia ou desvio padrao com significado estatistico; sua interpretacao adequada ocorre por frequencias absolutas e percentuais.",
                "Conclusao. O experimento atende ao enunciado da Atividade A12 ao calcular as medidas solicitadas para as variaveis de entrada e para a variavel prevista. Os resultados indicam predominio de assimetria nas distribuicoes, dispersao variavel entre atributos e concentracao da qualidade em valores medianos. Assim, a descricao estatistica confirma a necessidade de analisar cada variavel por um conjunto de medidas, e nao por uma unica estatistica isolada.",
            ],
            LEFT,
            y,
        )
        y -= 0.015
        draw_text(fig, "Referencias", LEFT, y, weight="bold")
        y -= 0.045
        for reference in [
            "CORTEZ, Paulo; CERDEIRA, Antonio; ALMEIDA, Fernando; MATOS, Telmo; REIS, Jose. Modeling wine preferences by data mining from physicochemical properties. Decision Support Systems, v. 47, n. 4, p. 547-553, 2009.",
            "UNIVERSITY OF CALIFORNIA IRVINE. Wine Quality. UCI Machine Learning Repository, 2009. Disponivel em: https://archive.ics.uci.edu/dataset/186/wine+quality. Acesso em: 7 maio 2026.",
            "PONTIFICIA UNIVERSIDADE CATOLICA DO PARANA. Atividade A12 - Analise de Dados. Curitiba: PUCPR, 2026.",
        ]:
            y = draw_justified_paragraph(fig, reference, LEFT, y, first_line_indent_cm=0.0)
        finish_page(pdf, fig, 5)

    print(PDF_PATH)


if __name__ == "__main__":
    build_pdf()
