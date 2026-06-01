from __future__ import annotations

from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = (".csv", ".xlsx")


def find_dataset(raw_dir: Path) -> tuple[Path, list[Path]]:
    files = sorted(
        path
        for path in raw_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not files:
        raise FileNotFoundError(
            "Nenhuma base .csv ou .xlsx foi encontrada em data/raw/."
        )
    return files[0], files


def read_dataset(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path)

    try:
        df = pd.read_csv(path)
    except pd.errors.ParserError:
        df = pd.read_csv(path, sep=";")

    if df.shape[1] == 1:
        df_semicolon = pd.read_csv(path, sep=";")
        if df_semicolon.shape[1] > 1:
            return df_semicolon
    return df


def prepare_numeric_dataset(df: pd.DataFrame, processed_dir: Path) -> tuple[pd.DataFrame, list[str]]:
    numeric_df = df.select_dtypes(include="number").copy()
    ignored_columns = [col for col in df.columns if col not in numeric_df.columns]

    if numeric_df.shape[1] < 3:
        raise ValueError(
            "A base precisa conter pelo menos tres variaveis numericas."
        )

    processed_dir.mkdir(parents=True, exist_ok=True)
    numeric_df.to_csv(processed_dir / "numeric_dataset.csv", index=False)
    return numeric_df, ignored_columns


def variable_summary(numeric_df: pd.DataFrame) -> pd.DataFrame:
    summary = numeric_df.agg(["count", "mean", "std", "min", "max"]).T
    summary = summary.reset_index().rename(
        columns={
            "index": "variavel",
            "count": "valores_validos",
            "mean": "media",
            "std": "desvio_padrao",
            "min": "minimo",
            "max": "maximo",
        }
    )
    summary["tipo_dado"] = [str(dtype) for dtype in numeric_df.dtypes]
    summary["representacao"] = "Descrever manualmente conforme a base escolhida"
    return summary[
        [
            "variavel",
            "tipo_dado",
            "valores_validos",
            "media",
            "desvio_padrao",
            "minimo",
            "maximo",
            "representacao",
        ]
    ]
