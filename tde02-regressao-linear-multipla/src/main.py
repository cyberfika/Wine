from __future__ import annotations

import argparse

from data_loader import find_dataset, prepare_numeric_dataset, read_dataset, variable_summary
from regression_analysis import (
    build_equation,
    choose_target,
    compute_correlations,
    fit_model,
    save_figures,
    save_predictions,
    save_results_json,
    select_independent_variables,
)
from report_generator import generate_markdown_report, generate_tex_report
from utils import ensure_directories, project_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TDE 02 - Regressao Linear Multipla")
    parser.add_argument("--target", help="Nome da variavel dependente numerica.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_directories()

    root = project_root()
    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"
    outputs_dir = root / "outputs"
    figures_dir = outputs_dir / "figures"

    dataset_path, all_dataset_files = find_dataset(raw_dir)
    df = read_dataset(dataset_path)
    numeric_df, ignored_columns = prepare_numeric_dataset(df, processed_dir)

    target, target_auto_selected = choose_target(numeric_df, args.target)
    summary = variable_summary(numeric_df)
    correlations = compute_correlations(numeric_df, target)
    features = select_independent_variables(correlations)

    model_result = fit_model(numeric_df, target, features)
    equation = build_equation(
        target,
        model_result["intercept"],
        model_result["coefficients"],
    )

    save_predictions(
        numeric_df,
        target,
        features,
        model_result["predictions"],
        model_result["residuals"],
        processed_dir,
    )
    save_figures(
        numeric_df[target],
        model_result["predictions"],
        model_result["residuals"],
        figures_dir,
    )
    save_results_json(
        outputs_dir / "results.json",
        target,
        features,
        correlations,
        model_result["intercept"],
        model_result["coefficients"],
        equation,
        model_result["r2"],
        model_result["mae"],
        model_result["rmse"],
    )
    generate_markdown_report(
        outputs_dir / "report.md",
        dataset_path,
        all_dataset_files,
        ignored_columns,
        summary,
        target,
        target_auto_selected,
        correlations,
        features,
        equation,
        model_result["intercept"],
        model_result["coefficients"],
        model_result["r2"],
        model_result["mae"],
        model_result["rmse"],
    )
    generate_tex_report(
        outputs_dir / "report.tex",
        dataset_path,
        all_dataset_files,
        ignored_columns,
        summary,
        target,
        target_auto_selected,
        features,
        correlations,
        equation,
        model_result["intercept"],
        model_result["coefficients"],
        model_result["r2"],
        model_result["mae"],
        model_result["rmse"],
    )

    print("TDE 02 concluida.")
    print(f"Base usada: {dataset_path}")
    print(f"Variavel dependente: {target}")
    print(f"Variaveis independentes: {features[0]}, {features[1]}")
    print(f"Equacao: {equation}")
    print(f"R2: {model_result['r2']:.4f}")
    print(f"Relatorio: {outputs_dir / 'report.md'}")
    print(f"Relatorio TeX: {outputs_dir / 'report.tex'}")


if __name__ == "__main__":
    main()
