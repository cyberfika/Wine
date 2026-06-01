from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import correlation_strength


def choose_target(numeric_df: pd.DataFrame, requested_target: str | None) -> tuple[str, bool]:
    if requested_target:
        if requested_target not in numeric_df.columns:
            raise ValueError(f"A variavel dependente '{requested_target}' nao existe ou nao e numerica.")
        return requested_target, False
    return numeric_df.columns[-1], True


def compute_correlations(numeric_df: pd.DataFrame, target: str) -> pd.DataFrame:
    independent_columns = [col for col in numeric_df.columns if col != target]
    correlations = (
        numeric_df[independent_columns]
        .corrwith(numeric_df[target])
        .rename("coeficiente_correlacao")
        .reset_index()
        .rename(columns={"index": "variavel_independente"})
    )
    correlations["correlacao_absoluta"] = correlations["coeficiente_correlacao"].abs()
    correlations["interpretacao"] = correlations["coeficiente_correlacao"].apply(correlation_strength)
    return correlations.sort_values("correlacao_absoluta", ascending=False).reset_index(drop=True)


def select_independent_variables(correlations: pd.DataFrame) -> list[str]:
    if len(correlations) < 2:
        raise ValueError("Sao necessarias ao menos duas variaveis independentes numericas.")
    return correlations.head(2)["variavel_independente"].tolist()


def fit_model(numeric_df: pd.DataFrame, target: str, features: list[str]) -> dict:
    x = numeric_df[features]
    y = numeric_df[target]

    x_design = np.column_stack([np.ones(len(x)), x.to_numpy(dtype=float)])
    y_values = y.to_numpy(dtype=float)
    beta, *_ = np.linalg.lstsq(x_design, y_values, rcond=None)

    predictions = x_design @ beta
    residuals = y_values - predictions

    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((y_values - float(np.mean(y_values))) ** 2))
    mse = float(np.mean(residuals**2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(residuals)))
    r2 = 1 - ss_res / ss_tot

    coefficients = {
        feature: float(coef) for feature, coef in zip(features, beta[1:])
    }

    return {
        "predictions": predictions,
        "residuals": residuals,
        "intercept": float(beta[0]),
        "coefficients": coefficients,
        "r2": float(r2),
        "mae": mae,
        "rmse": rmse,
    }


def build_equation(target: str, intercept: float, coefficients: dict[str, float]) -> str:
    parts = [f"{target} = {intercept:.4f}"]
    for feature, coefficient in coefficients.items():
        sign = "+" if coefficient >= 0 else "-"
        parts.append(f"{sign} {abs(coefficient):.4f}*{feature}")
    return " ".join(parts)


def save_predictions(
    numeric_df: pd.DataFrame,
    target: str,
    features: list[str],
    predictions: np.ndarray,
    residuals: np.ndarray,
    processed_dir: Path,
) -> None:
    output = numeric_df[[target, *features]].copy()
    output["valor_previsto"] = predictions
    output["residuo"] = residuals
    output.to_csv(processed_dir / "predictions.csv", index=False)


def save_figures(y_true: pd.Series, predictions: np.ndarray, residuals: np.ndarray, figures_dir: Path) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 5))
    plt.scatter(y_true, predictions, alpha=0.35)
    plt.xlabel("Valores reais")
    plt.ylabel("Valores previstos")
    plt.title("Valores reais versus valores previstos")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(figures_dir / "real_vs_previsto.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 5))
    plt.scatter(predictions, residuals, alpha=0.35)
    plt.axhline(0, color="red", linewidth=1)
    plt.xlabel("Valores previstos")
    plt.ylabel("Residuos")
    plt.title("Grafico de residuos")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(figures_dir / "residuos.png", dpi=160)
    plt.close()


def save_results_json(
    output_path: Path,
    target: str,
    features: list[str],
    correlations: pd.DataFrame,
    intercept: float,
    coefficients: dict[str, float],
    equation: str,
    r2: float,
    mae: float,
    rmse: float,
) -> None:
    payload = {
        "target_variable": target,
        "selected_independent_variables": features,
        "correlations": {
            row["variavel_independente"]: float(row["coeficiente_correlacao"])
            for _, row in correlations.iterrows()
        },
        "intercept": intercept,
        "coefficients": coefficients,
        "equation": equation,
        "r2_score": r2,
        "mae": mae,
        "rmse": rmse,
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
