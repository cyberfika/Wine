# Resumo da Atividade A14 — Teste de Hipótese

**Disciplina:** Métodos Quantitativos
**Aluno:** Jafte Carneiro Fagundes da Silva
**Data:** 01/junho/2026
**Universidade:** PUCPR — Escola Politécnica

---

## 📋 Objetivo da Atividade

Elaborar 4 situações de uso de Teste de Hipótese utilizando o dataset **Wine Quality** (UCI Machine Learning Repository), conforme solicitado no enunciado:

1. Teste de Hipótese com Intervalo de Confiança
2. Teste para Diferença entre Médias (Amostras Grandes)
3. Teste para Amostras Pequenas com Variâncias Iguais
4. Teste para Amostras Pequenas com Variâncias Diferentes

---

## 📊 Dados Utilizados

### Fonte
- **Dataset:** Wine Quality (UCI id=186)
- **Autores:** Cortez et al. (2009)
- **Localização:** `/Users/jafte/PyCharmProject/Wine/sample_data/`
- **Arquivo de referência:** `DataFrequencyDistribution.ipynb`

### Características dos Dados
- **Vinho Tinto:** 1.599 observações
- **Vinho Branco:** 4.898 observações
- **Total combinado:** 6.497 observações
- **Variáveis:** 11 variáveis físico-químicas contínuas + 1 ordinal + 1 nominal

### Variáveis Utilizadas nos Testes

| Questão | Variável | Tipo | Amostra Tinto | Amostra Branco |
|---------|----------|------|---------------|----------------|
| 1 | alcohol | Contínua | n=1.599, μ=10,423%, σ=1,066% | — |
| 2 | alcohol | Contínua | n=1.599, μ=10,423%, σ²=1,136 | n=4.898, μ=10,514%, σ²=1,514 |
| 3 | volatile acidity | Contínua | n=12, μ=0,616, σ²=0,023 | n=14, μ=0,253, σ²=0,002 |
| 4 | pH | Contínua | n=10, μ=3,355, σ²=0,016 | n=9, μ=3,187, σ²=0,013 |

---

## 🎯 Questão 1: Teste de Hipótese com Intervalo de Confiança

### Situação-Problema
Um enólogo deseja verificar se o teor médio de álcool dos vinhos tintos é diferente de 10,0%.

### Hipóteses
- **H₀:** μ = 10,0%
- **H₁:** μ ≠ 10,0%

### Dados Amostrais
- n = 1.599
- X̄ = 10,423%
- S = 1,066%
- α = 0,05 (bilateral)

### Solução
1. Valor crítico: Z = ±1,96
2. Intervalo de confiança: μ ∈ (10,371 ; 10,475)
3. Decisão: **Rejeita-se H₀** (10,0 não está contido no intervalo)

### Pseudocódigo
```
Entrada: X̄, S, n, μ₀, α
Z_c ← z_critico(α)
erro ← Z_c × (S/√n)
LI ← X̄ - erro
LS ← X̄ + erro
Se μ₀ < LI ou μ₀ > LS:
    Rejeitar H₀
Senão:
    Não rejeitar H₀
```

### Explicação do Pseudocódigo
- **Entrada:** Parâmetros amostrais e nível de significância
- **Valor crítico:** Para α=0,05 bilateral, Z=±1,96 (95% de confiança)
- **Erro padrão:** S/√n representa a dispersão da distribuição amostral
- **Intervalo de confiança:** Define a região de não-rejeição
- **Regra de decisão:** Se μ₀ cair fora do intervalo, há evidência para rejeitar H₀
- **Vantagem:** Método intuitivo baseado diretamente no intervalo de confiança

---

## 🎯 Questão 2: Diferença entre Médias (Amostras Grandes)

### Situação-Problema
Uma vinícola verifica se existe diferença no teor alcoólico médio entre vinhos tintos e brancos.

### Hipóteses
- **H₀:** μ_tinto = μ_branco
- **H₁:** μ_tinto ≠ μ_branco

### Dados Amostrais
| | Tinto | Branco |
|---|---|---|
| n | 1.599 | 4.898 |
| X̄ (%) | 10,423 | 10,514 |
| S² | 1,136 | 1,514 |

