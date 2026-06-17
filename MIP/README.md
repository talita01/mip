# MIP — Toolkit de Matriz Insumo-Produto (reutilizável)

Pacote `mipcore`: ferramentas de insumo-produto a partir dos dados oficiais do IBGE, **independentes de
qualquer aplicação** (serve para qualquer análise de IO sob demanda — multiplicadores, setores-chave,
impacto de demanda, pegadas, etc.).

## Ambiente (venv LOCAL, fora do OneDrive)

> ⚠️ O venv NÃO fica no OneDrive (milhares de arquivos causam falhas de sincronização). Fica local:

```
python3 -m venv ~/.venvs/fgv-mip
source ~/.venvs/fgv-mip/bin/activate
pip install -e "<caminho>/mip/MIP"   # instala o mipcore (editável)
pip install statsmodels              # usado pela aplicação PIB-Bio
```

## Uso

```python
import mipcore as mip

d = mip.tru.carregar(2019)                 # Tabela de Recursos e Usos, nível 68
print(mip.tru.checar_identidades(2019))    # controles contábeis (devem fechar)

m = mip.leontief.matrizes(d)               # D, Bn, A (ativ×ativ), L = (I-A)^-1
mp = mip.multiplicadores.producao_tipo1(m["L"])              # multiplicador de produção
trás, frente = mip.multiplicadores.rasmussen_hirschman(m["L"])  # setores-chave (>1)
ghs = mip.multiplicadores.ligacoes_puras_ghs(m["A"], y, j)      # ligações puras GHS
g_va = mip.multiplicadores.gerador(m["v"], m["L"])              # gerador de VA (pegada)

val, tris = mip.cnt.carregar()             # Contas Nacionais Trimestrais (SIDRA)
```

## Módulos (`mipcore/`)

| Módulo | O que faz |
|---|---|
| `tru` | Lê as TRU do IBGE (nível 68, qualquer ano 2010–2021); identidades de controle. |
| `precos_basicos` | Passagem a preços básicos pela estrutura oficial da MIP 2015. |
| `leontief` | Matrizes D, Bn, A e a inversa de Leontief; controles. |
| `multiplicadores` | Produção, geradores (VA/renda/emprego), Rasmussen-Hirschman, ligações puras GHS. |
| `sda` | Decomposição estrutural (tecnologia × demanda) a preços constantes, pares anuais encadeados (TRU ano-anterior). |
| `cnt` | Contas Nacionais Trimestrais via API SIDRA (tabelas 1846/1620). |

## Dados
`dados/brutos/`: TRU nível 68 correntes (2010–2021, `tru_anos/`) e a preços do ano anterior
(2011–2021, `tru_ano_anterior/`, tab3/tab4), MIP oficial 2015 (nível 67), TRU nível 12
(2021–2022). Fonte: IBGE/SIDRA.
`dados/estimadas/`: MIP estimadas 2019–2021 (68 setores) geradas por `gerar_matrizes_estimadas.py`
— estendem a série de Guilhoto (2010–2018, na pasta `mip/`) até o último ano com TRU 68.

## Método de preços básicos e validação
Desde 10/jun/2026 o padrão é o **método híbrido** (shares de destino das tabelas oficiais 04–10
da MIP 2015 × totais do próprio ano, fallback α_ij de Guilhoto-Sesso, realocação de margens) —
escolhido por benchmark fora da amostra (Tabela 03 de 2010: WMAPE 5,5% vs 8,1% GS-puro vs 16,4%
do método r_int anterior, descontinuado). Validação downstream: MIP oficial 2015 r(L)=1,0000
(desvio dos multiplicadores 0,15%); matrizes de Guilhoto 2010–2018 r(L)≥0,9987 (desvio médio
1,84%). Detalhes: §§1.4 e 2.4 do `Manual-Metodologico-Insumo-Produto.md`.

## Metodologia
Ver `Manual-Metodologico-Insumo-Produto.md` (na pasta mip): IBGE (2018), Miller & Blair (2009),
Guilhoto & Sesso Filho (2005), com referências ABNT.
