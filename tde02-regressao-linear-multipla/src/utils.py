from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_directories() -> None:
    root = project_root()
    for relative_path in [
        "data/raw",
        "data/processed",
        "outputs/figures",
    ]:
        (root / relative_path).mkdir(parents=True, exist_ok=True)


def format_number(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}"


def correlation_strength(value: float) -> str:
    abs_value = abs(value)
    if abs_value < 0.3:
        return "fraca"
    if abs_value <= 0.7:
        return "moderada"
    return "forte"


def r2_interpretation(r2_value: float) -> str:
    if r2_value < 0.3:
        return "baixa"
    if r2_value < 0.7:
        return "moderada"
    return "alta"

