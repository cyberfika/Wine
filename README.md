# 📊 Wine Quality — Frequency Distribution Analysis

### Métodos Quantitativos | PUCPR

Este repositório apresenta a construção completa da **Tabela de Distribuição de Frequência** para todas as variáveis do dataset **Wine Quality (UCI Machine Learning Repository)**, utilizando metodologia estatística formal e implementação em Python (Google Colab).

---

## 🎯 Objetivo do Projeto

Aplicar técnicas de **Estatística Descritiva** para:

* Construir tabelas de distribuição de frequência com intervalos de classe
* Aplicar rigorosamente o método ensinado em aula (baseado na fórmula de Sturges)
* Interpretar graficamente a variável mais relevante segundo a literatura
* Garantir reprodutibilidade computacional

---

## 🍷 Base de Dados

**Fonte:** UCI Machine Learning Repository
**Dataset:** Wine Quality (id=186)
**Autores:** Cortez et al. (2009)
**Link:** [https://archive.ics.uci.edu/dataset/186/wine+quality](https://archive.ics.uci.edu/dataset/186/wine+quality)

A base contém duas subamostras:

* 🍷 Vinho tinto (*red*)
* 🥂 Vinho branco (*white*)

As amostras foram coletadas no norte de Portugal e referem-se ao vinho **Vinho Verde**.

### 📌 Estrutura da Base

* 11 variáveis físico-químicas (contínuas)
* 1 variável ordinal (quality)
* 1 variável nominal (wine_type — adicionada na combinação dos datasets)

Total: **13 variáveis**

---

## 🧠 Tipo de Problema

A base pode ser interpretada como:

* 📈 Problema de regressão (qualidade como variável numérica)
* 📊 Problema de classificação ordinal (classes ordenadas)
* 🔎 Possível detecção de outliers (classes desbalanceadas)
* 🧪 Análise de relevância de variáveis

---

## 📚 Referência Científica

Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009).
**Modeling wine preferences by data mining from physicochemical properties.**
*Decision Support Systems*, 47, 547–553.

O artigo demonstra que variáveis como **alcohol** e **volatile acidity** possuem forte influência na qualidade do vinho.

---

## 📐 Metodologia Estatística Aplicada

A construção das tabelas de frequência seguiu rigorosamente o método ensinado em aula:

1. Organização em rol (ordem crescente)
2. Cálculo da amplitude total (AT = máximo − mínimo)
3. Determinação do número de classes (Fórmula de Sturges)
4. Arredondamento da amplitude de classe para cima
5. Construção de intervalos no padrão [a, b)
6. Cálculo de:

   * Frequência absoluta (fi)
   * Frequência acumulada (Fi)
   * Frequência relativa (fr) ✅
   * Frequência relativa acumulada (Fr) ✅
7. Cálculo do ponto médio (xi)

> A inclusão de frequências relativas foi decisão metodológica do aluno por constituir boa prática estatística.

---

## 🔍 Tratamento por Tipo de Variável

| Tipo de variável    | Tratamento aplicado                               |
| ------------------- | ------------------------------------------------- |
| Contínua            | Intervalos de classe (método completo)            |
| Ordinal (quality)   | Distribuição simples (sem intervalos artificiais) |
| Nominal (wine_type) | Distribuição categórica                           |

Essa abordagem segue o rigor estatístico adequado a cada tipo de dado.

---

## 📈 Visualizações

A variável **alcohol** foi escolhida para análise gráfica por sua relevância destacada no paper.

Foram gerados:

* 📊 Histograma (com classes de Sturges)
* 📈 Ogiva (frequência relativa acumulada usando limite superior das classes)
* 📦 Boxplot

### Principais conclusões:

* Distribuição concentrada entre 9% e 11,5%
* Leve assimetria positiva
* Presença de poucos valores extremos superiores
* Coerência com os achados da literatura

---

## 🛠️ Tecnologias Utilizadas

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Google Colab

---

## 📁 Arquivos Gerados

* `wine_quality_original.csv`
* `newdata_wine_quality_binned.csv`
* `freq_all_variables_long.csv`
* Tabelas individuais por variável

---

## 🎓 Conclusão

O projeto demonstra:

* Aplicação correta de métodos estatísticos clássicos
* Implementação computacional reprodutível
* Integração entre teoria estatística e análise prática de dados
* Consistência com literatura científica

Este trabalho consolida a compreensão de **distribuição de frequência**, **intervalos de classe**, **interpretação gráfica** e **tratamento adequado por tipo de variável**.

---

## 👨‍🎓 Autor

Jafte Carneiro Fagundes da Silva
Disciplina: Métodos Quantitativos — PUCPR
