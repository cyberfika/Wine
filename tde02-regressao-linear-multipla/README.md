# TDE 02 - Regressao Linear Multipla

Projeto em Python para resolver a TDE 02 da disciplina Metodos Quantitativos em Computacao, usando Regressao Linear Multipla.

## Objetivo

O projeto le uma base de dados com variaveis numericas, escolhe uma variavel dependente, calcula as correlacoes de Pearson, seleciona as duas variaveis independentes com maior correlacao absoluta e ajusta uma Regressao Linear Multipla pelo metodo dos minimos quadrados.

Neste trabalho foi usada a base Wine Quality. A variavel dependente escolhida foi `quality`.

## Estrutura

```text
tde02-regressao-linear-multipla/
|-- data/
|   |-- raw/
|   `-- processed/
|-- outputs/
|   |-- figures/
|   |-- report.md
|   |-- report.tex
|   `-- results.json
|-- src/
|   |-- main.py
|   |-- data_loader.py
|   |-- regression_analysis.py
|   |-- report_generator.py
|   `-- utils.py
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Como inserir a base

Coloque um arquivo `.csv` ou `.xlsx` em:

```text
data/raw/
```

Se houver mais de um arquivo, o programa usa o primeiro encontrado em ordem alfabetica e informa isso no relatorio.

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Executar

Para escolher a variavel dependente:

```bash
python src/main.py --target quality
```

Para executar automaticamente, usando a ultima coluna numerica como variavel dependente:

```bash
python src/main.py
```

## Saidas geradas

Os principais arquivos gerados ficam em:

```text
outputs/report.md
outputs/report.tex
outputs/results.json
outputs/figures/real_vs_previsto.png
outputs/figures/residuos.png
data/processed/numeric_dataset.csv
```

## Entrega no Canvas

Compacte a pasta inteira:

```text
tde02-regressao-linear-multipla/
```

Ela contem codigo-fonte, dados, relatorio, graficos e resultados.
