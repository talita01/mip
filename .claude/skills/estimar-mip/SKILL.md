---
name: estimar-mip
description: Estima a Matriz de Insumo-Produto do Brasil (68 setores) para um ou mais anos a partir das TRU oficiais do IBGE, com o pipeline mipcore (método híbrido de preços básicos), executando o ciclo completo - verificação de dados, geração, double check independente e relatório rotulado. Use quando a usuária pedir para estimar/gerar/atualizar uma MIP.
---

# Estimar MIP Brasil (68 setores) com o mipcore

Você vai estimar a MIP nacional para o(s) ano(s) pedido(s), seguindo o protocolo de
execução do projeto (rigor metodológico, nada inventado, double check independente,
resultado rotulado ✅/⚠️). A fonte de verdade metodológica é
`Manual-Metodologico-Insumo-Produto.md` (§1.4 validação, §2.4 método híbrido) — em caso
de dúvida ou divergência, o manual prevalece sobre estas instruções.

## Entradas

- **Ano(s)**: vêm como argumento (ex.: `/estimar-mip 2021` ou `/estimar-mip 2019 2020 2021`).
  Sem argumento: pergunte, ou ofereça o ano mais recente com TRU nível 68 disponível.

## Etapa 0 — Pré-checagens (não pule)

1. Venv FORA do OneDrive: `~/.venvs/fgv-mip`. Teste:
   `~/.venvs/fgv-mip/bin/python -c "import mipcore; print(mipcore.__version__)"`.
   Se falhar por caminho (o vault já mudou de `10_Projetos/` para `30_Areas/` uma vez),
   reinstale: `~/.venvs/fgv-mip/bin/pip install -e "<pasta-mip>/MIP"`.
2. Dados do ano: as TRU nível 68 ficam em `MIP/dados/brutos/` (arquivos `68_tab*_{ano}.xls`).
   - Se o ano não estiver lá, verifique a disponibilidade no FTP do IBGE
     (https://ftp.ibge.gov.br/Contas_Nacionais/Sistema_de_Contas_Nacionais/), baixe e
     salve em `MIP/dados/brutos/`.
   - Estado conhecido em jun/2026: TRU nível 68 existe para 2010–2021; 2022+ só nível 12
     preliminar.
   - **Ano sem TRU 68 (2022+): use a Etapa 1-B (projeção GRAS)**, que exige as TRU nível
     12 do ano-alvo E do ano-base em `MIP/dados/brutos/tru_n12/` (`12_tab{1,2}_{ano}.xls`;
     extraia de `nivel_12_2000_2022_xls.zip` ou baixe do FTP). Se nem o nível 12 do ano
     existir, diga isso honestamente e pare.

## Etapa 1 — Gerar

**1-A (ano COM TRU 68, 2010–2021):**

```
~/.venvs/fgv-mip/bin/python "<pasta-mip>/MIP/gerar_matrizes_estimadas.py" <anos...>
```

Saída: `MIP/dados/estimadas/MIP-BR-mipcore-68S-{ano}.xlsx` (abas: Referência, Usos SxS,
Mat A Coef Tec, Inv Leontief, Indicadores). O script já aborta com `assert` se as
identidades contábeis das TRU ou os controles de Leontief falharem — se abortar,
reporte o erro na hora, sem amortecimento, e não entregue o arquivo.

**1-B (ano SEM TRU 68, 2022+ — projeção GRAS, manual §2.5):**

```
~/.venvs/fgv-mip/bin/python "<pasta-mip>/MIP/gerar_matriz_gras.py" <alvo> <base>
```

(base = último ano com TRU 68, hoje 2021). Saída: `MIP-BR-mipcore-GRAS-68S-{alvo}.xlsx`.
Deixe explícito no relatório: camada de confiabilidade INFERIOR (incerteza ~3% média /
~13–14% máx nos multiplicadores, pelo backcast de `MIP/validar_ras.py`), e que a matriz
NÃO serve para SDA/mudança estrutural. O algoritmo GRAS segue Lenzen, Wood & Gallego
(2007) — fonte na pasta.

## Etapa 2 — Double check independente (além dos asserts do script)

Rode em Python (venv) e reporte os números:

1. **Controles internos**: `max|L·f − g|` (esperado < 1e-6) e `max colsum A < 1`
   (o script imprime ambos).
2. **Continuidade temporal**: correlação de Pearson entre `A` do ano e `A` do ano
   adjacente disponível — esperado r ≥ 0,99 (matrizes técnicas mudam devagar).
3. **Benchmark externo, quando existir**: para 2010–2018 há matrizes de Guilhoto
   (`MIP-BR-CN10-68S-{ano}.xlsx`, na raiz da pasta) — compare os multiplicadores de
   produção tipo I; desvio médio esperado ≈ 1,8% (referência: manual §1.4). Para a MIP
   oficial 2015, desvio esperado 0,15%. Desvio muito acima disso = investigar antes de
   entregar (lembrete histórico: códigos numéricos na TRU 2016 já inflaram
   multiplicadores em ~10% até a correção no `mipcore.tru._cod`).
4. **Round-trip**: reabra o xlsx gerado e confira que `L` lida ≡ `L` calculada.

## Etapa 3 — Relatório

Primeira frase com o resultado (ano, arquivo, veredito). Depois: tabela curta com os
controles da Etapa 2 e seus valores, rotulados ✅/⚠️. Declare sempre:

- método: híbrido (§2.4 do manual), tecnologia do setor D·Bn (IBGE, 2018);
- limitações do ano (TRU preliminar? margens 45001/46801 são exceções conhecidas do
  bridge de produtos);
- o que NÃO foi verificado, se algo ficou de fora.

Nunca apresente um número de validação que você não acabou de calcular nesta execução.
