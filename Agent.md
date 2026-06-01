# PROMPT PARA CODEX — TDE 02: REGRESSÃO LINEAR MÚLTIPLA

Você é um agente de programação e análise estatística. Sua tarefa é construir um projeto completo em Python para resolver o TDE 02 da disciplina Métodos Quantitativos, cujo tema é Regressão Linear Múltipla.

O trabalho deve ser individual, claro, reproduzível e adequado para entrega acadêmica.

## Objetivo

Criar um projeto que:

1. Leia uma base de dados contendo pelo menos três variáveis numéricas.
2. Liste as variáveis presentes na base e explique o que cada uma representa.
3. Permita definir uma variável dependente, isto é, a variável que será prevista.
4. Calcule o coeficiente de correlação entre cada variável independente e a variável dependente.
5. Se houver mais de três variáveis na base, escolha automaticamente as duas variáveis independentes com maior correlação absoluta em relação à variável dependente.
6. Execute uma Regressão Linear Múltipla usando exatamente duas variáveis independentes.
7. Apresente o passo a passo matemático da obtenção da equação da regressão.
8. Gere a equação final no formato:

   y = b0 + b1*x1 + b2*x2

9. Avalie a qualidade das previsões usando o coeficiente de determinação R².
10. Interprete o valor de R² em linguagem simples.
11. Gere todos os arquivos necessários para entrega: código, relatório, dados tratados, comentários e instruções de execução.

## Antes de começar

Verifique se existe uma base de dados no projeto.

- Se existir arquivo `.csv`, `.xlsx` ou similar, use-o.
- Se não existir base de dados, crie a estrutura do projeto e deixe instruções claras no README para que o usuário adicione a base.
- Não invente dados finais para o trabalho, salvo se criar apenas um arquivo de exemplo claramente identificado como `sample_dataset.csv`.
- Caso a base contenha variáveis não numéricas, o programa deve:
  - identificar essas colunas;
  - informar que elas não serão usadas;
  - criar uma versão filtrada contendo somente variáveis numéricas.

## Estrutura obrigatória do projeto

Crie a seguinte estrutura:

