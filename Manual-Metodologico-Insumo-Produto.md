---
title: Manual Metodológico — Análise de Insumo-Produto (MIP)
projeto: FGV-Bioeconomia
tipo: metodologia
classe: quantitativa
area: economia
data: 2026-06-02
atualizado: 2026-06-10 (verificação ponto a ponto contra fontes primárias; ferramental ampliado)
status: referência
---

# Manual Metodológico — Análise de Insumo-Produto (MIP)

> **Propósito.** Documento de referência para sustentar *diferentes* análises de insumo-produto (estimação da matriz, multiplicadores, encadeamentos, extensões regionais e conta-satélite de bioeconomia), ancorado em fontes oficiais (IBGE) e na literatura publicada.
>
> **Convenção de fontes — leitura obrigatória.** Para não misturar fonte com inferência, cada afirmação relevante é marcada:
> - ✅ **Verificado em fonte primária** (com a referência e a página/equação).
> - ⚠️ **Lacuna / não especificado nas fontes consultadas** — sinalizado como tal, sem preenchimento por conta própria.
> - 🔁 **Analogia explícita** a partir de uma definição da fonte (declarada como tal, não como dado original).
>
> Todas as referências seguem a **ABNT NBR 6023:2018** (seção [Referências](#referências)). Citações no texto em sistema autor-data (NBR 10520).

---

## Sumário

1. [Fontes de dados oficiais do IBGE — os identificadores reais (Fase 0)](#1-fontes-de-dados-oficiais-do-ibge--os-identificadores-reais-fase-0)
2. [Passagem a preços básicos](#2-passagem-a-preços-básicos)
3. [Construção da matriz de coeficientes técnicos — modelo oficial do IBGE](#3-construção-da-matriz-de-coeficientes-técnicos--modelo-oficial-do-ibge)
4. [Caixa de ferramentas analítica](#4-caixa-de-ferramentas-analítica)
5. [Extensões para bioeconomia (conta-satélite)](#5-extensões-para-bioeconomia-conta-satélite)
6. [Extensões regionais e inter-regionais](#6-extensões-regionais-e-inter-regionais)
7. [Confiabilidade, agregação e desagregação setorial](#7-confiabilidade-agregação-e-desagregação-setorial)
8. [Refinamentos e lacunas — estado da arte vs. materiais de base](#8-refinamentos-e-lacunas)
9. [Guia de decisão: qual método para qual análise](#9-guia-de-decisão-qual-método-para-qual-análise)
10. [Referências](#referências)

---

## 1. Fontes de dados oficiais do IBGE — os identificadores reais (Fase 0)

✅ O IBGE produz a Matriz de Insumo-Produto (MIP) **a partir das Tabelas de Recursos e Usos – TRU** das Contas Nacionais, em **duas etapas**: (1ª) compilação de fontes e construção dos quadros básicos de produção e consumo; (2ª) aplicação de um modelo matemático que, a partir desses quadros e de hipóteses sobre a tecnologia, calcula a matriz de coeficientes técnicos segundo o modelo de Leontief (IBGE, 2018, Apresentação).

✅ A partir das matrizes de 2000 e 2005, as MIP industriais **deixaram de se basear em Censos Econômicos** e passaram a se basear na **Pesquisa Industrial Anual – Empresa (PIA-Empresa)** (IBGE, 2018, Introdução). O Sistema de Contas Nacionais segue o **System of National Accounts 2008 (SNA 2008)** e a classificação integrada à **CNAE 2.0** (IBGE, 2018, Apresentação).

> ⚠️ **ADVERTÊNCIA DE VIGÊNCIA (jun. 2026): este manual descreve a série SCN referência 2010, que está em substituição.** O IBGE confirma a implantação da **nova série referência 2021**, com primeira publicação do SCN Anual prevista para **2026** e, em seguida, reformulação de todo o sistema, **inclusive a Matriz de Insumo-Produto**, compatibilizada com o novo marco; a nova série incorpora "sempre que possível" as recomendações do **SNA 2025** (não mais o SNA 2008) e traz atualização das classificações (IBGE, *Nota Técnica 01/2024 — Implantação da Série do SCN, Ano base 2021*, 29 abr. 2024, ✅ lida diretamente; IBGE, *Nota Metodológica nº 1*, 2025). **Consequências para este manual:** (i) a MIP oficial 2015, a série TRU nível 68 (2010–2021) e as equações (1)–(12) baseadas na publicação nº 62 permanecem a referência **corrente**, mas tornam-se legado quando a série 2021 sair; (ii) o número de produtos/atividades, a versão da CNAE e a data exata da nova MIP **ainda não são públicos** (só a nota introdutória existe) — não há como antecipá-los sem inventar; (iii) o IBGE divulgou o SCNA de 2021 ainda na metodologia 2010 para permitir comparação e retropolação, o que dá uma ponte entre as séries. **Gatilho de revisão deste manual: a publicação da série referência 2021 (a partir de 2026).**

### 1.1 Composição das TRU — Quadro 1 (notação oficial)

✅ Matrizes em maiúsculas; vetores (sempre colunas) em minúsculas (IBGE, 2018, "Estrutura básica de dados", Quadro 1):

| Símbolo | Significado |
|---|---|
| **V** | Matriz de produção (valor bruto da produção de cada produto por atividade) |
| **q** | Vetor do valor bruto da produção total **por produto** |
| **g** | Vetor do valor bruto da produção total **por atividade** |
| **Un** | Matriz de consumo intermediário **nacional** |
| **Um** | Matriz de consumo intermediário **importado** |
| **Fn** | Demanda final por produtos **nacionais** |
| **Fm** | Demanda final por produtos **importados** |
| **E** | Demanda final por atividade (calculada a partir de *Fn*) |
| **Tp** | Impostos/subsídios sobre produtos absorvidos como insumo pelas atividades |
| **Te** | Impostos/subsídios sobre produtos absorvidos pela demanda final |
| **y** | Vetor (matriz) de valor adicionado bruto por atividade |

✅ As TRU **não distinguem** origem nacional/importada; o modelo de insumo-produto exige esse detalhamento do consumo intermediário e final por origem (IBGE, 2018, "Estrutura básica de dados").

### 1.2 As tabelas publicadas pelo IBGE — identificadores exatos

✅ Publicação: **IBGE. *Matriz de insumo-produto: Brasil: 2015*. Rio de Janeiro: IBGE, 2018. 60 p. (Contas Nacionais, ISSN 1415-9813, n. 62). ISBN 978-85-240-4465-6.** Conteúdo (Sumário, IBGE, 2018):

**Grupo 1 — Tabelas básicas 2015**
1. Recursos de bens e serviços
2. Usos de bens e serviços
3. Oferta e demanda da produção nacional a preço básico
4. Oferta e demanda de produtos importados a preço básico
5. Destino dos impostos sobre produtos nacionais
6. Destino dos impostos sobre produtos importados
7. Destino da margem de comércio sobre produtos nacionais
8. Destino da margem de comércio sobre produtos importados
9. Destino da margem de transporte sobre produtos nacionais
10. Destino da margem de transporte sobre produtos importados

**Grupo 2 — Tabelas derivadas 2015**
11. Matriz dos coeficientes técnicos dos insumos nacionais — **Matriz Bn**
12. Matriz dos coeficientes técnicos dos insumos importados — **Matriz Bm**
13. Matriz de participação setorial na produção dos produtos nacionais — **Matriz D (Market Share)**
14. Matriz dos coeficientes técnicos intersetoriais — **Matriz D.Bn**
15. Matriz de impacto intersetorial — **Matriz de Leontief**

**Anexos:** 1 — Classificação de atividades da MIP e correspondência com a CNAE 2.0 (nível 67); 2 — Classificação de produtos da MIP e correspondência com a CNAE 2.0 (nível 127).

> 📌 **Implicação prática crucial.** As **Tabelas 5 a 10** são exatamente o "destino" (distribuição célula a célula) de impostos e margens que, na ausência de dados, o método de Guilhoto e Sesso Filho (2005) precisa *estimar* (ver §2.2). Quando o IBGE já publicou essas tabelas para o ano, **a distribuição é dado observado, não estimativa**.

### 1.3 Níveis de desagregação e acesso

✅ Níveis divulgados: **12×12** (impresso na publicação) e **67 atividades × 127 produtos** (portal do IBGE) (IBGE, 2018, nota 2). ⚠️ O nível **20×20** circula em distribuições do portal, mas **não é mencionado no texto da publicação digital verificada** — confirmar no portal antes de citar.

### 1.4 Inventário de bases de dados disponíveis na pasta (10 jun. 2026)

✅ Identificação feita nas abas "Referência" / cabeçalhos dos próprios arquivos:

| Base | Arquivo(s) | Conteúdo e fonte declarada |
|---|---|---|
| TRU oficiais, nível 68 | `MIP/dados/brutos/tru_anos/68_tab1/2_{2010–2021}.xls` | IBGE/SIDRA; insumo do pipeline `mipcore` |
| TRU a preços do ano anterior | `MIP/dados/brutos/tru_ano_anterior/68_tab3/4_{2011–2021}.xls` | IBGE (extraídas do zip em 10 jun. 2026); ano *t* valorado a preços de *t−1* — viabilizam SDA a preços constantes por pares encadeados (`mipcore.sda`) |
| MIP oficial 2015, nível 67 | `MIP/dados/brutos/Matriz_de_Insumo_Produto_2015_Nivel_67.xls` | IBGE (publicação nº 62); abas 01–15 |
| **MIP estimadas 2010–2018, 68 setores** | `MIP-BR-CN10-68S-{2010…2018}.xlsx` | "Sistema de Matrizes de Insumo-Produto para o Brasil — 68 setores", **Guilhoto**, estimadas em jan. 2020 (SCN nov. 2019), 68 setores × 128 produtos, referência 2010, **pela metodologia do §2.2** (a aba Referência exige citar GUILHOTO; SESSO FILHO, 2005; 2010). Trazem Produção, Usos P×S e S×S, **matriz A e inversa de Leontief prontas**, importações, impostos e margens |
| **MIP estimadas 2019–2021, 68 setores (mipcore)** | `MIP/dados/estimadas/MIP-BR-mipcore-68S-{2019,2020,2021}.xlsx` | Geradas em 10 jun. 2026 pelo pipeline `mipcore` (validado, §1.4) com `MIP/gerar_matrizes_estimadas.py` — **estendem a série de Guilhoto** (que para em 2018) até o último ano com TRU nível 68 publicada. Abas: Referência (método + citações), Usos SxS, Mat A, Inv Leontief, Indicadores (g, f, VAB, multiplicadores, R-H). Continuidade verificada: r(A) ≥ 0,99 entre anos consecutivos; round-trip das planilhas em precisão de máquina |
| **MIP projetada 2022, 68 setores (GRAS)** | `MIP/dados/estimadas/MIP-BR-mipcore-GRAS-68S-2022.xlsx` | Gerada em 11 jun. 2026 com `MIP/gerar_matriz_gras.py` (método e validação na §2.5) — **camada de confiabilidade inferior**: estrutura de 2021 rebalanceada aos agregados da TRU nível 12 de 2022 via GRAS. Controles: r(A vs 2021)=0,997; VBP total = nível 12 publicado (exato); round-trip em precisão de máquina; multiplicadores movem 1,8% em média vs 2021. Incerteza esperada (backcast): ~3% médio / ~13–14% máx nos multiplicadores. NÃO usar para SDA |
| **TRU nível 12, 2019–2022 (abas extraídas)** | `MIP/dados/brutos/tru_n12/12_tab{1,2}_{2019..2022}.xls` (+ tab3/tab4 de 2022) | Extraídas de `nivel_12_2000_2022_xls.zip` em 11 jun. 2026 — insumo das margens da projeção GRAS (§2.5). O zip cobre 2000–2022; **2023 não está na cópia local** |
| **MIP inter-regional 27 UFs, 2008** | `MIP-26x26-BR-2008.xlsx` | "Matriz inter-regional de Insumo-Produto para o Brasil 2008 — 26 setores", 27 UFs, ano-base 2000, **Guilhoto** (a aba Referência exige citar GUILHOTO et al., 2010 — MIP-Nordeste; metodologia do §6.1) |
| **MIP inter-regional RMSP, 2008** | `Matriz_RMSP_2008.xlsx` | "Matriz Interregional de Insumo-Produto para a Região Metropolitana de São Paulo, 2008", **Haddad, Faria e Vieira** (NEREUS; base metropolitana relacionada ao §6.4), municípios da RMSP × setores |
| **MIIP interestadual 27 UFs, 2011 (IIOAS)** | `administrador,+IIOAS_Brasil_RBERU_2017.xlsx` | 27 UFs × 68 setores, com `A`, `I-A` e `B=(I-A)⁻¹` **prontas** (núcleo 1836×1836). ✅ Validada (sistema de Leontief consistente, ver §6.3). Fonte: HADDAD; GONÇALVES JUNIOR; NASCIMENTO (2017). Adicionada em 16 jun. 2026 |
| **MIIP interestadual 27 UFs, 2019 (IIOAS)** | `IIOAS_BRUF_2019.xlsx` (dentro de `IIOAS_BRUF_2019 (1).rar`, ~115 MB) | 27 UFs × 68 setores × 128 produtos; matrizes de **fluxo** `MIIP SS`/`MIIP PS`/`Produção` (A/L a derivar). Fonte: HADDAD; ARAÚJO; ROCHA; VALE (2025). Contas socioambientais do resumo não vêm neste arquivo. Adicionada em 16 jun. 2026 |
| **Artigos IIOAS / EGC espacial (PDFs)** | `document.pdf` (IIOAS 2011, RBERU 2017), `7_1225ed.pdf` (MIIP 2019, RBERU 2025), `administrador,+02+Haddad+et+al._..._2013.pdf` (EGC anomalias climáticas, RBERU 2013) | Fundamentam §§6.2–6.4. Todos ✅ lidos diretamente em 16 jun. 2026 |
| **Teoria de IO — Guilhoto/Sonis/Hewings (5 PDFs SSRN, após dedup)** | `ssrn-2417397` (MPM inter-regional), `ssrn-2420129`/`ssrn-2420472` (ligações/setores-chave, EN/PT), `ssrn-2414028` (Leontief: antecedentes), `ssrn-2408067` (National IO Table of Brazil) | Adicionados em 16 jun. 2026. **Novo método extraído: MPM (§4.15)**; fontes primárias de §4.5 e §4.8. MPM e "new perspectives" ✅ lidos diretamente. Removidas em 16 jun. 2026 as cópias redundantes `ssrn-1900073` (= Guilhoto 2011), `ssrn-1836495` (= GS2010) e `ssrn-2417390` (= `ssrn-2414028`) |
| **Comércio em valor adicionado / GVC (2 PDFs)** | `Koopman-Wang-Wei-2014-Tracing-ValueAdded-NBER18579.pdf`, `Borin-Mancini-2019-Measuring-GVC-WB8804.pdf` | Baixados e ✅ lidos diretamente em 17 jun. 2026; base da nova §4.16 (decomposição de exportações brutas). KWW = decomposição canônica; Borin-Mancini = padrão atual da OMC |
| CNT — tabelas complementares | `Tab_Compl_CNT.zip` (→ `Tab_Compl_CNT_1T26.xls`) | Contas Nacionais Trimestrais, 1º tri. 2026 (complementa o módulo `cnt` do `mipcore`) |
| TRU nível 12 | `MIP/dados/brutos/tru_n12/12_tab2_{2021,2022}.xls` | IBGE/SIDRA |

> 📌 **Oportunidade de validação:** para 2010–2018 existem, na mesma pasta, as TRU oficiais **e** as MIP estimadas por Guilhoto com a metodologia do §2.2 — permite validar o pipeline próprio (`mipcore`) comparando matriz A, inversa de Leontief e multiplicadores contra as planilhas de Guilhoto, ano a ano (espelhando o teste de aderência de GUILHOTO; SESSO FILHO, 2005, §2.2: Pearson nos valores, Spearman nas ordenações).
>
> ✅ **Validação executada — série completa 2010–2018 (10 jun. 2026, `mipcore` × planilhas de Guilhoto, 68 setores alinhados por código):** identidades contábeis das TRU fecham em 0 em todos os anos; controles internos ok ($\max|Ly-g| \approx 10^{-10}$; $v'Ly = \Sigma VAB$; nenhuma coluna de $A \ge 1$). *(Tabela abaixo: método $r_{int}$ vigente à época; com o método híbrido adotado em seguida — §2.4 — os números melhoram: desvio médio dos multiplicadores 1,84% na série Guilhoto e r(L)=1,0000/desvio 0,15% contra a MIP oficial 2015.)*
>
> | ano | r(A) | r(L) | r(MP) | ρ(MP) | desv.% | chave ∩/mip/G |
> |---|---|---|---|---|---|---|
> | 2010 | 0,963 | 0,998 | 0,986 | 0,981 | 2,32 | 31/34/37 |
> | 2011 | 0,961 | 0,997 | 0,985 | 0,979 | 2,31 | 34/36/39 |
> | 2012 | 0,958 | 0,997 | 0,986 | 0,973 | 2,29 | 33/35/39 |
> | 2013 | 0,958 | 0,997 | 0,987 | 0,982 | 2,37 | 32/34/37 |
> | 2014 | 0,958 | 0,997 | 0,989 | 0,979 | 2,54 | 31/34/36 |
> | 2015 | 0,951 | 0,997 | 0,988 | 0,982 | 2,35 | 32/34/38 |
> | 2016 | 0,950 | 0,997 | 0,988 | 0,983 | 2,47 | 34/36/37 |
> | 2017 | 0,948 | 0,997 | 0,988 | 0,984 | 2,30 | 35/37/38 |
> | 2018 | 0,950 | 0,997 | 0,986 | 0,978 | 2,51 | 34/36/36 |
>
> (r = Pearson; ρ = Spearman; MP = multiplicadores de produção; desv.% = desvio relativo médio dos MP; "chave" = setores com índice R-H para trás > 1 em comum / no `mipcore` / em Guilhoto.) Magnitudes compatíveis com a aderência reportada em GUILHOTO; SESSO FILHO (2005). As maiores divergências setoriais (|dif| de MP até ~0,15) concentram-se em alimentos (1091–1093), açúcar, madeira e transporte aéreo — esperadas: o `mipcore` usa a estrutura oficial de margens/impostos da MIP 2015 (§2.1) e Guilhoto a distribuição por $\alpha_{ij}$ (§2.2), cuja margem de comércio é a fonte de erro reconhecida.
>
> 📌 **Achado da validação (registro de transparência):** a 1ª rodada acusou desvio anômalo de 10,3% em 2016; a causa era um **bug silencioso de leitura** — no arquivo `68_tab1_2016.xls` os códigos de produto vêm como células numéricas (`1911.0`) em vez de texto (`"01911"`), o que quebrava a ponte de códigos da passagem a preços básicos (o `r_int` caía no default 1,0 para os 128 produtos). Corrigido no `mipcore.tru` (normalização com zero-padding) em 10 jun. 2026; após a correção, 126/128 produtos casam em todos os anos 2010–2021 (exceções documentadas: produtos 45001 e 46801, comércio, sem correspondente no mapa da MIP 2015 — usam $r_{int}=1$).
>
> ✅ **Triângulo com a MIP oficial (2015, 10 jun. 2026):** agregando o pipeline `mipcore` de 68 para 67 atividades (única fusão: 4500 + 4680 → 4580, comércio) e comparando com as **Tabelas 14 (D·Bn) e 15 (Leontief) oficiais do IBGE**: Pearson 0,945 (matriz A), **0,996 (inversa de Leontief)**; multiplicadores: Pearson 0,982, Spearman 0,968, desvio relativo médio 2,93% (médias 1,773 vs 1,812). Maiores divergências: Fabricação de produtos do fumo (1200), Fabricação de bebidas (1100), Outros produtos alimentares (1093), Abate e carne (1091), Transporte aéreo (5100) — novamente setores de margens/impostos pesados. Conclusão prática: o custo de usar o pipeline próprio (ou matriz estimada) em vez da oficial é da ordem de **~3% nos multiplicadores**, concentrado nesses setores; para análises que dependam criticamente deles em 2015, usar a matriz oficial.
>
> 📌 `liv101604.pdf` era duplicata byte-idêntica de `IBGE-2018-MIP-Brasil-2015-liv101604.pdf` e foi removida em 16 jun. 2026 (mantida a cópia de nome descritivo).

✅ Anos de referência das MIP do IBGE no novo SCN: **2000, 2005, 2010 e 2015** (IBGE, 2018; IBGE, *Matriz de Insumo-Produto*, página institucional). ✅ **Conferido no FTP do IBGE em 10 jun. 2026:** a MIP de 2015 segue sendo a oficial mais recente; as TRU nível 68 vão até **2021** (2022–2023 só em nível 12, preliminar); há também a série **nível 51 (2000–2021)**, mais longa, ainda não baixada.

⚠️ **Códigos SIDRA específicos por tabela:** as fontes consultadas confirmam que as TRU (55 atividades × 110 produtos) e as MIP estão no portal/SIDRA, mas **não localizei, em fonte verificável, os números de tabela SIDRA individuais**. Acesso confirmado por: portal `ibge.gov.br/estatisticas/economicas/contas-nacionais/9085-matriz-de-insumo-produto.html` e FTP `ftp.ibge.gov.br/Contas_Nacionais/Matriz_de_Insumo_Produto/` (formato `.ods`). Não atribuo números SIDRA sem fonte.

---

## 2. Passagem a preços básicos

O consumo nas TRU está a **preços de consumidor** = preço básico + impostos (líquidos de subsídios) + margens de comércio e transporte (IBGE, 2018, Introdução). Há **dois caminhos**, conforme a disponibilidade de dados:

### 2.1 Caminho oficial do IBGE (dados definitivos)

✅ Retiram-se dos valores a preços de consumidor as parcelas de margens de comércio/transporte e os impostos líquidos de subsídios; essas parcelas são realocadas ao consumo dos produtos *comércio* e *transporte*, e criam-se linhas de impostos (IBGE, 2018, "Estrutura básica de dados"). A valoração a **preços básicos** é preferida por dar maior homogeneidade (margens e impostos variam por razões alheias ao processo produtivo).

✅ **Refinamento desde a MIP 2010 (ajuste CIF/FOB):** como produtos importados são valorados a preços CIF (incluindo frete e seguro) e esses serviços também constam na oferta, faz-se um ajuste para descontar essa parcela da oferta; o SNA 2008 recomenda registrar o ajuste dos serviços nacionais de transporte/seguro como uma importação e uma exportação de igual valor. **Objetivo declarado: evitar importações negativas e, consequentemente, coeficientes técnicos negativos para o produto importado** (IBGE, 2018, "Estrutura básica de dados").

✅ Distribuição de impostos sobre valor adicionado (ICMS, IPI): por atividade, conforme a estrutura de dedução de cada imposto/produto/atividade, gerando as Tabelas 5 e 6; imposto de importação distribuído proporcionalmente entre atividades consumidoras e demanda final (IBGE, 2018, "Passagem de preço de consumidor para preço básico"). Software de apoio: **ERETES** (IBGE, 2018, nota 3).

### 2.2 Caminho de Guilhoto–Sesso Filho (dados *preliminares*)

Aplicável quando o IBGE ainda não publicou as Tabelas 5–10 para o ano desejado. ✅ Algoritmo (GUILHOTO; SESSO FILHO, 2005, seções 2.1–2.2):

1. Organizar a Matriz de Uso a preços de mercado ($Z_{i,j}$ = produto *i* vendido ao destino *j*). Remover o **Dummy Financeiro** (zerar coluna; subtrair do Total da Atividade e da Demanda Total) — ele não recebe coeficientes.
2. Coeficientes de alocação (eq. 1):
$$\alpha_{ij} = \frac{Z_{i,j}}{\displaystyle\sum_{j=1}^{n} Z_{i,j}}$$
3. Distribuir os **totais por produto** de MGC, MGT, ICMS, IPI/ISS e OIIL multiplicando-os por $\alpha_{ij}$.
4. **Importação e imposto de importação (tratamento diferenciado):** zerar a coluna de **exportação** e subtraí-la da Demanda Final/Total; recalcular novos $\alpha_{ij}$; distribuir IMP e IIMP; reinserir o Dummy Financeiro.
5. Subtrair todas as parcelas da matriz a preços de mercado → **Matriz de Uso a preços básicos** (por resíduo).

✅ **Identidades** (GUILHOTO; SESSO FILHO, 2005, p. 3): $PB = PC - MGC - MGT - IIL$; $ONPB = OG_{PC} - OI - MGC - MGT - IIL$.

✅ **Validade:** os indicadores da matriz estimada não diferem estatisticamente dos da matriz oficial — Pearson nos valores e Spearman nas ordenações, este testado a $\alpha = 0{,}01$ (GUILHOTO; SESSO FILHO, 2005, §4, p. 22) — para 1994 e 1996 com **42 setores** (o número não consta legível na cópia local de 2005, mas é afirmado em GUILHOTO; SESSO FILHO, 2010, p. 57), e para 2005 com **55 setores** no novo SCN, Pearson/Spearman significativos a 1% para todos os indicadores (GUILHOTO; SESSO FILHO, 2010, p. 57 e Tabela 4, p. 61).

✅ **Viés conhecido da estimativa:** a matriz estimada tende a **superestimar** os multiplicadores, principalmente os de **tipo II** (efeito induzido), com maiores desvios em comércio e serviços (GUILHOTO; SESSO FILHO, 2010, §3 e conclusões, p. 56-61).

✅ **Limitação reconhecida pelos autores:** a distribuição da **margem de comércio** entre consumo intermediário e demanda final é a principal fonte de erro (GUILHOTO; SESSO FILHO, 2005, considerações finais). → Hoje, parcialmente superada quando se usam as Tabelas 7–10 oficiais (§1.2).

### 2.3 Atualização de matrizes — método RAS (ajuste biproporcional)

Complementar ao §2.2: usa-se quando se tem a matriz de coeficientes $A(0)$ de um **ano-base** e, para o **ano-alvo**, apenas três informações marginais: produção bruta $x(1)$, vendas intermediárias por linha $u(1)$ e compras intermediárias por coluna $v(1)$.

✅ Procedimento iterativo (MILLER; BLAIR, 2009, §7.4, p. 313-318): estimativa inicial $Z^0 = A(0)\,\hat{x}(1)$; ajuste de linhas $\hat{r}^1=[\hat{u}(1)](\hat{u}^0)^{-1}$, $A^1=\hat{r}^1A(0)$ (eqs. 7.8–7.9); ajuste de colunas $\hat{s}^1$, $A^2=A^1\hat{s}^1$ (eqs. 7.13–7.14); alternam-se ajustes até a convergência, resultando na forma que dá nome ao método:
$$A(1) \approx \hat{r}\,A(0)\,\hat{s} \quad \text{(eq. 7.16)}$$

✅ **Interpretação econômica:** fatores de linha $r_i$ = efeito **substituição** (mudança da participação do insumo *i* na economia); fatores de coluna $s_j$ = efeito **fabricação** (mudança na proporção insumos/produção da atividade *j*) — conferida por leitura direta em GUILHOTO (2011, §8.1, p. 50); em Miller e Blair está no §7.4.4 (p. ~328-329, camada de agente).

✅ **Propriedades e limitações** (MILLER; BLAIR, 2009, §7.4): o procedimento **preserva sinais** — nenhum coeficiente positivo vira negativo, pois $r_i, s_j \ge 0$ (p. 329); células conhecidas por pesquisa podem ser **fixadas** antes do ajuste (RAS modificado/informação exógena parcial, §7.4.5, p. 330); perpetua erros de $A(0)$ desatualizada; não separa mudança tecnológica real de mudança de preços relativos.

✅ **GRAS — RAS generalizado para matrizes com células negativas** (LENZEN; WOOD; GALLEGO, 2007, eqs. 3, 6a–9, p. 463-465 — conferido por leitura direta em 11 jun. 2026; exposição **corrigida** do GRAS de JUNIUS; OOSTERHAVEN, 2003, cuja cópia não foi obtida): decompõe-se $A = P - N$ ($P$ = elementos positivos; $N$ = módulos dos negativos); a solução que minimiza a função-objetivo corrigida $t'=\sum_{ij}|a_{ij}|z_{ij}\ln(z_{ij}/e)$ é $x_{ij} = r_i\,a_{ij}\,s_j$ para $a_{ij}\ge 0$ e $x_{ij} = a_{ij}/(r_i s_j)$ para $a_{ij}<0$ (eqs. 6a–6b), com $r_i,\,s_j$ obtidos alternadamente pelas quadráticas $\rho_i = \frac{u_i + \sqrt{u_i^2+4p_i n_i}}{2p_i}$ e $\sigma_j = \frac{v_j+\sqrt{v_j^2+4p_j n_j}}{2p_j}$ (eqs. 8a–8b), onde $p_i=\sum_j p_{ij}s_j$ e $n_i = \sum_j n_{ij}/s_j$ (eq. 9). Lenzen et al. mostram que a formulação original de J&O convergia para margens **escaladas por $e$** ($u^*=eu$) e não devolvia uma estimativa inicial já perfeita; a correção elimina ambos os defeitos (o exemplo numérico da p. 463 é usado como teste unitário do `mipcore.gras`). 📌 Notas de leitura: a eq. (9) impressa tem typo de subscrito ($p_j(s)$ onde o argumento é $r$); o caso-limite $p_i=0$ (linha sem elementos positivos) segue da própria restrição (7a): $r_i = -n_i/u_i$ — tratado em Temurshoev, Miller e Bouwmeester (2013), **fonte não lida**, aqui derivado diretamente.

> 📌 O mesmo RAS é usado na regionalização (MIP-Nordeste, eqs. 74–77 — ver §6.1); em português, GUILHOTO (2011, §8.1, eq. 8.7).

### 2.4 Método adotado pelo projeto — híbrido com benchmark empírico (10 jun. 2026)

✅ **Método:** para anos sem MIP oficial, a passagem a preços básicos do `mipcore` usa as
**participações de destino célula a célula das Tabelas 04–10 oficiais da MIP 2015** aplicadas
aos **totais do próprio ano** (margens, impostos e importações da aba *oferta* da TRU), com
*fallback* nos coeficientes $\alpha_{ij}$ de GUILHOTO; SESSO FILHO (2005, §2.2) onde a estrutura
de 2015 é vazia, tratamento de importações + imposto de importação com exclusão da coluna de
exportação (como em §2.2), e realocação das margens às linhas de comércio (45001/46801,
divididas pela produção relativa) e transporte (49001/50001, pela fração observada em 2015,
~99% terrestre). Implementação: `mipcore.precos_basicos.uso_basico_hibrido`.

✅ **Justificativa empírica (benchmark fora da amostra):** reconstruindo a **Tabela 03 oficial
de 2010** (uso nacional a preços básicos, 127×67) a partir da Tabela 02 — um transporte de
estrutura de 5 anos, análogo ao uso em 2019–2021:

| Método | WMAPE | Pearson | WMAPE nas linhas de margem |
|---|---|---|---|
| razão $r_{int}$ por produto (método anterior do `mipcore`) | 16,45% | 0,973 | 63,3% |
| Guilhoto–Sesso 2005 puro ($\alpha_{ij}$ do próprio ano) | 8,08% | 0,996 | 12,6% |
| **híbrido (shares 2015 × totais do ano)** | **5,46%** | **0,998** | **5,5%** |

A contabilidade do teste foi validada pela identidade exata Tabela 02 = Σ(03…10) com realocação
de margens (erro 0 nas três linhas de margem). O método anterior ($r_{int}$ com clip em 1,0)
tinha um defeito estrutural não documentado: **impedia as linhas de comércio/transporte de
crescer** na passagem a preços básicos (63% de erro nessas linhas) — foi **descontinuado como
padrão** e mantido apenas para reprodutibilidade (`uso_nacional_basico(d, r_int=...)`).

✅ **Efeito nos benchmarks downstream:** contra a MIP oficial 2015 (Tabelas 14–15, agregação
68→67), o pipeline passou de r(L)=0,996/desvio 2,93% para **r(L)=1,0000/desvio 0,15%**; contra
as matrizes de Guilhoto 2010–2018, de desvio médio 2,35% para **1,84%** (r(L)≥0,9987 em todos
os anos).

⚠️ **Hipótese residual declarada:** estabilidade das participações de destino de 2015 — o erro
dessa hipótese, medido no transporte 2015→2010, é o WMAPE de 5,5% acima. Reancorar quando o
IBGE publicar MIP oficial mais recente.

### 2.5 Projeção de anos sem TRU nível 68 — GRAS + TRU nível 12 (11 jun. 2026)

✅ **Problema:** a TRU nível 68 termina em 2021; para 2022+ o IBGE publica apenas a TRU
**nível 12** preliminar. **Método implementado** (`mipcore.gras.estimar`): projeta-se a matriz
de usos $Z$ do último ano com TRU 68 por **GRAS** (§2.3 — obrigatório, não RAS: $Z$ do método
híbrido contém ~1,9% de massa negativa, herdada da realocação de margens), com margens-alvo
construídas escalando as margens do ano-base pelo **crescimento dos 12 blocos do nível 12**
(CI por bloco de produto nas linhas; CI por atividade nas colunas; VBP por atividade para $g$).
O mapeamento 68→12 por faixas de divisão CNAE é **verificado numericamente** a cada execução
contra o VBP publicado (desvio máximo observado: 0,00%). Aproximações declaradas: CI do nível
12 a preços de consumidor transferido como fator de crescimento às margens de $Z$ (básico);
bloco de produto ≈ bloco de atividade; fechamento $\sum u = \sum v$ por reescala de $u$ (fator
1,02 nos testes); bloco com CI nulo (adm. pública) usa o crescimento do VBP; VAB do ano-base
escalado pelo VBP do bloco.

✅ **Validação retroativa fora da amostra** (`MIP/validar_ras.py`; alvo 2021, cuja matriz
verdadeira é conhecida — desvios dos multiplicadores de produção tipo I):

| Variante | base 2020→2021 | base 2019→2021 (2 anos) |
|---|---|---|
| C — ingênuo: $A$(base) sem ajuste | 4,02% médio / 17,4% máx | 4,01% / 10,5% |
| A — GRAS com margens verdadeiras (teto do método) | 0,29% / 2,3% | 0,36% / 2,0% |
| **B — GRAS com margens do nível 12 (realista)** | **2,77% / 14,4%** | **2,99% / 13,0%** |

O gargalo é a informação do nível 12, não o GRAS (teto de 0,3%). Os erros máximos concentram-se
em setores de choque de preço (carvão 14%, siderurgia 14%, transporte aéreo 13%, eletrônicos
13%); setores bio entre 0,1% e 6% (biocombustíveis ~4–6%, agricultura ~2–3%). Nota honesta: no
salto de 2 anos o erro **máximo** da variante realista supera o do ingênuo (13,0% vs 10,5%),
embora a média melhore — para setores específicos de choque, a projeção pode piorar.

⚠️ **Limitações de uso:** a matriz projetada (`MIP-BR-mipcore-GRAS-68S-2022.xlsx`) herda a
estrutura fina do ano-base apenas rebalanceada — **não usar para SDA/mudança estrutural** (a
mudança tecnológica fina é quase nula por construção); adequada para multiplicadores e análise
de impacto corrente, com a incerteza da tabela acima. Camada de confiabilidade declarada na
própria aba Referência do arquivo.

---

## 3. Construção da matriz de coeficientes técnicos — modelo oficial do IBGE

> Esta seção **preenche, com a fonte oficial primária**, a etapa que os papers de Guilhoto–Sesso delegavam a Miller e Blair.
>
> ✅ **Verificação (10 jun. 2026):** as afirmações das Seções 1–3 foram conferidas ponto a ponto contra a cópia local da publicação (`IBGE-2018-MIP-Brasil-2015-liv101604.pdf` — versão digital de 17 p., com o texto metodológico/notas técnicas, **sem** as tabelas de dados): duas etapas de produção, PIA-Empresa/SNA 2008/CNAE 2.0, Quadro 1, sumário das Tabelas 1–15, passagem a preços básicos, ajuste CIF/FOB, distribuição de ICMS/IPI (e nota sobre o ERETES), hipóteses tecnológicas e **equações (1)–(10)** conferem com o original. ⚠️ A cópia termina na eq. (10) e na forma combinada não numerada $q = Bn\,D\,q + fn$ — ver nota abaixo sobre a numeração das duas equações finais.

✅ **Hipótese tecnológica adotada pelo IBGE:** *modelo de tecnologia do setor simples* (industry technology), **sem subprodutos**, em vigor desde as matrizes de 2000. A classificação brasileira sempre adota **mais produtos do que atividades**, o que restringe os modelos àqueles baseados em tecnologia do setor (IBGE, 2018, "As hipóteses utilizadas e os modelos baseados na tecnologia do setor").

✅ **Equações do modelo** (IBGE, 2018, "Cálculo dos coeficientes técnicos"; $\langle x \rangle$ = matriz diagonal; $l$ = vetor-soma unitário):

Valor bruto da produção por produto e por atividade:
$$q = V'l \quad (3) \qquad\qquad q = Un\,l + fn \quad (4) \qquad\qquad g = Vl \quad (6)$$

Matriz de **market-share** (participação setorial na produção) — *Matriz D*:
$$D = V\langle q\rangle^{-1} \quad (7)$$

Matriz de coeficientes técnicos **produto × atividade** dos insumos nacionais — *Matriz Bn*:
$$Bn = Un\,\langle g\rangle^{-1} \quad (8)$$

Relação produção-atividade: $g = D\,q$ (9). Combinando, chega-se aos **dois sistemas de Leontief**:

$$\boxed{q = (I - Bn\,D)^{-1}\,fn} \qquad\text{(produto × produto)}$$
$$\boxed{g = (I - D\,Bn)^{-1}\,D\,fn} \qquad\text{(atividade × atividade)}$$

> ⚠️ **Numeração das duas equações finais:** a cópia digital local termina na eq. (10) e na forma combinada não numerada $q = Bn\,D\,q + fn$; a derivação confirma as **fórmulas** acima, mas os números "(11)" e "(12)" **não puderam ser conferidos** nessa cópia (presumivelmente constam da edição completa de 60 p.). Em trabalho final, citar pelas fórmulas, não pelos números.

onde (IBGE, 2018):
- **D·Bn** = matriz de coeficientes técnicos diretos **atividade × atividade** (Tabela 14) → mais adequada a análises de **relações intersetoriais**;
- **Bn·D** = matriz de coeficientes técnicos diretos **produto × produto** → mais adequada à ótica das **relações tecnológicas**;
- a escolha entre as duas formulações depende **exclusivamente do objetivo do estudo**; nenhuma é teoricamente superior (IBGE, 2018).
- **Tabela 15** = Matriz de impacto intersetorial = inversa de Leontief.

🔁 **Matriz Bm (Tabela 12):** definida pelo IBGE como "coeficientes técnicos dos insumos importados"; por analogia direta à eq. (8), corresponde a $Bm = Um\,\langle g\rangle^{-1}$ (analogia declarada — **verificado em 10 jun. 2026 que o texto da publicação não traz a equação de Bm**, apenas nomeia a Tabela 12; a analogia permanece como tal).

✅ **Duas hipóteses possíveis** (IBGE, 2018): *Hipótese 1 — tecnologia do produto* (tecnologia é característica do produto); *Hipótese 2 — tecnologia do setor* (tecnologia é característica da atividade; insumos pela média ponderada por *market-share*). O IBGE adota a Hipótese 2, variante simples. Os exemplos de subprodutos citados (não tratados): sucata de metal, bagaço de cana-de-açúcar.

---

## 4. Caixa de ferramentas analítica

Notação: $A$ = coeficientes técnicos diretos (= D·Bn na ótica atividade×atividade); $L=(I-A)^{-1}$ = inversa de Leontief, elemento $l_{ij}$; $\bar{L}$ = inversa do modelo fechado (consumo das famílias endogeneizado).

### 4.1 Impacto de demanda
✅ $X = (I-A)^{-1}Y$; $\Delta X = (I-A)^{-1}\Delta Y$; impacto sobre uma variável $V$ (emprego, renda, importações, impostos, valor adicionado): $\Delta V = \hat{v}\,\Delta X$, com $v_i = V_i/X_i$ (GUILHOTO et al., 2010 — *MIP-Nordeste*, eqs. 84–87).

### 4.2 Multiplicadores de produção
✅ **Tipo I** (aberto): $MP_j = \sum_{i=1}^{n} l_{ij}$ (GUILHOTO; SESSO FILHO, 2005, eq. 19). **Tipo II** (fechado, com induzido): $\overline{MP}_j = \sum_{i=1}^{n}\bar{l}_{ij}$ (GUILHOTO; SESSO FILHO, 2010, eq. 2).

### 4.3 Multiplicadores/geradores de emprego, renda, VA e impostos
✅ Coeficiente $C_i^e = e_i/VBP_i$; gerador direto+indireto $G^e = C^e (I-A)^{-1}$; multiplicador $MV_i = GV_i/v_i$, com $GV_j=\sum_i b_{ij}v_i$ (GUILHOTO et al., 2010 — *MIP-Nordeste*, eqs. 88–93). Versões Tipo I (direto+indireto) e Tipo II (com induzido, famílias endogenizadas). ✅ Multiplicadores de emprego Tipo I e II também em GUILHOTO; SESSO FILHO (2010, eqs. 3–4).

### 4.4 Encadeamentos de Rasmussen-Hirschman (setores-chave)
✅ Com $B=(I-A)^{-1}$, $B^*$ = média dos elementos, $L_{\bullet j}$/$L_{i\bullet}$ = somas de coluna/linha (GUILHOTO; SESSO FILHO, 2005, eqs. 2–4):
$$\text{para trás (poder de dispersão): } U_j = \frac{L_{\bullet j}/n}{B^*} \qquad \text{para frente (sensibilidade): } U_i = \frac{L_{i\bullet}/n}{B^*}$$
Valores $>1$ ⇒ setor-chave.

### 4.5 Ligações puras GHS (Guilhoto–Sonis–Hewings)
✅ Corrige o R-H por não ponderar a escala de produção. Partição $A=\begin{bmatrix}A_{jj}&A_{jr}\\A_{rj}&A_{rr}\end{bmatrix}$; $\Delta_j=(I-A_{jj})^{-1}$, $\Delta_r=(I-A_{rr})^{-1}$ (GUILHOTO; SESSO FILHO, 2005, eqs. 5–10):
$$PBL = \Delta_r A_{rj} Y_j \quad(14) \qquad PFL = \Delta_j A_{jr} \Delta_r Y_r \quad(15) \qquad PTL = PBL + PFL \quad(16)$$
Normalizados pela média: $PBLN = PBL/PBLm$, etc. (eqs. 17–18).

> 📌 **Fonte primária e divergência entre formulações (✅ conferidas por leitura direta):** a derivação canônica das ligações puras está em SONIS; GUILHOTO; HEWINGS; MARTINS (*Linkages, Key Sectors and Structural Change: Some New Perspectives* — lido em 16 jun. 2026), via decomposições multiplicativas $L=P_2P_1$ e $L=P_1P_3$ com $P_1=(I-A_r)^{-1}$ (eqs. 17–21). Lá, **PBL e PFL usam a produção total do setor** $q_{jj}$ (não a demanda final): $PBL = i'_{rr}\,\Delta_r A_{rj}\,q_{jj}$ (eq. 26) e $PFL = A_{jr}\Delta_r\,q_{rr}$ (eq. 31), com a justificativa explícita de que, ao isolar o setor, a produção total funciona como o vetor de impacto correto. Há, portanto, três variantes na literatura: (i) GUILHOTO; SESSO FILHO (2005, eq. 14): $PBL=\Delta_r A_{rj}Y_j$ (demanda final); (ii) GUILHOTO (2011, §6.6, eq. 6.23): $PBL=\Delta_r A_{rj}\Delta_j Y_j$ ($\Delta_j$ interposto); (iii) fonte primária: $q_{jj}$ em vez de $Y_j$. Em trabalho aplicado, declarar qual se usa e citar a fonte. (Typo na fonte de 2011: a eq. 6.19 imprime $(I-A_{jj})^{-1}$ onde deveria ser $A_{rr}$.)

### 4.6 Fechamento em relação às famílias — formulação matricial do Tipo II

✅ O modelo é fechado endogeneizando o consumo das famílias via matriz ampliada (MILLER; BLAIR, 2009, §2.5 e §6.2; GUILHOTO, 2011, §3.2, eqs. 3.8–3.12):
$$\bar{A}=\begin{bmatrix}A & h_c\\ h_r' & 0\end{bmatrix} \qquad \bar{L}=(I-\bar{A})^{-1}$$
com $h_r'$ = linha de coeficientes de renda do trabalho ($a_{n+1,j}$ = renda das famílias por unidade de produção de *j*) e $h_c$ = coluna de coeficientes de consumo por unidade de renda. (⚠️ Ao citar GUILHOTO, 2011, cap. 3: a numeração de equações da fonte é **duplicada** — o §3.4 reusa os números 3.10–3.12 já usados no §3.2; citar sempre seção + equação.)

✅ **Leituras úteis** (MILLER; BLAIR, 2009, §6.2, p. 247-254): multiplicador **simples** de renda $m(h)_j=\sum_i a_{n+1,i}\,l_{ij}$ (eq. 6.11); multiplicador **total** de renda $\bar{m}(h)_j = \bar{l}_{n+1,j}$ — o elemento da última linha de $\bar{L}$ (eq. 6.13); Tipo I $= m(h)_j/a_{n+1,j}$ e Tipo II $= \bar{m}(h)_j/a_{n+1,j}$ (eqs. 6.14–6.16). A **razão Tipo II/Tipo I é constante entre setores** (Apêndice 6.2) — atalho computacional: obtidos os Tipo I, os Tipo II saem por um fator único.

✅ **Limitação:** o Tipo I tende a **subestimar** e o Tipo II a **superestimar** os efeitos — "os dois podem ser considerados limites inferior e superior do efeito indireto verdadeiro; uma estimativa realista geralmente fica aproximadamente no meio" (OOSTERHAVEN; PIEK; STELDER, 1986, p. 69, apud MILLER; BLAIR, 2009, p. 253 — conferido por leitura direta). Convergente com o viés de superestimação do Tipo II encontrado empiricamente por GUILHOTO; SESSO FILHO (2010) — ver §2.2.

### 4.7 Modelo de Ghosh e a medida moderna de ligação para frente

✅ Espelho do modelo de Leontief pelo lado da oferta (MILLER; BLAIR, 2009, §12.1): coeficientes de **alocação** $B=\hat{x}^{-1}Z$ (eq. 12.1), inversa de Ghosh $G=(I-B)^{-1}$ (eq. 12.5), modelo $x'=v'G$ (eq. 12.6) e $\Delta x = G'\,\Delta v$ (eq. 12.11). Relações de similaridade com Leontief: $L=\hat{x}\,G\,\hat{x}^{-1}$ e $G=\hat{x}^{-1}L\,\hat{x}$ (eqs. 12.16–12.17).

✅ **Uso recomendado — ligação para frente:** medir a sensibilidade de dispersão pelas **somas de linha de $G$** (e não de $L$), pois $G$ capta a dependência do setor como *vendedor* de insumos (MILLER; BLAIR, 2009, §12.2, p. 555-557). ✅ GUILHOTO (2011, §6.3, eq. 6.9) já adota essa convenção: $U_i = [G_{i\bullet}/n]/G^*$ com a inversa de Ghosh — ou seja, na prática brasileira recente os índices "para frente" de R-H são calculados via Ghosh.

✅ **Advertência central:** a hipótese de coeficientes de alocação estáveis é frágil para projeção de **quantidades** (crítica de Oosterhaven, 1988-89: insumos primários se transmitem para frente sem aumento correspondente de insumos primários nos compradores — §12.1.3, p. 548-549); Dietzenbacher (1997) reinterpreta o modelo de Ghosh como modelo de **preços** (cost-push), com $\pi = (\hat{x}^0)^{-1}x^1(s)$ (eq. 12.18) e a **equivalência exata** com o modelo de preços de Leontief: $\pi = \tilde{p}$ (eqs. 12.20–12.21, p. 553 — "generate exactly the same results"). Ligações para frente diretas e totais: $FL(d)_i = \sum_j b_{ij}$ (eq. 12.28) e $FL(t)_i = \sum_j g_{ij}$ (eq. 12.29), **somas de linha** de $B$ e $G$ (p. 558).

### 4.8 Campo de influência (Sonis–Hewings)

✅ Identifica os **coeficientes diretos cujas variações causam maior impacto estrutural**. Fonte primária: SONIS; HEWINGS (1989, 1994) e HEWINGS; FONSECA; GUILHOTO; SONIS (1989), aplicada ao Brasil; exposição com a razão de determinantes $Q(E)=\det B/\det B(E)$ como polinômio das mudanças incrementais em SONIS; GUILHOTO; HEWINGS; MARTINS (*Some New Perspectives*, §6, eq. 33 — lido em 16 jun. 2026). Formulação operacional (GUILHOTO, 2011, §6.4, eqs. 6.10–6.12): perturbação $\varepsilon$ em $a_{i_0j_0}$, campo
$$F(\varepsilon_{ij})=\frac{\big[B(\varepsilon_{ij})-B\big]}{\varepsilon_{ij}} \qquad S_{ij}=\sum_{k=1}^{n}\sum_{l=1}^{n}\big[f_{kl}(\varepsilon_{ij})\big]^2$$
os maiores $S_{ij}$ marcam os elos críticos da economia.

✅ Em Miller e Blair, o **campo de influência de primeira ordem** é o produto externo da coluna *i* pela linha *j* da inversa: $F[i,j] = L_{\bullet i}\,L_{j\bullet}$, e a variação da inversa por uma mudança em $a_{ij}$ é $\Delta L_{(ij)} = F[i,j]\,k^1_{(ij)}$, com $k^1_{(ij)} = \Delta a_{ij}/(1 - l_{ji}\Delta a_{ij})$ (MILLER; BLAIR, 2009, §12.3.6, p. 578; campos de ordem superior são apenas mencionados, sem fórmulas — nota 33, p. 579). Base matemática verificada no Apêndice 12.1: $l^*_{rs(ij)}=l_{rs}+\dfrac{l_{ri}\,l_{js}\,\Delta a_{ij}}{1-l_{ji}\,\Delta a_{ij}}$ (eq. A12.1.4, p. 585) e $L^* = L + \dfrac{(LC)(RL)}{1-RLC}$ (eq. A12.1.3).

### 4.9 Extração hipotética

✅ Mede a importância de um setor pelo custo de removê-lo (MILLER; BLAIR, 2009, §12.2.6, p. 560-565):
- **Para trás:** zerar a **coluna** *j* de $A$ → $\bar{x}^{(cj)}=[I-\bar{A}^{(cj)}]^{-1}f$; medida $B_j^{(t)} = i'x - i'\bar{x}^{(cj)}$ (% de queda da produção total).
- **Para frente:** zerar a **linha** *j* de $B$ (alocação/Ghosh) → $F_j^{(t)}$ análogo.
- **Total:** zerar linha **e** coluna → $T_j = i'x - i'\bar{x}^{(j)}$.
Normalizações por % do produto total e pela média entre setores (Tabela 12.5, p. 565). Sensível ao nível de agregação setorial.

### 4.10 Modelo de preços de Leontief (repasse de custos)

✅ Dual do modelo de quantidades (MILLER; BLAIR, 2009, §2.6, p. 41-51):
$$p' = p'A + v' \;\Rightarrow\; p=(I-A')^{-1}\tilde{v}$$
com $\tilde{v}$ = valor adicionado por unidade de produção. Um choque de custo $\Delta v$ (imposto, energia, salários) repassa-se **para a frente** na cadeia: $\Delta p = (I-A')^{-1}\Delta\tilde{v}$. A dualidade é completa com o modelo de quantidades (p. 49-50). Uso típico: simular impacto inflacionário setorial de tributos ou de preços administrados.

### 4.11 Miyazawa — multiplicadores inter-relacionais de renda

✅ Desagrega as famílias em $q$ grupos de renda (MILLER; BLAIR, 2009, §6.4, p. 271-276; releitura dirigida em 10 jun. 2026): $V=[v_{gj}]$ (renda paga ao grupo *g* por unidade de produção de *j*) e $C=[c_{ih}]$ (consumo do produto *i* por unidade de renda do grupo *h*). Com $B=(I-A)^{-1}$, o **multiplicador inter-relacional de renda** é
$$K = (I - VBC)^{-1}$$
e o sistema fechado decompõe-se em blocos (eqs. 6.41–6.43, p. ~273):
$$\begin{bmatrix}x\\ y\end{bmatrix} = \begin{bmatrix}B(I + CKVB) & BCK\\ KVB & K\end{bmatrix}\begin{bmatrix}f^*\\ 0\end{bmatrix} \qquad x = B(I + CKVB)\,f^* \qquad y = KVB\,f^*$$
$K_{gh}$ = efeito sobre a renda do grupo *g* de uma unidade adicional de renda do grupo *h*, captando a realimentação renda→consumo→renda entre grupos. ✅ Formulação em português (GUILHOTO, 2011, §9.3): $y^c = CQ$ (9.2), $Q = Vx$ (9.4), $x = (I - A - CV)^{-1}y^e$ (eq. 9.7; forma-produto $x = Z(I-CVZ)^{-1}y^e$, eq. 9.8). Uso: análise **distributiva** de choques (quem ganha a renda gerada).

### 4.12 Decomposição estrutural (SDA)

✅ Separa a variação da produção entre dois anos em **mudança tecnológica** ($\Delta L$) e **mudança de demanda final** ($\Delta f$) (MILLER; BLAIR, 2009, §13.1, p. 593-602 — equações conferidas diretamente no exemplar em 10 jun. 2026). De $\Delta x = x^1 - x^0 = L^1f^1 - L^0f^0$ (eq. 13.2), as duas formas polares exatas:
$$\Delta x = (\Delta L)f^0 + L^1(\Delta f) \quad (13.3) \qquad \Delta x = (\Delta L)f^1 + L^0(\Delta f) \quad (13.4)$$
há também as formas com **termo de interação** $(\Delta L)(\Delta f)$ somado ou subtraído (eqs. 13.5–13.6), e a média das polares (eq. 13.7):
$$\Delta x = \tfrac{1}{2}(\Delta L)(f^0+f^1) + \tfrac{1}{2}(L^0+L^1)(\Delta f)$$
✅ As alternativas são todas "matematicamente corretas" e dão contribuições diferentes; Dietzenbacher e Los (1998, apud MILLER; BLAIR, 2009, p. 595) concluem que **a média das polares é geralmente aceitável** — a escolha deve ser declarada. Generalização para produtos de $n$ termos: eqs. 13.8–13.12 (p. 598-599).

✅ **Decomposição da mudança de demanda final** (p. 599-601): com a matriz de demanda final por categorias $F^t$ $(n\times p)$, definem-se o **nível** $f^t = i'F^t i$, a **distribuição** entre categorias $d^t = (1/f^t)\,y^t$ (eq. 13.13) e a **matriz-ponte de composição** $B^t = F^t(\hat{y}^t)^{-1}$ (eq. 13.14), de modo que $f^t = f^t B^t d^t$ (eq. 13.15). A variação decompõe-se em (eq. 13.19):
$$\Delta f = \underbrace{\tfrac{1}{2}(\Delta f)(B^0d^0 + B^1d^1)}_{\text{efeito nível}} + \underbrace{\tfrac{1}{2}\big[f^0(\Delta B)d^1 + f^1(\Delta B)d^0\big]}_{\text{efeito mix (composição)}} + \underbrace{\tfrac{1}{2}(f^0B^0 + f^1B^1)(\Delta d)}_{\text{efeito distribuição}}$$
com a simplificação para uma única categoria ($p=1$): $\Delta f = \tfrac{1}{2}(\Delta f)(B^0+B^1) + \tfrac{1}{2}(f^0+f^1)(\Delta B)$ (eq. 13.20). A decomposição de $\Delta L$ em mudanças da matriz $A$ está em §13.1.4 (p. 602 e ss.). Requer matrizes comparáveis (mesma classificação e **preços constantes** — exigência declarada na p. 594).

> 📌 **Implementação e dados:** `mipcore.sda` implementa a eq. 13.7 com preços constantes por **pares anuais encadeados** — TRU corrente de *t−1* × TRU de *t* a preços de *t−1* (tabelas 68_tab3/tab4 do IBGE, disponíveis na pasta para 2011–2021; ver §1.4). Primeira aplicação: pasta `sda-brasil` (fora desta pasta de referência, conforme a convenção do projeto).

### 4.13 Modelos mistos — produção exógena (oferta fixa)

✅ Quando a produção de alguns setores é dada por fora do modelo (ex.: oferta agropecuária limitada por safra/área), particiona-se o sistema entre setores **endógenos** (demanda determina produção) e **exógenos** (produção fixada) (MILLER; BLAIR, 2009, §13.2, p. 621-632). Caso útil com demanda final constante: o transbordamento de uma variação exógena de produção é
$$\Delta x^{en} = L^{(k)}A_{12}\,\Delta x^{ex} \quad \text{(eq. 13.59)}$$
Aplicações citadas: cotas agrícolas, contribuição setorial com oferta fixa, fechamento parcial de mineração. → Relevante para choques de **oferta** em cadeias agro/bio, onde o modelo de demanda padrão não se aplica.

### 4.14 Insumo-produto dinâmico

✅ Incorpora o investimento via matriz de coeficientes de capital $B$ ($b_{ij}$ = estoque de capital do setor *i* por unidade de produção de *j*) (MILLER; BLAIR, 2009, §13.4, p. 639-654):
$$(I-A)x^t - B(x^{t+1}-x^t) = f^t \quad \text{(eqs. 13.75–13.78)}$$
⚠️ **Advertências fortes:** $B$ é tipicamente **singular** (setores que não fornecem bens de capital geram linhas nulas); o sistema é **extremamente sensível às condições iniciais** (pode gerar produções negativas); a mensuração de coeficientes de capital é mais precária que a dos técnicos (p. 640-649). Trajetória de crescimento equilibrado (*turnpike*): problema de autovalor $Qx=\lambda x$ com $Q$ função de $A$ e $B$ (eqs. 13.97–13.99). ✅ Formulação compacta em português: GUILHOTO (2011, §3.4, eqs. 3.10–3.13). Na pasta há ainda ten Raa (1986) sobre as dificuldades teóricas do modelo dinâmico (não detalhado aqui).

### 4.15 Matriz de Multiplicadores-Produto (MPM) e paisagem econômica

✅ Ferramenta de **análise estrutural** que organiza a inversa de Leontief em torno dos multiplicadores de linha e coluna, unificando R-H (§4.4), campo de influência (§4.8) e Miyazawa (§4.11) numa única estrutura (SONIS; HEWINGS, 1997, 1999, apud GUILHOTO; SONIS; HEWINGS, *Multiplier Product Matrix Analysis for Interregional Input-Output Systems* — ✅ lido diretamente em 16 jun. 2026, eqs. 1–31). Com $B=(I-A)^{-1}$, multiplicadores de coluna $B_{\bullet j}=\sum_i b_{ij}$ e de linha $B_{i\bullet}=\sum_j b_{ij}$, e intensidade global $V=\sum_i\sum_j b_{ij}$, a **MPM** é
$$M = \frac{1}{V}\,M_r(B)\,M_c(B), \qquad m_{ij}=\frac{1}{V}\,B_{i\bullet}\,B_{\bullet j} \quad \text{(eqs. 4–5)}$$
- **Conexão com R-H:** as hierarquias rank-size dos multiplicadores de coluna e linha da MPM **são exatamente** os índices de Rasmussen-Hirschman para trás e para frente: $BL_j=\frac{(1/n)B_{\bullet j}}{(1/n^2)V}$ e $FL_i=\frac{(1/n)B_{i\bullet}}{(1/n^2)V}$ (eqs. 6–7). Setor-chave: ambos $>1$.
- **Paisagem econômica:** reordenando linhas/colunas de $M$ de modo que os maiores "cruzamentos" (linha $i_0$ + coluna $j_0$ de maior multiplicador) desçam pela diagonal, obtém-se uma superfície que revela a hierarquia setorial e permite uma **taxonomia** comparativa entre economias (regiões diferentes ou a mesma região no tempo). Os elementos de $M$ são as **intensidades de primeira ordem do campo de influência** (§4.8).
- **Versão inter-regional** (região $r$ + resto $R$): pela decomposição de Schur-Banachiewicz/Miyazawa da inversa em blocos, $B_r=(I-A_{rr})^{-1}$ e $B_R=(I-A_{RR})^{-1}$ são os **multiplicadores internos de Miyazawa**, e a MPM decompõe-se em quatro blocos $M(B)_{rr}, M(B)_{rR}, M(B)_{Rr}, M(B)_{RR}$ (eqs. 22–31), separando a propagação intrarregional dos transbordamentos inter-regionais. → Aplicável diretamente às matrizes interestaduais prontas da §6.3.

📌 **Aplicações na pasta** (lidas em 16 jun. 2026): a versão nacional/setores-chave está em GUILHOTO; SONIS; HEWINGS; MARTINS, *Índices de Ligações e Setores Chave na Economia Brasileira: 1959-1980* (PT) e SONIS; GUILHOTO; HEWINGS; MARTINS, *Linkages, Key Sectors and Structural Change: Some New Perspectives* (EN) — este último é também a **fonte primária** das ligações puras GHS (§4.5) e do campo de influência (§4.8).

### 4.16 Comércio em valor adicionado e decomposição de exportações (cadeias globais de valor)

✅ Com a fragmentação internacional da produção, as **exportações brutas deixam de medir o valor adicionado** que um país gera ao exportar: elas embutem insumos importados e contam mais de uma vez o valor que cruza a fronteira várias vezes. A decomposição das exportações brutas em componentes de valor adicionado é hoje um ramo central da análise de insumo-produto, construído sobre uma **tabela inter-país (ICIO/MRIO)** com $G$ países e $N$ setores (§6.5 lista as bases). ⚠️ Esta ferramenta **não roda sobre a MIP nacional sozinha**: exige a base internacional.

✅ **Decomposição canônica** (KOOPMAN; WANG; WEI, 2014, eqs. 13–24, p. 11-16 — conferido por leitura direta em 17 jun. 2026): as exportações brutas de um país decompõem-se em quatro grandes blocos:
1. **Valor adicionado doméstico absorvido no exterior** (exportações em valor adicionado de Johnson-Noguera, 2012): o que o país produz e o exterior de fato consome;
2. **Valor adicionado doméstico que retorna** ao país de origem (via importações de bens finais ou intermediários): faz parte do PIB doméstico, mas não é "exportação de valor adicionado";
3. **Valor adicionado estrangeiro** embutido nas exportações (parte do PIB de outros países): o conteúdo importado;
4. **Dupla contagem pura**, que só existe quando há comércio de intermediários em mão dupla.

A partir desses blocos derivam-se, com precisão verificada nas eqs. 22–24: as **exportações em valor adicionado** (VAX de Johnson-Noguera, 2012) são os blocos 1+2 (valor criado em casa *e* absorvido fora); o **valor adicionado doméstico nas exportações** $DVA = v(I-a_{ii})^{-1}e$ são os blocos 1+2+3+4 (eq. 22, a parcela do PIB doméstico que é exportada, inclusive a que retorna ao país); o **conteúdo doméstico** é o $DVA$ mais a dupla contagem doméstica (bloco 5); e a **especialização vertical / conteúdo estrangeiro** $VS = (1 - v_i b_{ii})e$ são o bloco 3 mais a dupla contagem estrangeira (eqs. 23–24, generalizando Hummels-Ishii-Yi, 2001). O ponto-chave verificado no livro: os blocos 1 a 4 são parte do PIB do país de origem; o bloco 3 (valor estrangeiro) é parte do PIB de outros países; os termos de dupla contagem **não pertencem a nenhum PIB** (por isso "puros").

✅ **Padrão atual e refinamento** (BORIN; MANCINI, 2019, p. 2-5 — conferido por leitura direta): reúne a literatura (Hummels-Ishii-Yi; Johnson-Noguera; Koopman-Wang-Wei; Wang-Wei-Zhu; Los et al.) sob um arcabouço único para os níveis **agregado, bilateral e setorial**, e mostra que a **definição de "dupla contagem" depende da pergunta** — daí "perspectivas" alternativas (baseada na origem, *source*, e no destino, *sink*), cada uma adequada a um tipo de questão. Toda decomposição deve satisfazer **acurácia** (cada componente mede o que diz medir) e **consistência interna**. Em revisão crítica recente, a decomposição source-based de Borin e Mancini (2019; 2023), na perspectiva do país exportador, é tratada como o **padrão** para decompor o valor adicionado das exportações brutas, e é a usada pela OMC. → **Uso para a bioeconomia:** medir o conteúdo importado embutido nas exportações de soja, carne, celulose ou etanol, e a posição do agro/bio brasileiro nas cadeias (a montante como fornecedor de insumos, a jusante como comprador), com a base MRIO do §6.5. 📌 A derivação completa (multi-país, multissetor) e os códigos estão em Borin e Mancini; aqui registra-se o arcabouço, não a reimplementação.

---

## 5. Extensões para bioeconomia (conta-satélite)

✅ **Insumo-produto ambiental generalizado** (MILLER; BLAIR, 2009, cap. 10, §10.3, p. 447-451 — conferido por leitura direta): com coeficientes de impacto direto $D^p = [d^p_{kj}]$ (poluente *k* por R\$ de produção de *j* — notação do próprio livro),
$$x^{p*} = D^p x \quad (10.1) \qquad x^{p*} = \big[D^p L\big]\,f \quad (10.2)$$
sendo $[D^p L]$ a matriz de **coeficientes de impacto ambiental total** (pegada por R\$ de demanda final). Generalização (§10.3.2–10.3.3, p. 448-451): empilham-se $D^e, D^p, D^l, \dots$ numa matriz $D$ e define-se $D^* = DL$, com $\bar{x} = Hf$, $H = \begin{bmatrix}D^*\\ L\end{bmatrix}$ (forma de análise de impacto, p. 451). Empilhando $D^e, D^l, \dots$ obtêm-se pegadas de energia, terra, água, CO₂, emprego sobre a **mesma** inversa de Leontief.

✅ **Commodities ecológicas** (MILLER; BLAIR, 2009, cap. 10, §10.4.7, p. 473-475 — conferido por leitura direta): coeficientes de insumo ecológico $R = M\hat{x}^{-1}$ e de saída ecológica $Q = N'\hat{x}^{-1}$ — **com transposta**, explícita no livro ("$N'$ is the transpose of the matrix of ecological commodity output flows", p. 474): na Tabela 10.4 os fluxos de saída ecológica $N$ são registrados como (setor × tipo de saída), e o exemplo numérico usa $N'$ (tipo × setor). Requisitos totais: $R^* = R(I-A)^{-1}$, $Q^* = Q(I-A)^{-1}$ (p. 475). 📌 **Registro de correção dupla:** a fórmula original deste manual ($Q=N'\hat{x}^{-1}$) estava correta; uma "correção" de 10 jun. 2026 baseada em extração de agente removeu a transposta indevidamente; a leitura direta do exemplar restaurou a forma original. O §10.5 (p. 475) confirma ainda que o modelo aumentado de Leontief "was first proposed in Leontief (1970)".

✅ **Modelo ambiental original de Leontief** (LEONTIEF, 1970, p. 262-271 — p. 262-265 conferidas por leitura direta): a poluição entra como "commodity" adicional — linha de coeficientes de geração de poluente por unidade de produção, eqs. (5)/(5a), p. 264, formando uma matriz aumentada cuja inversa dá a poluição direta + indireta embutida em cada bem final (exemplo numérico nas p. 263-265). A coluna da atividade de **abatimento** (antipoluição) entra nas p. 266 em diante (não relidas diretamente; corroborada por MILLER; BLAIR, 2009, §10.5, p. 475). O mesmo arcabouço generaliza para trabalho, capital, água, terra. → É a origem histórica do arcabouço generalizado de Miller & Blair acima; cópia na pasta.

✅ **Emissões incorporadas no comércio (MRIO)** (ZHOU; KOJIMA, 2010, Parte I, §3, p. I-14 a I-19 — conferido por leitura direta): no sistema MRIO em blocos, $X = AX + F + E$ com $A^{rs} = X^{rs}/X^s$ (eq. I.1) e multiplicadores $B^{rs}$ da inversa de Leontief multirregional (eqs. I.2–I.3; no paper, $E$ denota exportações para o resto do mundo, **não** emissões). As emissões por princípio de responsabilidade: **produtor** (= territorial), $C^r_{prod} = c^r X^r + C^r_{hh}$ (eq. I.4), com $c^r$ = vetor-linha de intensidade de emissão por setor; **consumidor** (MRIO), $C^s_{con} = (\sum_r c^r B^{rs})F^{ss} + \sum_{n\neq s}[(\sum_r c^r B^{rn})F^{ns}] + C^s_{im} + C^s_{hh}$ (eq. I.5) — i.e., intensidades × inversa MRIO × demanda final, mais importações do resto do mundo e emissões diretas das famílias; e **compartilhada** produtor/consumidor pela razão de valor adicionado (eqs. I.14–I.16, base Lenzen et al.). A troca produtor→consumidor muda os inventários nacionais de −525 Mt-CO₂ (China) a +543 Mt-CO₂ (EUA) no caso de 10 economias em 2000 (Tabela I.4) — relevante para pegadas de exportações do agro/bio. 📌 A formulação compacta "$E=e(I-A_{MRIO})^{-1}Y$" da versão anterior deste manual era paráfrase correta em substância, mas com símbolos que não são os do paper; substituída pela notação original.

✅ **Unidades híbridas (energia/emissões)** (GUILHOTO, 2011, cap. 7, eqs. 7.14–7.20): fluxos de energia em unidades físicas combinados aos fluxos monetários; requisitos diretos e totais de energia e de CO₂ sobre a inversa híbrida $(I-A^*)^{-1}$.

✅ **Mensuração de agronegócio/cadeias bio-based via IP:** a metodologia de GUILHOTO; SESSO FILHO (2010) é a base do cálculo do **PIB do Agronegócio** do CEPEA-Esalq/USP, com a economia segmentada em insumos, produção primária (agropecuária), agroindústria e agrosserviços, deduzindo-se o consumo intermediário para evitar dupla contagem (CEPEA, *PIB do Agronegócio Brasileiro*; nota metodológica). → Caminho metodológico estabelecido para isolar e dimensionar cadeias da bioeconomia a partir da MIP nacional.

> ⚠️ **Lacuna para o projeto de bioeconomia:** a MIP do IBGE (nº 62) **não fornece** contas-satélite físicas ($D^p$ de terra, água, carbono, biodiversidade). Esses coeficientes precisam ser anexados a partir de fontes ambientais externas (ex.: SEEG, Censo Agropecuário, contas econômico-ambientais SEEA) e acoplados à $L$. Não há, nas fontes lidas, uma conta-satélite de bioeconomia pronta para o Brasil.

---

## 6. Extensões regionais e inter-regionais

### 6.1 Regionalização por método híbrido (não-survey)
✅ A *MIP-Nordeste* constrói um sistema **interestadual** (9 estados do NE + Resto do Brasil; 111 setores / 169 produtos; ano-base 2004 — Quadros 4 e 5 e p. 57; o §2.8.4, p. 58, registra que matrizes estaduais foram construídas para as 27 UFs) partindo das tabelas nacionais e regionalizando (GUILHOTO et al., 2010 — equações conferidas por leitura direta em 11 jun. 2026):
- **Quociente locacional** $LQ_i^R = \dfrac{X_i^R/X^R}{X_i^N/X^N}$; regra: se $LQ<1$, $a_{ij}^{RR}=a_{ij}^N\cdot LQ$; se $LQ\ge1$, mantém o nacional (eqs. 78–80). Variantes PLQ e CIQ (eqs. 81–82).
- **% de suprimento regional** $p_j^R=\dfrac{X_j^R-E_j^R}{X_j^R-E_j^R+M_j^R}$; $A^R=\hat{P}A$ (eqs. 50–52).
- **RAS** (ajuste biproporcional) para equilibrar margens (eqs. 74–77).
- **Sistema de Leontief inter-regional** em blocos $A=\begin{bmatrix}A^{LL}&A^{LM}\\A^{ML}&A^{MM}\end{bmatrix}$, $X=(I-A)^{-1}Y$ (eqs. 64–70), captando feedbacks inter-regionais.

### 6.2 Método IIOAS — sistema interestadual consistente com a matriz nacional
✅ O **IIOAS** (*Interregional Input-Output Adjustment System*, baseado em Haddad et al., 2016) estima o sistema inter-regional para as **27 UFs** sob informação limitada, com a vantagem central de **consistência com a matriz nacional**. Aplicável a qualquer país que (i) publique suas TRU e (ii) disponha de informação setorial regionalizada. **Verificado por leitura direta** (HADDAD; GONÇALVES JUNIOR; NASCIMENTO, 2017, eqs. 1–39, pp. 425-435; e HADDAD; ARAÚJO; ROCHA; VALE, 2025, mesma formulação, pp. 608-619 — ambos cotejados em 16 jun. 2026). O algoritmo:

1. **Dados de partida** (nacional): matriz de produção, usos a preços básicos, impostos indiretos (ICMS+IPI+OIIL) e importação, em 128 produtos × 68 setores, estimados por GUILHOTO; SESSO FILHO (2005; 2010). **Dados regionais**: VBP, exportações e VA por UF e setor; investimento, consumo das famílias e gastos do governo por UF (Contas Regionais, PIA, PPM, PAM, PAS, RAIS, Comex Stat).
2. **Hipótese central** (compartilhada com a *MIP-Nordeste*): demanda regional por produtos domésticos e importados segue o **padrão tecnológico nacional** (mesmo *mix* de insumos e preferências). Constroem-se coeficientes geradores de demanda $CCI^{DOM}_{ij}=Z^{DOM}_{ij}\hat{X}_j^{-1}$ (eq. 1) e regionalizam-se por VBP, INVT, CFT e GGT da UF (eqs. 3–7), obtendo $DEMDOM^R$; idem para importados (eqs. 8–14).
3. **Matrizes de comércio interestadual**: oferta doméstica $OFDOM^R = VBP^R - X^R$ (eq. 15); participações $SHIN$ com valor intrarregional inicial $\min(OFDOM/DEMDOM,1)\cdot F$ (eq. 16, fator de comerciabilidade $F$) e fluxos inter-regionais por um modelo gravitacional com **impedância** = tempo de viagem entre UFs (eq. 17, base Dixon e Rimmer, 2004); ajuste **RAS** para conciliar oferta (linhas) e demanda (colunas) em cada $TRADE^{sd}_i$ (eq. 18).
4. **Regionalização** sob a hipótese de Chenery-Moses (mesma participação regional para todos os usuários de uma região): coeficientes regionais de consumo intermediário (eq. 23), demanda final (eqs. 24–26) e impostos (eqs. 27–39), convertidos a fluxos monetários pelos totais regionais.

📌 **Validação externa** (versão 2019): os fluxos bilaterais estimados são comparados aos **fluxos de ICMS do CONFAZ**, com alta correlação (HADDAD et al., 2025, Figura 3). → Aprimoramento direto sobre a regionalização por LQ/RAS da *MIP-Nordeste* (§6.1), com a mesma família de hipóteses, porém ancorado em mais fontes regionais e validado contra dados fiscais observados.

### 6.3 Matrizes interestaduais prontas para uso (dados na pasta)

✅ **Há duas matrizes interestaduais completas na pasta** (adicionadas em 16 jun. 2026), que dispensam estimar o sistema do zero:

| Recurso | Ano-base | Conteúdo | Estado verificado |
|---|---|---|---|
| `administrador,+IIOAS_Brasil_RBERU_2017.xlsx` (130 MB) | **2011** | 27 UFs × 68 setores; abas `A`, `I-A` e `B=(I-A)⁻¹` **prontas** (núcleo 1836×1836), além de `IIOS` (fluxos), `Sectors`, `Regions` | ✅ **Carregada e validada** em 16 jun. 2026: $A\in[0,\,0{,}405]$, todas as somas de coluna $\le 0{,}846$, sem negativos; $\max\lvert(I-A)B-I\rvert = 7\times10^{-15}$ (B é a inversa de Leontief exata). Sistema de Leontief válido |
| `IIOAS_BRUF_2019.xlsx` (no `.rar`, ~115 MB) | **2019** | 27 UFs × 68 setores × 128 produtos; abas `MIIP SS` (setor×setor, 1863×1977), `MIIP PS` (produto×setor), `Produção` | ✅ Estrutura inspecionada em 16 jun. 2026: traz os **fluxos** inter-regionais (não A/L prontas); $A$ e $L$ são deriváveis. As contas socioambientais citadas no resumo (CO₂, energia, água, emprego) **não** estão neste arquivo |

Fontes: HADDAD; GONÇALVES JUNIOR; NASCIMENTO (2017) para a de 2011; HADDAD; ARAÚJO; ROCHA; VALE (2025) para a de 2019. **Implicação operacional:** a "abertura por estado" antes adiada deixou de exigir estimação própria por LQ ou IIOAS. Com a matriz pronta, análises por UF (multiplicadores estaduais, transbordamentos inter-regionais, setores-chave por estado, autossuficiência) tornam-se diretas. ✅ **Implementado em `mipcore.regional`** (17 jun. 2026), para **2011 e 2019**: carrega o sistema (controles a ~1e-14) e expõe multiplicadores de produção, R-H, autossuficiência por UF, **demanda final regional**, extração hipotética de região, MPM e agregação a 27×27, com índices por bloco $(27\times68)$. A demanda final (`demanda_final`) é validada por $L\cdot f = VBP$: para 2019, lida das colunas 1841–1976 da MIIP SS (5 categorias — investimento, famílias, governo, ISFLSF, exportações — mais discrepância; WMAPE 0%); para 2011, obtida por $f=(I-A)\,VBP$ com o VBP da aba IIOS (linha 1917). A extração hipotética usa essa demanda final **real** por padrão (antes era um choque unitário), o que muda o impacto de extrair SP de ~14–16% para **~21–23% da produção nacional**. Para 2011 lê A pronta; para **2019 deriva $A = Z\,\text{diag}(1/VBP)$** da aba "MIIP SS" (Z = bloco intermediário, linhas 7–1842 × colunas 5–1840; VBP = "Valor da produção", linha 1856), com a identidade contábil Z + importação + impostos + VAB = VBP conferida a **0%** (146 colunas com VBP=0, setores sem produção em certas UFs, ficam com coeficientes nulos). Validação externa: o ranking de autossuficiência reproduz o padrão do artigo nos dois anos (SP no topo; AP/TO/RR/RO no fundo; RJ cai de 4º em 2011 para 9º em 2019, mudança estrutural real) — coberto por testes em `MIP/tests/`. Receita em [`COOKBOOK.md`](COOKBOOK.md), §7. ⚠️ Por diretriz do projeto, as **contas socioambientais** presentes no arquivo de 2019 (CO₂, água, energia, linhas 1861–1863) **não** são carregadas: conta-satélite fica fora desta pasta.

### 6.4 Aplicação — calibração de EGC espacial
✅ Uma base inter-regional de IP serve de núcleo para modelos de **Equilíbrio Geral Computável espacial**. O modelo de referência é o **B-MARIA** (*Brazilian Multisectoral and Regional/Interregional Analysis*), desenvolvido por Haddad (1999): reconhece as 27 regiões brasileiras, identifica 56 setores produzindo 110 *commodities*, com fluxos inter-regionais de bens, custos de transporte por par origem-destino e fatores primários regionais (HADDAD; PORSSE; PEREDA, 2013, p. 23 — ✅ verificado por leitura direta em 16 jun. 2026; calibrado para 2005-2007, software GEMPACK). Exemplo de aplicação: integração de um modelo físico (função-lucro agronômica) ao EGC para medir o impacto sistêmico das anomalias climáticas de 2005, que reduziram o PIB nacional em 0,163% e o emprego em 0,403%, com cada R\$ 1,00 de perda agrícola direta gerando R\$ 3,25 de perda na economia (efeito das ligações intersetoriais e inter-regionais). Outra aplicação da mesma família: enchentes de São Paulo, acoplando dados GIS à estrutura de IP metropolitana (HADDAD; TEIXEIRA, 2015; cópia local é o *working paper* ERSA 2013).

### 6.5 Bases inter-país (ICIO/MRIO) oficiais para comércio em valor adicionado

✅ A decomposição de exportações (§4.16) e a análise de comércio em valor adicionado exigem uma **tabela inter-país (ICIO/MRIO)**, que combina as IO nacionais com estatísticas de comércio para rastrear fluxos entre países e setores. O manual antes citava apenas a AIO-2000 (ZHOU; KOJIMA, 2010), de 2000. As bases vigentes, **todas com o Brasil incluído**, são:

| Base | Responsável | Cobertura | Verificação |
|---|---|---|---|
| **FIGARO** | Eurostat + JRC (Comissão Europeia) | Edição **2024**, série 2010–2022, 64 setores × 64 produtos; 27 UE + 18 parceiros (inclui Brasil) + resto do mundo; traz também emprego e variáveis ambientais | ✅ verificado em fonte oficial (jun. 2026) |
| **OECD ICIO / TiVA** | OCDE (e OCDE-OMC para os indicadores TiVA) | Edição **2023**; base dos indicadores Trade in Value Added | ✅ verificado em fonte oficial (jun. 2026) |
| **EXIOBASE** | consórcio europeu | MRIO ambientalmente estendido (energia, emissões, água, terra); extensão FIGARO-E3 (2025) integra isso ao FIGARO | [Provável] — citar versão vigente da fonte |
| **EORA** | Univ. de Sydney (Lenzen et al., 2013) | MRIO global com ampla cobertura de países, inclusive em desenvolvimento | [Provável] — citar versão vigente |
| **GTAP** | Purdue (Global Trade Analysis Project) | Base global que sustenta modelos EGC; versão MRIO | [Provável] — citar versão vigente |
| **ADB MRIO** | Banco Asiático de Desenvolvimento | Foco Ásia-Pacífico, com parceiros | [Provável] — citar versão vigente |

⚠️ **Sinceridade sobre o que verifiquei:** as edições de FIGARO (2024) e OECD ICIO (2023) e a inclusão do Brasil foram confirmadas em fonte oficial nesta sessão (jun. 2026); EXIOBASE, EORA, GTAP e ADB MRIO estão nomeadas a partir de BORIN; MANCINI (2019) e de conhecimento geral, **sem conferência da versão vigente** — antes de usar, checar a edição atual na fonte. 📌 Por que importa para este projeto: com qualquer uma dessas bases, as exportações do agro/bio brasileiro entram na decomposição do §4.16 sem que seja preciso construir a MRIO.

---

## 7. Confiabilidade, agregação e desagregação setorial

> Ferramentas de **robustez** — quanto confiar nos multiplicadores — e de **redimensionamento setorial** — como agregar ou abrir setores sem distorcer a estrutura. Diretamente úteis quando se quer destacar cadeias específicas (ex.: bio-based) de uma TRU agregada.

### 7.1 Incerteza paramétrica e coeficientes críticos

✅ O efeito de erros $\Delta A$ nos coeficientes propaga-se para a inversa com cota superior proporcional ao **número de condição** $M$ de $(I-A)$ (BULLARD; SEBALD, 1977, eq. 3, p. 77 — conferido por leitura direta). ⚠️ Os próprios autores admitem que a cota é **"muito frouxa" na prática** (p. 77) — serve para ordenar sensibilidades, não para intervalos realistas (para estes, ver §7.2). O método ranqueia os coeficientes por sensibilidade do resultado, identificando o **subconjunto pequeno de coeficientes "críticos"** que precisa de dados precisos — os demais podem permanecer históricos (aplicado a modelos de energia, p. 78-80). Uso: priorizar onde gastar esforço de coleta/atualização.

### 7.2 Sensibilidade por Monte Carlo

✅ Perturbam-se os coeficientes com distribuições de erro atribuídas a cada célula e recomputa-se $(I-A)^{-1}$ — **1.000 inversões** no experimento com a matriz dos EUA (BULLARD; SEBALD, 1988, p. 708-711 — conferido por leitura direta): **mais de 90% dos elementos da inversa** têm média populacional a menos de **2%** da média amostral (95% de confiança), e a produção bruta total e o vetor de intensidade de energia ficam dentro de **1%**; o valor **97,5%** refere-se à cota superior de confiança sobre os **desvios-padrão** (≤ 1,16× o desvio amostral), não aos elementos da inversa. Os erros tendem a **se cancelar** na inversão (com pequeno viés médio de superestimação), e a agregação — base 360→90 setores, testada também em 90→30 e 101 — não altera materialmente a distribuição da incerteza. Uso: reportar intervalos de confiança de multiplicadores em vez de números pontuais. 📌 Registro: versão anterior deste manual dizia "97,5% dos elementos a ~2% do publicado", conflando os dois resultados; corrigido por releitura direta em 11 jun. 2026.

### 7.3 Agregação sem distorção

✅ **Dupla inversão de Leontief** (LEONTIEF, 1967 — conferido por leitura direta): para comparar matrizes com classificações incompatíveis, em vez de agregar (o que distorce a estrutura), particiona-se a economia e deriva-se a matriz reduzida exata do grupo de interesse, $A_{11}^* = I - B_{11}^{-1}$ (com $B=(I-A)^{-1}$) — eq. (7), p. 414 —, absorvendo no resíduo os fluxos do resto da economia; a forma particionada equivalente $A_{11}^* = A_{11} + A_{12}(I-A_{22})^{-1}A_{21}$ é a eq. (11), p. 415. A diferença entre $A_{11}^*$ e a matriz agregada convencional mede o **erro de agregação**.

✅ **Viés de agregação de primeira ordem** (GUILHOTO, 2011, §4.4, eqs. 4.37 e 4.41, apud Morimoto): $F=(A^*S-SA)\,y$ — minimizado quando os setores agregados têm estruturas de insumos semelhantes. Critério prático para desenhar a agregação.

### 7.4 Desagregação com informação parcial

✅ Wolsky (1984, p. 283-285 e Apêndice A — conferido por leitura direta) resolve o problema inverso: **abrir um setor em dois** dispondo da matriz agregada e de informação parcial sobre o novo detalhamento. Os pesos de produção $w_1, w_2$ (razões dos produtos brutos, $w_2 = 1-w_1$) podem ser inferidos "de demonstrações financeiras de firmas ou de estatísticas publicadas por associações setoriais" (p. 285). A matriz desagregada aumentada $\mathbb{A}$ é exata e explícita (eqs. 5–8); sua inversa $\mathbb{L}^{-1}$ é recuperada a baixo custo a partir de $l^{-1}$ da matriz agregada (eqs. 9–12), sem reinverter o sistema inteiro; a **matriz distintiva** $\Delta \equiv A - \mathbb{A} = L - \mathbb{L}$ (eq. 13) é parametrizada pelos desvios das estruturas de compra ($\delta_i, \delta_n$) e venda ($\sigma_j, \sigma_n$) e pelo termo cruzado $\xi$ (eqs. 14–16); quando esses desvios são desconhecidos, o Apêndice A dá **cotas** em função apenas de $w_1, w_2$ e dos coeficientes agregados. → **Caminho metodológico direto para destacar setores bioeconômicos** (ex.: separar "bioenergia" dentro de um setor agregado da TRU) com dados parciais de associações setoriais ou pesquisas específicas.

---

## 8. Refinamentos e lacunas

| Tema | Situação nos materiais de base | Refinamento / fonte verificada |
|---|---|---|
| Distribuição de margens/impostos | Estimada por $\alpha_{ij}$; viés na margem de comércio (GUILHOTO; SESSO FILHO, 2005) | ✅ Tabelas 7–10 oficiais do IBGE dão o destino observado das margens (IBGE, 2018) |
| Coeficientes negativos de importados | — | ✅ Ajuste CIF/FOB desde a MIP 2010 elimina importações negativas (IBGE, 2018) |
| Simetrização SUT→A | Delegada a Miller & Blair pelos papers | ✅ Modelo oficial explícito: tecnologia do setor simples, eqs. (3)–(12) (IBGE, 2018) |
| Base de dados industrial | Censos (até 1990) | ✅ PIA-Empresa desde 2000/2005 (IBGE, 2018) |
| Regionalização | LQ + RAS + gravitacional (GUILHOTO et al., 2010) | ✅ IIOAS, consistente com a matriz nacional e validado contra ICMS/CONFAZ (HADDAD et al., 2017; 2025); **matrizes 2011 e 2019 prontas na pasta** (§6.3) |
| Ferramental analítico ampliado | R-H, GHS, multiplicadores | ✅ Documentado nas §§4.6–4.16 a partir de MILLER; BLAIR (2009), GUILHOTO (2011) e SONIS; GUILHOTO; HEWINGS: Tipo II formal, Ghosh, campo de influência, extração hipotética, preços, Miyazawa, SDA, mistos, dinâmico, MPM |
| Robustez e redimensionamento setorial | — | ✅ §7: incerteza paramétrica, Monte Carlo, agregação e desagregação (BULLARD; SEBALD, 1977; 1988; LEONTIEF, 1967; WOLSKY, 1984) |
| **Comércio em valor adicionado / cadeias globais (GVC)** | ⚠️ Ausente nas versões anteriores | ✅ Adicionado em §4.16: decomposição de exportações brutas (KOOPMAN; WANG; WEI, 2014; BORIN; MANCINI, 2019, padrão da OMC) — requer base ICIO/MRIO |
| **Bases MRIO internacionais (dados)** | Só AIO-2000 (ZHOU; KOJIMA, 2010) | ✅ Quadro de fontes vigentes em §6.5: FIGARO, OECD ICIO, EXIOBASE, EORA, GTAP (todas incluem o Brasil) |
| **Transição SCN referência 2010 → 2021** | Manual ancorado na referência 2010 | ⚠️ Série 2021 a partir de 2026, com nova MIP e SNA 2025 (IBGE, Nota Técnica 01/2024); detalhes de classificação ainda não públicos (§1, advertência de vigência) |
| Setor informal / produção familiar | ⚠️ Ausente na metodologia Guilhoto–Sesso (2005/2010) | ⚠️ Não localizado tratamento nas fontes lidas |
| Conta-satélite de bioeconomia | ⚠️ Ausente na MIP do IBGE | ⚠️ Requer acoplar coeficientes ambientais externos à $L$ (sem fonte pronta para o Brasil nas fontes lidas) |

---

## 9. Guia de decisão: qual método para qual análise

| Pergunta de análise | Insumo necessário | Ferramenta | Fonte |
|---|---|---|---|
| Quanto a produção total muda se a demanda final muda? | $A$, $Y$ | $\Delta X=(I-A)^{-1}\Delta Y$ | IBGE (2018); GUILHOTO et al. (2010) |
| Quais setores mais irradiam crescimento? | $L$ | R-H ($U_j$, $U_i$); GHS ($PBL/PFL$) | GUILHOTO; SESSO FILHO (2005) |
| Impacto sobre emprego/renda/impostos? | $L$, coeficientes setoriais | Geradores/multiplicadores Tipo I e II | GUILHOTO et al. (2010) |
| Análise tecnológica (produto×produto) vs. intersetorial (atividade×atividade)? | $Bn$, $D$ | $(I-Bn\,D)^{-1}$ vs. $(I-D\,Bn)^{-1}$ | IBGE (2018) |
| Matriz de ano sem dados definitivos? | TRU preliminar + totais de margens/impostos | Algoritmo $\alpha_{ij}$ | GUILHOTO; SESSO FILHO (2005) |
| Atualizar matriz antiga com totais novos? | $A(0)$, $x(1)$, $u(1)$, $v(1)$ | RAS; com células negativas, GRAS | MILLER; BLAIR (2009, §7.4); LENZEN; WOOD; GALLEGO (2007) |
| MIP de ano sem TRU 68 (2022+)? | $Z$, $g$ do último ano com TRU 68 + TRU nível 12 do alvo | GRAS com margens do nível 12 (`mipcore.gras.estimar`) — §2.5; incerteza ~3% nos multiplicadores | LENZEN; WOOD; GALLEGO (2007); validação própria (§2.5) |
| Efeitos induzidos pelo consumo (Tipo II)? | $\bar{A}$ (famílias endógenas) | $\bar{L}=(I-\bar{A})^{-1}$; razão II/I constante | MILLER; BLAIR (2009, §6.2) |
| Quem fica com a renda gerada (distribuição)? | $V$, $C$ por grupo de renda | Miyazawa $K=(I-VBC)^{-1}$ | MILLER; BLAIR (2009, §6.4); GUILHOTO (2011, §9.3) |
| Repasse de custos / inflação setorial? | $A$, $\Delta\tilde{v}$ | Modelo de preços $\Delta p=(I-A')^{-1}\Delta\tilde{v}$ | MILLER; BLAIR (2009, §2.6) |
| Quanto a economia perde sem o setor *j*? | $A$, $B$ (alocação), $f$ | Extração hipotética ($B_j$, $F_j$, $T_j$) | MILLER; BLAIR (2009, §12.2.6) |
| Quais elos estruturais são críticos? | $A$, $L$ | Campo de influência ($S_{ij}$) | GUILHOTO (2011, §6.4) |
| Crescimento entre dois anos: tecnologia ou demanda? | $L^0,L^1,f^0,f^1$ comparáveis | SDA (média das formas polares) | MILLER; BLAIR (2009, §13.1) |
| Choque de OFERTA (safra, quebra, cota)? | $A$ particionada | Modelos mistos ($\Delta x^{en}=L^{(k)}A_{12}\Delta x^{ex}$) | MILLER; BLAIR (2009, §13.2) |
| Investimento/capacidade ao longo do tempo? | $A$ + matriz de capital $B$ | IO dinâmico (com cautela: $B$ singular) | MILLER; BLAIR (2009, §13.4) |
| Quanto confiar nos multiplicadores? | distribuições de erro de $A$ | Monte Carlo; coeficientes críticos | BULLARD; SEBALD (1988; 1977) |
| Destacar/abrir um setor (ex.: bio) na TRU? | matriz agregada + dados parciais | Desagregação de Wolsky; dupla inversão | WOLSKY (1984); LEONTIEF (1967) |
| Pegada ambiental / bioeconomia? | $L$ + coeficientes $D^p$ externos | $x^{p*}=[D^p L]\,f$; MRIO p/ comércio | MILLER; BLAIR (2009); LEONTIEF (1970); ZHOU; KOJIMA (2010) |
| Recortes regionais / transbordamentos entre estados? | matriz interestadual pronta (2011/2019, §6.3) ou TRU + dados regionais | IRIO sobre a MIIP pronta; ou estimar por LQ/RAS, IIOAS | HADDAD et al. (2017; 2025); GUILHOTO et al. (2010) |
| Multiplicadores / setores-chave por UF? | MIIP interestadual pronta (§6.3) | $L=(I-A)^{-1}$ em blocos $(27\times68)$; R-H e extração regionais | HADDAD et al. (2017; 2025) |
| Choques espaciais / simulação de política? | base IP inter-regional | EGC espacial (modelo B-MARIA) | HADDAD; PORSSE; PEREDA (2013); HADDAD; TEIXEIRA (2015) |

---

## Referências

BORIN, A.; MANCINI, M. **Measuring what matters in global value chains and value-added trade**. Washington: World Bank, 2019. (Policy Research Working Paper, n. 8804). Disponível em: https://documents1.worldbank.org/curated/en/639481554384583291/pdf/Measuring-What-Matters-in-Global-Value-Chains-and-Value-Added-Trade.pdf. Acesso em: 17 jun. 2026. [Cópia local: `Borin-Mancini-2019-Measuring-GVC-WB8804.pdf`] (✅ lido diretamente em 17 jun. 2026, §§1-2, p. 2-5; arcabouço unificado, perspectivas source/sink). Versão estendida: BORIN; MANCINI (2023).

BULLARD, C. W.; SEBALD, A. V. Effects of parametric uncertainty and technological change on input-output models. **The Review of Economics and Statistics**, v. 59, n. 1, p. 75-81, 1977.

BULLARD, C. W.; SEBALD, A. V. Monte Carlo sensitivity analysis of input-output models. **The Review of Economics and Statistics**, v. 70, n. 4, p. 708-712, 1988.

CENTRO DE ESTUDOS AVANÇADOS EM ECONOMIA APLICADA (CEPEA). **PIB do agronegócio brasileiro: comentários metodológicos**. Piracicaba: CEPEA-Esalq/USP, [s. d.]. Disponível em: https://www.cepea.org.br/upload/kceditor/files/Cepea_NotaMetodologica_Nova.pdf. Acesso em: 2 jun. 2026.

GUILHOTO, J. J. M. **Análise de insumo-produto: teoria e fundamentos**. Munique: University Library of Munich, 2011. (MPRA Paper, n. 32566). Disponível em: https://mpra.ub.uni-muenchen.de/32566/. Acesso em: 10 jun. 2026. [Cópia local: `Guilhoto-2011-Analise-Insumo-Produto-MPRA32566.pdf`. A cópia SSRN redundante `ssrn-1900073.pdf` foi removida em 16 jun. 2026]

GUILHOTO, J. J. M. **Leontief e insumo-produto: antecedentes, princípios e evolução**. Munique: University Library of Munich, 2011. (revisão histórica da teoria de IO). [Cópia local: `ssrn-2414028.pdf`. A cópia idêntica `ssrn-2417390.pdf` foi removida em 16 jun. 2026]

GUILHOTO, J. J. M.; CAMARGO, F. S.; IMORI, D.; INOMATA, S. **National input-output table of Brazil**. (história e características das tabelas de IO do Brasil, referência 2005; integração à tabela internacional BRICS). [Cópia local: `ssrn-2408067.pdf`]

GUILHOTO, J. J. M.; SONIS, M.; HEWINGS, G. J. D. **Multiplier product matrix analysis for interregional input-output systems: an application to the Brazilian economy**. Urbana: REAL/University of Illinois. (MPM inter-regional; aplicação a 2 regiões do Brasil, 1992). [Cópia local: `ssrn-2417397.pdf`] (✅ lido diretamente em 16 jun. 2026, eqs. 1–31)

GUILHOTO, J. J. M.; SONIS, M.; HEWINGS, G. J. D.; MARTINS, E. B. **Índices de ligações e setores chave na economia brasileira: 1959-1980**. (versão em português de SONIS et al.). [Cópia local: `ssrn-2420472.pdf`]

GUILHOTO, J. J. M.; SESSO FILHO, U. A. Estimação da matriz insumo-produto a partir de dados preliminares das contas nacionais. **Economia Aplicada**, São Paulo, v. 9, n. 2, p. 277-299, abr./jun. 2005.

GUILHOTO, J. J. M.; SESSO FILHO, U. A. Estimação da matriz insumo-produto utilizando dados preliminares das contas nacionais: aplicação e análise de indicadores econômicos para o Brasil em 2005. **Economia & Tecnologia**, Curitiba, ano 6, v. 23, p. 53-62, out./dez. 2010.

GUILHOTO, J. J. M.; AZZONI, C. R.; ICHIHARA, S. M.; KADOTA, D. K.; HADDAD, E. A. **Matriz de insumo-produto do Nordeste e estados: metodologia e resultados**. Fortaleza: Banco do Nordeste do Brasil, 2010.

HADDAD, E. A.; GONÇALVES JUNIOR, C. A.; NASCIMENTO, T. O. Matriz interestadual de insumo-produto para o Brasil: uma aplicação do método IIOAS. **Revista Brasileira de Estudos Regionais e Urbanos (RBERU)**, v. 11, n. 4, p. 424-446, 2017. [Cópias locais: `document.pdf` (artigo RBERU) e `Haddad-2017-IIOAS-TD-Nereus-02-2017.pdf` (TD NEREUS); dados em `administrador,+IIOAS_Brasil_RBERU_2017.xlsx` (matriz 2011)]

HADDAD, E. A.; ARAÚJO, I. F.; ROCHA, A.; VALE, V. A. Matriz interestadual de insumo-produto para o Brasil, 2019. **Revista Brasileira de Estudos Regionais e Urbanos (RBERU)**, v. 19, n. 4, p. 607-638, 2025. DOI: 10.54766/rberu.v19i4.1225. [Cópia local: `7_1225ed.pdf`; dados em `IIOAS_BRUF_2019.xlsx`]

HADDAD, E. A.; PORSSE, A. A.; PEREDA, P. C. Regional economic impacts of climate anomalies in Brazil. **Revista Brasileira de Estudos Regionais e Urbanos (RBERU)**, v. 7, n. 2, p. 19-33, 2013. [Cópia local: `administrador,+02+Haddad+et+al._v7_n2_pp19-33_2013.pdf`]

HADDAD, E. A. **Regional inequality and structural changes: lessons from the Brazilian experience**. Aldershot: Ashgate, 1999. (modelo B-MARIA; citado por HADDAD; PORSSE; PEREDA, 2013).

DIXON, P. B.; RIMMER, M. T. Disaggregation of results from a detailed general equilibrium model. **(apud HADDAD; GONÇALVES JUNIOR; NASCIMENTO, 2017; HADDAD et al., 2025)**, 2004. (base das eqs. 16–17 do IIOAS; não lida diretamente).

HADDAD, E. A.; TEIXEIRA, E. Economic impacts of natural disasters in megacities: the case of floods in São Paulo, Brazil. **Habitat International**, v. 45, p. 106-113, 2015. [Cópia local: `ERSA2013_paper_00409.pdf`, versão *working paper*]

EUROSTAT; JOINT RESEARCH CENTRE (Comissão Europeia). **FIGARO: EU inter-country supply, use and input-output tables** (edição 2024, série 2010–2022). Disponível em: https://ec.europa.eu/eurostat/web/esa-supply-use-input-tables/database-figaro. Acesso em: 17 jun. 2026.

HUMMELS, D.; ISHII, J.; YI, K.-M. The nature and growth of vertical specialization in world trade. **Journal of International Economics**, v. 54, n. 1, p. 75-96, 2001. (citado via KOOPMAN; WANG; WEI, 2014; BORIN; MANCINI, 2019 — não lido diretamente).

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Matriz de insumo-produto: Brasil: 2015**. Rio de Janeiro: IBGE, 2018. 60 p. (Contas Nacionais, n. 62). ISBN 978-85-240-4465-6. Disponível em: https://biblioteca.ibge.gov.br/visualizacao/livros/liv101604.pdf. Acesso em: 10 jun. 2026. [Cópia local: `IBGE-2018-MIP-Brasil-2015-liv101604.pdf`]

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Sistema de Contas Nacionais — Nota Técnica 01/2024: implantação da série do SCN, ano base 2021**. Rio de Janeiro: IBGE, 29 abr. 2024. Disponível em: https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv102085.pdf. Acesso em: 17 jun. 2026. (✅ lida diretamente em 17 jun. 2026)

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Implantação da Série do SCN — referência 2021: nota metodológica nº 1**. Rio de Janeiro: IBGE, 2025. Disponível em: https://biblioteca.ibge.gov.br/visualizacao/livros/liv102216.pdf. Acesso em: 17 jun. 2026.

JOHNSON, R. C.; NOGUERA, G. Accounting for intermediates: production sharing and trade in value added. **Journal of International Economics**, v. 86, n. 2, p. 224-236, 2012. (exportações em valor adicionado; citado via KOOPMAN; WANG; WEI, 2014; BORIN; MANCINI, 2019 — não lido diretamente).

KOOPMAN, R.; WANG, Z.; WEI, S.-J. Tracing value-added and double counting in gross exports. **American Economic Review**, v. 104, n. 2, p. 459-494, 2014. (versão NBER Working Paper, n. 18579, 2012). Disponível em: https://www.nber.org/system/files/working_papers/w18579/w18579.pdf. Acesso em: 17 jun. 2026. [Cópia local: `Koopman-Wang-Wei-2014-Tracing-ValueAdded-NBER18579.pdf`] (✅ lido diretamente em 17 jun. 2026, eqs. 13–24, p. 11-16)

LEONTIEF, W. An alternative to aggregation in input-output analysis and national accounts. **The Review of Economics and Statistics**, v. 49, n. 3, p. 412-419, 1967.

LEONTIEF, W. Environmental repercussions and the economic structure: an input-output approach. **The Review of Economics and Statistics**, v. 52, n. 3, p. 262-271, 1970.

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Sistema de contas nacionais: Brasil**: ano de referência 2010. 3. ed. Rio de Janeiro: IBGE, 2016. (Série Relatórios Metodológicos, v. 24). Disponível em: https://biblioteca.ibge.gov.br/visualizacao/livros/liv98142.pdf. Acesso em: 10 jun. 2026. [Cópia local: `IBGE-2016-SCN-Ref2010-3ed-RelatoriosMetodologicos-v24.pdf` — capa conferida; conteúdo ainda não cotejado com afirmações do manual]

MILLER, R. E.; BLAIR, P. D. **Input-output analysis: foundations and extensions**. 2. ed. Cambridge: Cambridge University Press, 2009.

ORGANISATION FOR ECONOMIC CO-OPERATION AND DEVELOPMENT (OECD). **OECD Inter-Country Input-Output (ICIO) database** (edição 2023). Paris: OECD. Disponível em: https://www.oecd.org/sti/ind/inter-country-input-output-tables.htm. Acesso em: 17 jun. 2026. (base dos indicadores OECD-WTO TiVA).

ORGANIZAÇÃO DAS NAÇÕES UNIDAS (ONU) et al. **System of National Accounts 2025**. Nova York: United Nations, 2025. Endossado pela Comissão de Estatística da ONU em mar. 2025. Disponível em: https://unstats.un.org/unsd/nationalaccount/SNAUpdate/2025/. Acesso em: 17 jun. 2026. (não lido diretamente; citado pela adoção declarada pelo IBGE na série referência 2021).

SONIS, M.; GUILHOTO, J. J. M.; HEWINGS, G. J. D.; MARTINS, E. B. **Linkages, key sectors and structural change: some new perspectives**. Urbana: REAL/University of Illinois. (ligações puras GHS, campo de influência e MPM; aplicação ao Brasil). [Cópia local: `ssrn-2420129.pdf`] (✅ lido diretamente em 16 jun. 2026: ligações R-H eqs. 1–2; Cella/Clements eqs. 3–14; ligações puras eqs. 15–32; campo de influência eq. 33). Fonte primária das §§4.5 e 4.8.

JUNIUS, T.; OOSTERHAVEN, J. The solution of updating or regionalizing a matrix with both positive and negative entries. **Economic Systems Research**, v. 15, n. 1, p. 87-96, 2003. *(Cópia não obtida — citado por intermédio de Lenzen, Wood e Gallego, 2007.)*

LENZEN, M.; WOOD, R.; GALLEGO, B. Some comments on the GRAS method. **Economic Systems Research**, v. 19, n. 4, p. 461-465, 2007. *(Cópia na pasta, baixada em 11 jun. 2026.)*

WOLSKY, A. M. Disaggregating input-output models. **The Review of Economics and Statistics**, v. 66, n. 2, p. 283-291, 1984.

ZHOU, X.; KOJIMA, S. **Carbon emissions embodied in international trade: an assessment from the Asian perspective**. Hayama: Institute for Global Environmental Strategies (IGES), 2010.

> **Nota sobre uma referência.** A cópia local de Miller e Blair está rotulada "2012", mas a página de copyright do exemplar confirma **2009** (2ª edição, Cambridge University Press; o arquivo é reimpressão). ✅ Verificado no exemplar local em 10 jun. 2026 — citar como 2009, conforme a referência acima.

---

## Nota de honestidade sobre lacunas (o que NÃO foi inventado)

**Lacunas abertas** (não localizadas em fonte verificável; sinalizadas no texto, não preenchidas por inferência):
1. Os números de tabela **SIDRA** individuais das TRU/MIP (§1.3).
2. O nível de divulgação **20×20** — não mencionado no texto da publicação IBGE nº 62 verificada (§1.3).
3. Tratamento de **setor informal / produção familiar** (§8).
4. Conta-satélite de **bioeconomia** pronta para o Brasil (§5, §8) — por diretriz do projeto (jun. 2026), o desenvolvimento de conta-satélite fica **fora deste manual**; a §5 permanece apenas como referência teórica de acoplamento.
5. Numeração das equações **(11) e (12)** do IBGE — a cópia digital local (17 p.) termina na eq. (10); fórmulas confirmadas pela derivação, números não (§3).
6. **IBGE (2016, Relatórios Metodológicos v. 24)**: cópia local baixada em 10 jun. 2026 e capa conferida (3ª ed., referência 2010), mas o **conteúdo ainda não foi cotejado** com afirmações do manual.
7. ~~§6.3: atribuição ao modelo B-MARIA não conferida~~ → **resolvido em 16 jun. 2026**: HADDAD; PORSSE; PEREDA (2013, p. 23), lido diretamente, nomeia e descreve o **B-MARIA** (Haddad, 1999): 27 regiões, 56 setores, 110 *commodities*, calibrado para 2005-2007. A aplicação às enchentes de SP (HADDAD; TEIXEIRA, 2015) segue sem o artigo final lido (cópia local é o *working paper*), mas o nome e a estrutura do modelo estão agora verificados (§6.4).
8. **JUNIUS; OOSTERHAVEN (2003)** e **TEMURSHOEV; MILLER; BOUWMEESTER (2013)**: cópias não obtidas (paywall) — o GRAS está coberto pela exposição corrigida de LENZEN; WOOD; GALLEGO (2007), lida diretamente; o caso-limite $p_i=0$ atribuído a Temurshoev et al. foi **derivado** da restrição (7a), não lido.

**Lacunas resolvidas na revisão de 10 jun. 2026:**
1. ~~Equação da Matriz Bm~~ → verificado que a publicação IBGE **não traz** a equação; a analogia $Bm = Um\langle g\rangle^{-1}$ permanece declarada como tal (§3).
2. ~~Fórmulas de campo de influência / SDA / extração~~ → documentadas nas §§4.8, 4.9 e 4.12 a partir de GUILHOTO (2011) e MILLER; BLAIR (2009).
3. ~~Seções 1–3 sem conferência na fonte primária~~ → verificadas contra a cópia local da publicação IBGE nº 62 (eqs. 1–10).
4. ~~Data da edição de Miller & Blair~~ → copyright 2009 confirmado no exemplar local.
5. ~~Definição da matriz de Miyazawa~~ → releitura dirigida de M&B §6.4: $K=(I-VBC)^{-1}$, decomposição em blocos (eqs. 6.41–6.43) — corrigida a forma "$K=(I-HC)^{-1}$" extraída incorretamente na 1ª passada (§4.11).
6. ~~Números de equação do SDA~~ → a 1ª extração reportara "eqs. 13.36–13.37, p. 617-620"; conferência direta no exemplar mostrou **eqs. 13.2–13.7, p. 593-596**, e acrescentou as formas com interação e a decomposição de $\Delta f$ em nível/mix/distribuição (eqs. 13.13–13.20, p. 599-601) (§4.12).
7. ~~Campo de influência sem a formulação de M&B~~ → §12.3.6 (p. 578) e Apêndice 12.1 (eqs. A12.1.3–A12.1.4, p. 583-585, conferidas diretamente) (§4.8).
8. ~~HADDAD et al. (2017) sem verificação~~ → baixado e conferido; §6.2 verificada contra o resumo/introdução (autores: Haddad, Gonçalves Junior e Nascimento).
11. ~~IIOAS só por resumo/introdução; B-MARIA não conferido; sem dados regionais~~ → **resolvido em 16 jun. 2026** com as fontes adicionadas pela Talita: artigo RBERU completo do IIOAS (eqs. 1–39) e da MIIP 2019 lidos diretamente (§6.2); B-MARIA verificado (§6.4); e **duas matrizes interestaduais prontas** (2011 e 2019) na pasta, a de 2011 carregada e validada como sistema de Leontief consistente (§6.3). A "abertura por estado" passou de "estimar" para "usar dado pronto".
9. ~~Validação do pipeline restrita a 2015~~ → série 2010–2018 validada + triângulo com a MIP oficial 2015 (§1.4), com correção de bug de leitura dos códigos de produto de 2016 no `mipcore.tru`.
10. ~~GRAS sem fonte primária lida (antiga lacuna aberta nº 8)~~ → LENZEN; WOOD; GALLEGO (2007) baixado e **lido diretamente** em 11 jun. 2026 (eqs. 3, 6a–9); algoritmo implementado em `mipcore.gras` com o exemplo da p. 463 como teste unitário, validação retroativa na §2.5 e projeção 2022 gerada. Remanescente registrado na nova lacuna nº 8 (J&O 2003 e Temurshoev 2013 não obtidos).

**Verificação ponto a ponto — com camadas de confiança declaradas (atualizado na sessão de releitura de 10 jun. 2026):**
- **Conferido por leitura direta** (camada ✅ plena): IBGE 2018 (Quadro 1, CIF/FOB, hipóteses, eqs. 1–10); **GUILHOTO; SESSO FILHO (2005)** — algoritmo, identidades, eqs. 1–19, limitação da margem (tudo confere; tabelas do PDF não renderizam); **GUILHOTO; SESSO FILHO (2010)** — eqs. 1–7, 42/55 setores, Tabela 4, viés de superestimação do tipo II; **GUILHOTO (2011)** — todas as 8 citações do manual (3.8–3.12; §3.4; 4.35–4.41; 6.8–6.12; 6.16–6.29; 7.1–7.20; 8.1–8.7; 9.1–9.8); **MILLER; BLAIR (2009)** — §10.3 (eqs. 10.1–10.2, generalizado), §10.4.7 (ecológicas, p. 473-475), §12.1 (Ghosh, 12.1–12.17), §12.1.5 (preços, 12.18–12.21), §12.2 (ligações 12.22–12.29; extração, Tabela 12.5), §12.3.6 (campo de influência), Apêndice 12.1, §13.1 (SDA, 13.2–13.20), copyright; identidades das tabelas oficiais 02–10 (validação aritmética exata); todos os benchmarks numéricos (refazíveis por script).
- **Promovidos a leitura direta na mesma sessão:** M&B §6.2 (eqs. 6.11–6.16, multiplicadores de renda tipo I/II), §6.4 (Miyazawa: V, C, $VBC=L$, $K=(I-VBC)^{-1}$, eqs. 6.37–6.47 — a eq. 6.44 $x=(I-A-CV)^{-1}f^*$ coincide com GUILHOTO, 2011, eq. 9.7) e §7.4.1 (RAS, eqs. 7.3–7.16).
- **Promovidos a leitura direta no bloco final (11 jun. 2026):** M&B p. 254 (razão II/I aproximadamente constante entre setores — literal) e §§7.4.4–7.4.6 (interpretação substituição/fabricação atribuída a Stone, 1961, §7.4.4, p. 329; preservação de sinais e zeros, p. 329; RAS modificado, eq. 7.36, p. 330); **MIP-Nordeste** (eqs. 50–52, 64–70, 74–77, 78–82, 84–87, 88–93 conferidas; 111 setores e 169 produtos nos Quadros 4–5 e p. 57; ano-base 2004; 27 UFs no §2.8.4, p. 58); **BULLARD; SEBALD (1977)** (eq. 3, p. 77 + ressalva "very loose"); **BULLARD; SEBALD (1988)** (p. 708-711 — com correção do §7.2, ver registro de erros); **LEONTIEF (1967)** (eq. 7, p. 414; eq. 11, p. 415); **LEONTIEF (1970)** (eqs. 5/5a e exemplo, p. 262-265; coluna de abatimento p. 266+ não relida, corroborada por M&B §10.5); **WOLSKY (1984)** (p. 283-285: eqs. 5–16, Apêndice A, pesos por demonstrações financeiras/associações setoriais); **ZHOU; KOJIMA (2010)** (Parte I, §§2–3: eqs. I.1–I.5 e I.14–I.16, Tabela I.4; notação do manual reescrita na forma original do paper).
- **Adicionado por leitura direta em 11 jun. 2026:** LENZEN; WOOD; GALLEGO (2007) — GRAS corrigido, eqs. 3, 6a–9, exemplo numérico p. 463 (§2.3, §2.5; implementado e testado em `mipcore.gras`).
- **Adicionado por leitura direta em 16 jun. 2026** (novas fontes da Talita): HADDAD; GONÇALVES JUNIOR; NASCIMENTO (2017) e HADDAD; ARAÚJO; ROCHA; VALE (2025) — método IIOAS completo, eqs. 1–39 (§6.2); HADDAD; PORSSE; PEREDA (2013) — modelo B-MARIA, p. 23 (§6.4); matriz interestadual 2011 carregada e validada numericamente, $(I-A)B=I$ a $7\times10^{-15}$ (§6.3); GUILHOTO; SONIS; HEWINGS (MPM inter-regional, eqs. 1–31) e SONIS; GUILHOTO; HEWINGS; MARTINS (*Some New Perspectives*, eqs. 1–33) — base da nova §4.15 (MPM) e fonte primária de §4.5 (ligações puras GHS) e §4.8 (campo de influência).
- **Adicionado em 17 jun. 2026 (auditoria de estado da arte, governada pela skill `pesquisa-tecnica`):** KOOPMAN; WANG; WEI (2014, eqs. 13–24) e BORIN; MANCINI (2019, §§1-2) — lidos diretamente, base da nova §4.16 (decomposição de exportações em valor adicionado/GVC). **Verificado em fonte oficial, sem leitura integral:** IBGE *Nota Técnica 01/2024* (transição SCN 2010→2021, MIP a reformular, adoção do SNA 2025; advertência de vigência no §1, lida diretamente) e *Nota Metodológica nº 1* (2025); edições vigentes de FIGARO (2024) e OECD ICIO (2023), com Brasil incluído (§6.5). **Não verificado por leitura direta** (citado de fonte secundária ou só por status): SNA 2025 (citado pela adoção declarada do IBGE); JOHNSON; NOGUERA (2012) e HUMMELS; ISHII; YI (2001) (via KWW/Borin-Mancini); versões vigentes de EXIOBASE, EORA, GTAP e ADB MRIO (§6.5); a derivação multi-país completa de Borin-Mancini (registrado o arcabouço, não reimplementado).
- **Permanecem fora da camada de leitura direta** (apenas estes): M&B Apêndice 6.2 (formalização da razão II/I); LEONTIEF (1970) p. 266 em diante (atividade de abatimento — corroborada por fonte secundária verificada); HADDAD; TEIXEIRA (2015) artigo final (cópia local é o *working paper*; nome/estrutura do B-MARIA conferidos via HADDAD; PORSSE; PEREDA, 2013); e os itens das lacunas abertas acima (IBGE 2016 v. 24 não cotejado; DIXON; RIMMER 2004, JUNIUS; OOSTERHAVEN 2003 e TEMURSHOEV et al. 2013 citados via fonte secundária).

**Registro de erros encontrados nas releituras (regra 7 — inclusive os meus):**
1. 1ª rodada: agente afirmou $Q$ **sem** transposta; eu "corrigi" o manual — **a leitura direta mostrou que a transposta existe no livro** ($Q = N'\hat{x}^{-1}$, p. 474) e a fórmula original do manual estava certa. Restaurada.
2. 2ª rodada: agente afirmou que o livro usa $D$ e não $D^p$ — **o livro usa $D^p$ nas eqs. 10.1–10.2**; nota de "adaptação de notação" removida.
3. Agentes erraram números de equação do SDA (13.36→13.2-13.7) e a forma de Miyazawa ((I−HC)⁻¹→(I−VBC)⁻¹) — corrigidos em rodadas anteriores.
4. A suspeita de erro de extração nas citações do cap. 3 de GUILHOTO (2011) era infundada: **a própria fonte duplica os números** 3.10–3.12 entre §3.2 e §3.4 (falha tipográfica do working paper) — ambas as citações corretas; citar sempre seção + equação.
5. Typo na fonte GUILHOTO (2011, eq. 6.19): imprime $(I-A_{jj})^{-1}$ onde deveria ser $A_{rr}$.
6. Bloco final (11 jun. 2026): o §7.2 dizia "97,5% dos elementos da inversa ficaram a ~2% do valor publicado" — **conflação de dois resultados distintos** de Bullard e Sebald (1988): o correto é ">90% dos elementos com média populacional a <2% da amostral (95% de confiança)"; os 97,5% referem-se à cota sobre os desvios-padrão (1,16×). Também eram imprecisos "milhares de inversões" (são 1.000) e "agregação 360→30" (base 360→90, com testes 90→30 e 101). Corrigido por leitura direta.
7. Bloco final: a fórmula MRIO atribuída a ZHOU; KOJIMA (2010) usava símbolos que não são os do paper ($E$ para emissões, quando no paper $E$ são exportações; $e$, $Y$ em vez de $c$, $F$) — substância correta, notação reescrita na forma original (eqs. I.1–I.5).

**Nota sobre cópias locais:** `ERSA2013_paper_00409.pdf` é a versão working paper (ERSA 2013) de HADDAD; TEIXEIRA (2015); `files.pdf` é um press release do Monitor do PIB FGV-IBRE, sem relação com este manual.

**Deduplicação executada em 16 jun. 2026** (md5 binário + hash de conteúdo normalizado; 9 arquivos removidos, persistência verificada na sessão): byte-idênticos — `liv101604.pdf` (= `IBGE-2018-MIP-Brasil-2015-liv101604.pdf`), `ssrn-1853629.pdf` (= `MIP-Nordeste-2004.pdf`), `Brown-...-1979 (1).pdf` e `(2).pdf` (= original), `Raa-...-1986 (1).pdf` (= original); conteúdo idêntico (só carimbo/capa diferia) — `Leontief-AlternativeAggregationInputOutput-1967 (1).pdf` (= original), `ssrn-2417390.pdf` (= `ssrn-2414028.pdf`), `ssrn-1900073.pdf` (= Guilhoto 2011 MPRA), `ssrn-1836495.pdf` (= GS2010). 📌 **Correção (regra 7):** versão anterior desta nota afirmava que as cópias "(1)/(2)" de **Brown-1979 e Raa-1986** "diferem em bytes e foram mantidas" — **estava errado**: eram byte-idênticas (md5 confirmado) e foram removidas agora. Apenas as duas cópias de **Leontief-AlternativeAggregation-1967** de fato diferiam em bytes (mesmo conteúdo, carimbo JSTOR distinto); manteve-se uma. ⚠️ **Não removidas** (mesmo paper, versões com conteúdo diferente — decisão da Talita): as duas cópias de GS2010 com nomes distintos (`Guilhoto-Sesso_2010_Estimacao-MIP-Brasil-2005.pdf` e `Metodologia-guilhoto-sesso-EA-2010.pdf`). ⚠️ Se o OneDrive ressincronizar algum arquivo removido (já ocorreu antes), apagá-lo pela interface web do OneDrive força a remoção na nuvem. A nota metodológica do CEPEA continua **sem cópia na pasta** (citada de fonte online). Removido em 16 jun. 2026: `Temurshoev-Miller-Bouwmeester-2013-Note-GRAS.pdf` era um HTML de 5,8 KB (tentativa de download que falhou em 11 jun., não um PDF; o GRAS está coberto por LENZEN; WOOD; GALLEGO, 2007). **Fontes adicionadas pela Talita em 16 jun. 2026** (todas lidas diretamente): `document.pdf`, `7_1225ed.pdf`, `administrador,+02+Haddad+et+al._..._2013.pdf`, e as matrizes `administrador,+IIOAS_Brasil_RBERU_2017.xlsx` (2011) e `IIOAS_BRUF_2019 (1).rar` (2019). **Segundo lote (8 PDFs SSRN de teoria de IO), com deduplicação verificada por conteúdo:** `ssrn-1900073` ≈ `Guilhoto-2011-MPRA32566` (mesmo paper, difere ~1%); `ssrn-1836495` ≈ GS2010 já na pasta; `ssrn-2414028` = `ssrn-2417390` (idênticos, "Leontief: antecedentes"); `ssrn-1853629` = MIP-Nordeste (ressincronizado pelo OneDrive após remoção em 10 jun.). **Genuinamente novos (mantidos):** `ssrn-2417397` (MPM inter-regional, base da nova §4.15), `ssrn-2420129`/`ssrn-2420472` (ligações/setores-chave, fonte primária de §4.5 e §4.8), `ssrn-2408067` (história das tabelas de IO do Brasil). As cópias redundantes deste lote foram **removidas** em 16 jun. 2026 (ver o parágrafo "Deduplicação executada" acima).

Datas de acesso às fontes online: **2 jun. 2026** (originais), **10 jun. 2026** (IBGE nº 62 e GUILHOTO, 2011), **11 jun. 2026** (LENZEN; WOOD; GALLEGO, 2007, para o GRAS), **16 jun. 2026** (cotejo das fontes IIOAS/B-MARIA e validação das matrizes interestaduais adicionadas pela Talita) e **17 jun. 2026** (auditoria de estado da arte: IBGE Nota Técnica 01/2024, SNA 2025, FIGARO/ICIO, e download e leitura de KOOPMAN; WANG; WEI, 2014 e BORIN; MANCINI, 2019).
