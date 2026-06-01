from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".matplotlib_cache"))

import matplotlib.pyplot as plt
import pandas as pd


DATA_DIR = BASE_DIR / "sample_data"
OUTPUT_DIR = BASE_DIR / "export" / "bayes_examples"


def load_wine_quality() -> pd.DataFrame:
    red = pd.read_csv(DATA_DIR / "winequality-red.csv", sep=";")
    white = pd.read_csv(DATA_DIR / "winequality-white.csv", sep=";")

    red["wine_type"] = "red"
    white["wine_type"] = "white"

    return pd.concat([red, white], ignore_index=True)


def save_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: Path,
    color: str,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    bars = ax.bar(data[x_col].astype(str), data[y_col], color=color, edgecolor="#333333", linewidth=0.7)

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(data[y_col]) * 1.18)
    ax.grid(axis="y", alpha=0.25)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def build_example_1(df: pd.DataFrame) -> pd.DataFrame:
    high_alcohol = df[df["alcohol"] >= 12].copy()
    total = len(high_alcohol)

    table = (
        high_alcohol["quality"]
        .value_counts()
        .sort_index()
        .rename_axis("quality")
        .reset_index(name="frequencia")
    )
    table["total_alcohol_alto"] = total
    table["probabilidade_condicional"] = table["frequencia"] / total
    table["probabilidade_percentual"] = table["probabilidade_condicional"] * 100
    table["evento_condicionado"] = "alcohol >= 12"

    table.to_csv(OUTPUT_DIR / "exemplo_1_quality_dado_alcohol_alto.csv", index=False)

    save_bar_chart(
        table,
        x_col="quality",
        y_col="probabilidade_percentual",
        title="Exemplo 1: P(quality | alcohol >= 12)",
        xlabel="Valor de quality",
        ylabel="Probabilidade condicional (%)",
        output_path=OUTPUT_DIR / "exemplo_1_quality_dado_alcohol_alto.png",
        color="#4C78A8",
    )

    return table


def build_example_2(df: pd.DataFrame) -> pd.DataFrame:
    quality_7 = df[df["quality"] == 7].copy()
    total = len(quality_7)

    table = (
        quality_7["wine_type"]
        .value_counts()
        .rename_axis("wine_type")
        .reset_index(name="frequencia")
    )
    table["total_quality_7"] = total
    table["probabilidade_condicional"] = table["frequencia"] / total
    table["probabilidade_percentual"] = table["probabilidade_condicional"] * 100
    table["evento_condicionado"] = "quality = 7"

    order = pd.CategoricalDtype(categories=["red", "white"], ordered=True)
    table["wine_type"] = table["wine_type"].astype(order)
    table = table.sort_values("wine_type").reset_index(drop=True)
    table["wine_type"] = table["wine_type"].astype(str)
    table.to_csv(OUTPUT_DIR / "exemplo_2_wine_type_dado_quality_7.csv", index=False)

    save_bar_chart(
        table,
        x_col="wine_type",
        y_col="probabilidade_percentual",
        title="Exemplo 2: P(wine_type | quality = 7)",
        xlabel="Tipo de vinho",
        ylabel="Probabilidade condicional (%)",
        output_path=OUTPUT_DIR / "exemplo_2_wine_type_dado_quality_7.png",
        color="#59A14F",
    )

    return table


def build_summary(example_1: pd.DataFrame, example_2: pd.DataFrame) -> None:
    prediction_1 = example_1.loc[example_1["probabilidade_condicional"].idxmax()]
    prediction_2 = example_2.loc[example_2["probabilidade_condicional"].idxmax()]

    summary = pd.DataFrame(
        [
            {
                "exemplo": 1,
                "pergunta": "Dado que alcohol >= 12, qual valor de quality e mais provavel?",
                "previsao": f"quality = {int(prediction_1['quality'])}",
                "probabilidade_percentual": prediction_1["probabilidade_percentual"],
            },
            {
                "exemplo": 2,
                "pergunta": "Dado que quality = 7, qual valor de wine_type e mais provavel?",
                "previsao": f"wine_type = {prediction_2['wine_type']}",
                "probabilidade_percentual": prediction_2["probabilidade_percentual"],
            },
        ]
    )
    summary.to_csv(OUTPUT_DIR / "resumo_previsoes_bayes.csv", index=False)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_wine_quality()
    example_1 = build_example_1(df)
    example_2 = build_example_2(df)
    build_summary(example_1, example_2)

    print(f"Arquivos gerados em: {OUTPUT_DIR}")
    print()
    print("Exemplo 1 - P(quality | alcohol >= 12)")
    print(example_1[["quality", "frequencia", "probabilidade_percentual"]].to_string(index=False))
    print()
    print("Exemplo 2 - P(wine_type | quality = 7)")
    print(example_2[["wine_type", "frequencia", "probabilidade_percentual"]].to_string(index=False))


if __name__ == "__main__":
    main()