```text
/tde02-regressao-linear-multipla
│
├── data/
│   ├── raw/
│   └── processed/
│
├── outputs/
│   ├── figures/
│   ├── report.md
│   └── results.json
│
├── src/
│   ├── main.py
│   ├── data_loader.py
│   ├── regression_analysis.py
│   ├── report_generator.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
````

## Requisitos técnicos

Use Python moderno e código limpo.

Bibliotecas permitidas:

* pandas
* numpy
* scikit-learn
* matplotlib
* seaborn, somente se realmente necessário
* openpyxl, caso precise ler `.xlsx`

O código deve ser:

* simples;
* bem organizado;
* modular;
* sem erros de execução;
* com funções pequenas;
* com nomes claros;
* com comentários úteis em português;
* com tratamento de erros;
* sem complexidade desnecessária.

## Funcionalidades obrigatórias

### 1. Leitura da base

O programa deve procurar automaticamente arquivos em:

```text
data/raw/
```

Aceitar preferencialmente:

```text
.csv
.xlsx
```

Caso existam vários arquivos, usar o primeiro encontrado e avisar no relatório.

### 2. Identificação das variáveis

O programa deve gerar no relatório uma seção:

```markdown
## 1. Variáveis presentes na base
```

Nessa seção, listar cada coluna numérica encontrada.

Como o programa não conhece semanticamente o significado real de cada variável, ele deve criar uma tabela com:

* nome da variável;
* tipo de dado;
* quantidade de valores válidos;
* média;
* desvio padrão;
* valor mínimo;
* valor máximo;
* campo "representação", inicialmente preenchido como: "Descrever manualmente conforme a base escolhida".

### 3. Escolha da variável dependente

O programa deve permitir definir a variável dependente de duas formas:

1. Por argumento de linha de comando:

```bash
python src/main.py --target nome_da_coluna
```

2. Se nenhum argumento for informado, escolher automaticamente a última coluna numérica como variável dependente e deixar isso claramente indicado no relatório.

### 4. Cálculo das correlações

Para cada variável independente numérica, calcular a correlação de Pearson com a variável dependente.

Gerar no relatório:

```markdown
## 3. Correlação entre variáveis independentes e dependente
```

A tabela deve conter:

* variável independente;
* coeficiente de correlação;
* correlação absoluta;
* interpretação simples:

  * próxima de 0: fraca;
  * entre 0,3 e 0,7: moderada;
  * acima de 0,7: forte.

### 5. Escolha das duas variáveis independentes

Selecionar as duas variáveis independentes com maior correlação absoluta com a variável dependente.

Registrar no relatório:

```markdown
As duas variáveis independentes escolhidas foram:
- x1 = ...
- x2 = ...
```

Explicar que elas foram escolhidas por apresentarem maior associação linear com a variável dependente.

### 6. Regressão Linear Múltipla

Implementar a regressão usando `LinearRegression` do `scikit-learn`.

Também apresentar no relatório o passo a passo matemático:

```markdown
## 4. Obtenção da equação de Regressão Linear Múltipla
```

Explicar:

1. A forma geral da regressão:

```text
y = b0 + b1*x1 + b2*x2
```

2. O significado de cada termo:

   * y: variável dependente;
   * x1 e x2: variáveis independentes;
   * b0: intercepto;
   * b1 e b2: coeficientes angulares.

3. A matriz de entrada X com as duas variáveis independentes.

4. O vetor y com a variável dependente.

5. A ideia de mínimos quadrados.

6. A fórmula conceitual:

```text
β = (XᵀX)^(-1)Xᵀy
```

7. A equação final calculada com os valores reais dos coeficientes.

Exemplo de saída esperada:

```text
y = 12.3456 + 0.7890*x1 - 0.4321*x2
```

### 7. Avaliação da qualidade das previsões

Calcular:

* R²;
* opcionalmente MAE;
* opcionalmente RMSE.

A seção do relatório deve se chamar:

```markdown
## 5. Avaliação da qualidade das previsões
```

Explicar que o principal coeficiente de qualidade será o R², pois ele indica quanto da variação da variável dependente é explicada pelo modelo.

Interpretação obrigatória:

* R² próximo de 0: modelo explica pouco a variação dos dados;
* R² intermediário: modelo tem capacidade moderada de explicação;
* R² próximo de 1: modelo explica grande parte da variação da variável dependente.

Gerar uma frase automática, por exemplo:

```markdown
O valor de R² encontrado foi 0,82. Isso significa que aproximadamente 82% da variação da variável dependente é explicada pelas duas variáveis independentes escolhidas.
```

### 8. Gráficos

Gerar ao menos dois gráficos em `outputs/figures/`:

1. Gráfico de valores reais versus valores previstos.
2. Gráfico de resíduos.

Os gráficos devem ser salvos como `.png` e mencionados no relatório.

### 9. Arquivo `results.json`

Gerar um arquivo JSON com:

```json
{
  "target_variable": "...",
  "selected_independent_variables": ["...", "..."],
  "correlations": {},
  "intercept": 0.0,
  "coefficients": {},
  "equation": "...",
  "r2_score": 0.0,
  "mae": 0.0,
  "rmse": 0.0
}
```

### 10. README.md

O README deve explicar:

* objetivo do projeto;
* como inserir a base de dados;
* como instalar dependências;
* como executar;
* como escolher a variável dependente;
* onde encontrar o relatório final;
* quais arquivos devem ser compactados para entrega no Canvas.

Incluir instruções:

```bash
pip install -r requirements.txt
python src/main.py --target nome_da_coluna
```

Ou, para execução automática:

```bash
python src/main.py
```

### 11. Relatório final

O arquivo `outputs/report.md` deve ser escrito em português acadêmico, claro e direto.

Ele deve conter exatamente estas seções:

```markdown
# TDE 02 – Regressão Linear Múltipla

## Introdução

## 1. Variáveis presentes na base

## 2. Variável dependente escolhida

## 3. Correlação entre variáveis independentes e dependente

## 4. Obtenção da equação de Regressão Linear Múltipla

## 5. Avaliação da qualidade das previsões

## Conclusão
```

A conclusão deve retomar:

* qual variável foi prevista;
* quais variáveis independentes foram usadas;
* qual foi a equação encontrada;
* qual foi o R²;
* se o modelo apresentou qualidade baixa, moderada ou alta.

## Cuidados importantes

* Não usar variáveis categóricas nesta atividade.
* Não usar mais de duas variáveis independentes no modelo final.
* Não omitir o passo a passo matemático.
* Não apresentar apenas o código; o relatório textual é obrigatório.
* Não entregar somente gráficos.
* Não fazer commit, push ou pull request sem autorização expressa do usuário.
* Não alterar arquivos externos ao projeto.
* Não apagar bases de dados fornecidas pelo usuário.

## Resultado esperado

Ao final, o projeto deve permitir que o usuário compacte em um único arquivo:

```text
tde02-regressao-linear-multipla/
```

contendo:

* textos;
* dados;
* comentários;
* códigos;
* relatório;
* gráficos;
* resultados.

Esse pacote será entregue no Canvas para o TDE 02.

```
```