### Solução
1. Erro padrão: √(1,136/1599 + 1,514/4898) = 0,03192
2. Z₀ = (10,423 - 10,514) / 0,03192 = -2,85
3. Decisão: **Rejeita-se H₀** (|-2,85| = 2,85 > 1,96)

### Pseudocódigo
```
Entrada: X̄₁, X̄₂, S₁², S₂², n₁, n₂, α
erro_padrao ← √(S₁²/n₁ + S₂²/n₂)
Z₀ ← (X̄₁ - X̄₂) / erro_padrao
Z_c ← z_critico(α)  [ex.: 1,96 para α=0,05]
Se |Z₀| > Z_c:
    Rejeitar H₀
Senão:
    Não rejeitar H₀
```

### Explicação do Pseudocódigo
- **Entrada:** Médias, variâncias e tamanhos de ambas as amostras
- **Erro padrão da diferença:** √(S₁²/n₁ + S₂²/n₂) mede a dispersão da distribuição amostral das diferenças
- **Estatística Z₀:** Quantifica quantos desvios padrão a diferença observada está distante de zero
- **Valor crítico:** Define região de rejeição bilateral
- **Regra de decisão:** Comparação com valor crítico
- **Justificativa:** Teorema do Limite Central garante normalidade para n>30

---

## 🎯 Questão 3: Amostras Pequenas com Variâncias Iguais

### Situação-Problema
Um pesquisador compara acidez volátil entre pequenas amostras de vinhos tintos e brancos, assumindo variâncias iguais.

### Hipóteses
- **H₀:** μ₁ = μ₂
- **H₁:** μ₁ ≠ μ₂

### Dados Amostrais
| | Tinto | Branco |
|---|---|---|
| n | 12 | 14 |
| X̄ | 0,616 | 0,253 |
| S² | 0,023 | 0,002 |

### Solução
1. Variância agrupada: S_p² = 0,01162
2. t₀ = (0,616 - 0,253) / √(0,01162 × (1/12 + 1/14)) = 8,35
3. gl = 12 + 14 - 2 = 24
4. Valor crítico: t_(24; 0,025) = 2,064
5. Decisão: **Rejeita-se H₀** (8,35 > 2,064)

### Pseudocódigo
```
Entrada: X̄₁, X̄₂, S₁², S₂², n₁, n₂, α
S_p² ← [(n₁-1)S₁² + (n₂-1)S₂²] / (n₁ + n₂ - 2)
t₀ ← (X̄₁ - X̄₂) / √[S_p² × (1/n₁ + 1/n₂)]
gl ← n₁ + n₂ - 2
t_c ← t_critico(α, gl)
Se |t₀| > t_c:
    Rejeitar H₀
Senão:
    Não rejeitar H₀
```

### Explicação do Pseudocódigo
- **Entrada:** Médias, variâncias e tamanhos de ambas as amostras
- **Variância agrupada:** Combina variâncias amostrais ponderadas pelos graus de liberdade
- **Estatística t₀:** Segue distribuição t de Student com gl graus de liberdade
- **Graus de liberdade:** gl = n₁ + n₂ - 2 (perda de 2 gl por duas médias estimadas)
- **Distribuição t:** Mais dispersa que Z, com caudas mais pesadas (maior incerteza com amostras pequenas)
- **Pressupostos:** Normalidade das populações e igualdade de variâncias (crucial)

---

## 🎯 Questão 4: Amostras Pequenas com Variâncias Diferentes (Welch)

### Situação-Problema
Um enólogo compara pH entre pequenas amostras de vinhos tintos e brancos, com variâncias presumivelmente diferentes.

### Hipóteses
- **H₀:** μ₁ = μ₂
- **H₁:** μ₁ ≠ μ₂

### Dados Amostrais
| | Tinto | Branco |
|---|---|---|
| n | 10 | 9 |
| X̄ | 3,355 | 3,187 |
| S² | 0,016 | 0,013 |

### Solução
1. A = 0,016/10 = 0,0016; B = 0,013/9 = 0,001444
2. t* = (3,355 - 3,187) / √(0,0016 + 0,001444) = 3,04
3. gl (Welch-Satterthwaite) = 17
4. Valor crítico: t_(17; 0,025) = 2,110
5. Decisão: **Rejeita-se H₀** (3,04 > 2,110)

