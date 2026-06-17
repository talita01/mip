# Cookbook — pergunta de pesquisa → comando → resultado

Receitas rodáveis sobre o `mipcore`. Cada uma liga uma pergunta do guia de decisão (§9 do
[manual](Manual-Metodologico-Insumo-Produto.md)) ao código que a responde. Todos os
trechos foram executados e conferidos. Pré-requisito: `import mipcore as m` (ver
[README](README.md) para o setup do venv).

> Convenção dos dados: `m.tru.carregar(ano)` lê a TRU nível 68 já a preços básicos pelo
> método híbrido (§2.4). `m.leontief.matrizes(d)` devolve um dict com `A`, `L` (inversa de
> Leontief), `Z` (usos intersetoriais), `g` (VBP), `VAB` e `atividades` (códigos).

---

## 1. Quais setores mais irradiam crescimento? (multiplicadores e setores-chave)
§9: "Quais setores mais irradiam crescimento?" → R-H sobre `L`.

```python
import numpy as np, mipcore as m
d   = m.tru.carregar(2019)
mat = m.leontief.matrizes(d)
mp           = m.multiplicadores.producao_tipo1(mat["L"])      # multiplicador de produção
tras, frente = m.multiplicadores.rasmussen_hirschman(mat["L"]) # índices R-H (>1 = setor-chave)
cod = [c.strip() for c in mat["atividades"]]
chave = [(cod[i], round(tras[i],2), round(frente[i],2))
         for i in range(len(cod)) if tras[i] > 1 and frente[i] > 1]
print("setores-chave (R-H para trás e para frente > 1):", chave[:10])
```

## 2. Quanto a produção muda se a demanda final mudar? (impacto de demanda)
§9: "Quanto a produção total muda se a demanda final muda?" → ΔX = L · Δf.

```python
import numpy as np, mipcore as m
mat = m.leontief.matrizes(m.tru.carregar(2019))
delta_f = np.zeros(len(mat["atividades"]))
delta_f[0] = 1000.0                      # +R$ 1 bi de demanda final no setor 1 (agricultura)
delta_x = mat["L"] @ delta_f             # impacto na produção de todos os setores
print("produção total induzida:", round(delta_x.sum(), 1), "(multiplicador agregado do choque)")
```

## 3. Impacto sobre emprego/renda/impostos? (geradores e multiplicadores)
§4.3. Precisa de um vetor de coeficiente setorial externo (ex.: emprego por R$ de produção,
da RAIS/PNAD); o `mipcore` não embute esse dado.

```python
import numpy as np, mipcore as m
mat = m.leontief.matrizes(m.tru.carregar(2019))
coef = mat["VAB"] / mat["g"]                       # exemplo: VA por R$ de produção
gerador = m.multiplicadores.gerador(coef, mat["L"])   # efeito direto+indireto por setor
mult    = m.multiplicadores.multiplicador(coef, mat["L"])  # multiplicador (total/direto)
print("gerador de VA — média:", round(gerador.mean(), 3))
```

## 4. Setores-chave ponderando a escala (ligações puras GHS)
§4.5. Corrige o R-H por não ponderar o tamanho do setor.

```python
import mipcore as m
mat = m.leontief.matrizes(m.tru.carregar(2019))
Y = mat["g"] - mat["Z"].sum(1)                     # demanda final por resíduo
ghs = m.multiplicadores.ghs_todos(mat["A"], Y)     # dict: "PTL" (ligação pura total) e "PTLN" (normalizada)
cod = [c.strip() for c in mat["atividades"]]
top = sorted(range(len(cod)), key=lambda i: ghs["PTL"][i], reverse=True)[:10]
print("top 10 por ligação pura total:", [cod[i] for i in top])
# para um único setor: m.multiplicadores.ligacoes_puras_ghs(mat["A"], Y, j) -> {"PBL","PFL","PTL"}
```

## 5. O crescimento veio de tecnologia ou de demanda? (decomposição estrutural)
§4.12. SDA a preços constantes, por pares de anos encadeados.

```python
import mipcore as m
serie = m.sda.serie(range(2011, 2022))   # lista de dicts: ano, dx, tec, dem, x0, residuo
for r in serie:                          # efeito-tecnologia vs efeito-demanda, agregados
    print(r["ano"], "| ΔX:", round(r["dx"].sum()),
          "| tecnologia:", round(r["tec"].sum()), "| demanda:", round(r["dem"].sum()))
# abertura do efeito-demanda pelas 6 categorias da TRU: sda.decompor_par_categorias(ano)
```

## 6. Estimar a MIP de um ano (nacional)
Ano **com** TRU 68 (2010–2021): use o gerador ou a skill `/estimar-mip <ano>`.

```bash
~/.venvs/fgv-mip/bin/python MIP/gerar_matrizes_estimadas.py 2021
```

Ano **sem** TRU 68 (2022+): projeção GRAS a partir do último ano disponível (§2.5). Camada
de confiabilidade inferior; não usar para SDA.

```python
import mipcore as m
est = m.gras.estimar(2022, 2021)          # projeta 2022 a partir de 2021 + TRU nível 12
print("max soma de coluna de A:", round(est["A"].sum(0).max(), 3))
# ou: ~/.venvs/fgv-mip/bin/python MIP/gerar_matriz_gras.py 2022 2021
```

## 7. Análise por estado (sistema interestadual IIOAS)
§6. Multiplicadores e setores-chave por UF, autossuficiência, extração de um estado. Anos
2019 e 2011 (para a 2019, extraia o `.rar` uma vez — ver [README](README.md), seção Setup).

```python
import mipcore as m
sys = m.regional.carregar(2019)                       # 27 UFs × 68 setores (ano mais recente)
# sys = m.regional.carregar(2011)                     # ano alternativo (matriz com A/B prontas)

mp = m.regional.multiplicador_producao(sys)           # array (27, 68): UF × setor
i_sp = sys["uf"].index("SP")
print("multiplicador de produção, SP, setor 1:", round(mp[i_sp, 0], 2))

aut = m.regional.autossuficiencia_uf(sys)             # participação intra-regional dos insumos
print("autossuficiência SP:", round(aut["SP"], 3), "| RR:", round(aut["RR"], 3))

df = m.regional.demanda_final(sys)                    # demanda final regional (validada: L·f = VBP)
print("demanda final total: R$", round(df["total"].sum()/1e6, 2), "tri")
if df["categorias"]:                                  # composição (só 2019): famílias, governo, etc.
    print({c: round(v.sum()/1e6, 2) for c, v in df["categorias"].items()})

ext = m.regional.extracao_regiao(sys, "SP")           # extração de UF: usa a demanda final REAL por padrão
print("impacto de extrair SP:", round(ext["impacto_relativo"]*100, 1), "% (", ext["nota"], ")")

Luf = m.regional.agregar_uf(sys["L"])                 # inversa agregada a 27×27
mpm = m.regional.mpm(Luf)                             # matriz de multiplicadores-produto (§4.15)
```

---

## Comércio em valor adicionado / cadeias globais (GVC)
§4.16. **Não roda só com a MIP nacional**: exige uma base inter-país (ICIO/MRIO) — FIGARO,
OECD ICIO etc. (§6.5). O `mipcore` ainda não implementa a decomposição de Koopman-Wang-Wei /
Borin-Mancini; o manual documenta o arcabouço. Frente a desenvolver quando houver a base.