### Pseudocódigo
```
Entrada: X̄₁, X̄₂, S₁², S₂², n₁, n₂, α
A ← S₁²/n₁
B ← S₂²/n₂
t* ← (X̄₁ - X̄₂) / √(A + B)
gl ← ⌊(A + B)² / (A²/(n₁-1) + B²/(n₂-1))⌋
t_c ← t_critico(α, gl)
Se |t*| > t_c:
    Rejeitar H₀
Senão:
    Não rejeitar H₀
```

### Explicação do Pseudocódigo
- **Entrada:** Médias, variâncias e tamanhos de ambas as amostras
- **Componentes de variância:** A e B calculam contribuições individuais (não agrupadas)
- **Estatística t*:** Não agrupa variâncias, segue distribuição t aproximadamente
- **Graus de liberdade ajustados (Welch-Satterthwaite):** Fórmula complexa que penaliza variâncias desiguais
  - Quando variâncias muito diferentes: gl < n₁+n₂-2 (valor crítico mais conservador)
- **Arredondamento:** ⌊·⌋ trunca para inteiro (necessário para tabela t)
- **Vantagem:** Não requer pressuposição de homogeneidade; robusto e versátil

---

## 📁 Arquivos Gerados

| Arquivo | Localização | Descrição |
|---------|------------|-----------|
| A14_TesteDeHipotese.tex | `/AtividadeA14/` | Documento LaTeX completo com 4 questões e pseudocódigos explicados |
| RESUMO_A14.md | `/AtividadeA14/` | Este arquivo — Resumo em Markdown |

---

## 🔑 Conceitos-Chave Abordados

### Métodos Estatísticos
- ✅ Teste de hipótese bilateral
- ✅ Intervalo de confiança
- ✅ Distribuição Normal (Z)
- ✅ Distribuição t de Student
- ✅ Variância agrupada
- ✅ Teste de Welch (variâncias diferentes)
- ✅ Graus de liberdade ajustados

### Condições de Aplicação

| Situação | Teste | Distribuição | Pressupostos |
|----------|-------|--------------|-------------|
| 1 amostra grande | Z | Normal | n>30 |
| 2 amostras grandes | Z | Normal | n₁,n₂>30 |
| 2 amostras pequenas, σ₁²=σ₂² | t (agrupado) | t-Student | n₁,n₂<30, igualdade de variâncias |
| 2 amostras pequenas, σ₁²≠σ₂² | t-Welch | t-Student | n₁,n₂<30, variâncias diferentes |

---

## 💡 Interpretação dos Resultados

### Questão 1
O teor alcoólico médio dos vinhos tintos (10,423%) é **significativamente diferente** de 10,0% com 95% de confiança.

### Questão 2
Há diferença significativa no teor alcoólico entre vinhos tintos (10,423%) e brancos (10,514%), apesar da pequena diferença aparente (0,091%), com α=0,05.

### Questão 3
A acidez volátil dos vinhos tintos (0,616) é **significativamente maior** que a dos brancos (0,253), com diferença extremamente significativa (t=8,35).

### Questão 4
O pH dos vinhos tintos (3,355) é **significativamente maior** que o dos brancos (3,187), refletindo maior acidez nos brancos, com α=0,05.

---

## 📚 Referências

- **Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009)**
  *Modeling wine preferences by data mining from physicochemical properties*
  Decision Support Systems, 47(3), 547-553

- **UCI Machine Learning Repository**
  Wine Quality Dataset (id=186)
  https://archive.ics.uci.edu/dataset/186/wine+quality

---

## ✅ Status da Atividade

- ✅ Situação 1 elaborada e resolvida
- ✅ Situação 2 elaborada e resolvida
- ✅ Situação 3 elaborada e resolvida
- ✅ Situação 4 elaborada e resolvida
- ✅ Pseudocódigos implementados
- ✅ Explicações detalhadas de cada pseudocódigo
- ✅ Documento LaTeX compilável
- ✅ Pronto para apresentação ao professor

---

**Data de Conclusão:** 08/junho/2026
**Aluno:** Jafte Carneiro Fagundes da Silva
**Disciplina:** Métodos Quantitativos — PUCPR
