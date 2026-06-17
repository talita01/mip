"""
mipcore.sda — Análise de Decomposição Estrutural (SDA) a preços constantes.

Decompõe a variação da produção entre anos consecutivos em mudança TECNOLÓGICA (ΔL) e
mudança de DEMANDA FINAL (Δf), pela média das formas polares (Miller & Blair, 2009,
§13.1, eq. 13.7, p. 595):

    Δx = ½·(ΔL)·(f0 + f1) + ½·(L0 + L1)·(Δf)

Preços constantes via TRU "ano anterior" do IBGE (68_tab3/tab4: ano t valorado a preços
de t-1), pareadas com as TRU correntes de t-1 — cada par fica numa mesma base de preços,
e a série é encadeada ano a ano (sem deflator externo).

Aproximação herdada de mipcore.precos_basicos: estrutura de margens/impostos da MIP 2015.
"""
from pathlib import Path
import numpy as np
import xlrd
from . import tru, leontief

DADOS_PA = Path(__file__).resolve().parent.parent / "dados" / "brutos" / "tru_ano_anterior"


def carregar_ano_anterior(ano):
    """TRU do ano `ano` valorada a preços do ano anterior (68_tab3/tab4).
    Mesmo formato de tru.carregar; g e q calculados da matriz de produção (IBGE, eqs. 1 e 5)."""
    t3 = xlrd.open_workbook(DADOS_PA / f"68_tab3_{ano}.xls")
    t4 = xlrd.open_workbook(DADOS_PA / f"68_tab4_{ano}.xls")
    prod_ws = t3.sheet_by_name("producao")
    produtos = [tru._cod(prod_ws.cell_value(r, 0), 5) for r in range(tru.R0, tru.R1)]
    of = t3.sheet_by_name("oferta")
    oferta = {k: tru._num(of, tru.R0, tru.R1, c, c + 1).ravel() for k, c in
              [("oferta_pc", 2), ("MGC", 3), ("MGT", 4), ("II", 5), ("IPI", 6),
               ("ICMS", 7), ("OUTROS", 8), ("IMPOSTOS", 9), ("oferta_pb", 10)]}
    V = tru._num(prod_ws, tru.R0, tru.R1, 2, 2 + tru.N_ATIV)
    U = tru._num(t4.sheet_by_name("CI"), tru.R0, tru.R1, 2, 2 + tru.N_ATIV)
    g = V.sum(0)                             # g_j = Σ_i v_ij  (IBGE, eq. 5)
    return {
        "ano": ano, "produtos": produtos, "atividades": tru.codigos_atividades(),
        "oferta": oferta, "V_pa": V,
        "importacao": tru._num(t3.sheet_by_name("importacao"), tru.R0, tru.R1, 2, 3).ravel(),
        "U_pa": U,
        "DF": tru._num(t4.sheet_by_name("demanda"), tru.R0, tru.R1, 2, 8),
        "demanda_cols": ["exportacao", "governo", "isflsf", "familias", "fbcf", "estoque"],
        "VA": {"VAB": g - U.sum(0), "valor_prod": g},   # identidade: VAB = g - CI da atividade
        "g": g,
        "q": V.sum(1),                       # q_i = Σ_j v_ij  (IBGE, eq. 1)
    }


def _sistema(d):
    m = leontief.matrizes(d)
    f = m["g"] - m["Z"].sum(1)               # demanda final por atividade (resíduo: L·f = g exato)
    return m["A"], m["L"], f, m["g"]


def decompor_par(ano):
    """SDA do par (ano-1 → ano), ambos a preços de (ano-1). Retorna dict com vetores por
    atividade: dx, tec (contribuição de ΔL), dem (contribuição de Δf), x0."""
    A0, L0, f0, x0 = _sistema(tru.carregar(ano - 1))
    A1, L1, f1, x1 = _sistema(carregar_ano_anterior(ano))
    dL, df = L1 - L0, f1 - f0
    tec = 0.5 * dL @ (f0 + f1)               # eq. 13.7, termo de tecnologia
    dem = 0.5 * (L0 + L1) @ df               # eq. 13.7, termo de demanda final
    return {"ano": ano, "dx": x1 - x0, "tec": tec, "dem": dem, "x0": x0,
            "residuo": float(np.abs((x1 - x0) - (tec + dem)).max())}


def serie(anos=range(2011, 2022)):
    """SDA encadeado para a sequência de anos (cada par a preços do ano inicial do par)."""
    return [decompor_par(a) for a in anos]


def demanda_por_categoria(d):
    """Demanda final por ATIVIDADE × categoria (68×6), consistente com o resíduo f = g − Z·i.

    Usa o bloco de demanda final do método híbrido (precos_basicos.uso_basico_hibrido —
    nacional a preços básicos, por categoria), leva ao espaço de atividades via market-share
    D e reescala cada linha para que a soma das categorias feche com o resíduo contábil."""
    from . import precos_basicos
    m = leontief.matrizes(d)
    f_res = m["g"] - m["Z"].sum(1)
    DFb = precos_basicos.uso_basico_hibrido(d)[:, 68:]       # produto × 6 categorias, nac. básico
    E = m["D"] @ DFb                                         # atividade × 6 categorias
    soma = E.sum(1)
    esc = np.divide(f_res, soma, out=np.ones_like(soma), where=np.abs(soma) > 1e-9)
    return E * esc[:, None]


def decompor_par_categorias(ano):
    """Como decompor_par, com o termo de demanda aberto pelas 6 categorias da TRU
    (Δf = Σ_k Δf_k; contribuição da categoria k = ½(L0+L1)·Δf_k)."""
    d0, d1 = tru.carregar(ano - 1), carregar_ano_anterior(ano)
    A0, L0, f0, x0 = _sistema(d0)
    A1, L1, f1, x1 = _sistema(d1)
    E0, E1 = demanda_por_categoria(d0), demanda_por_categoria(d1)
    Lm = 0.5 * (L0 + L1)
    dem_k = Lm @ (E1 - E0)                                   # 68 × 6: efeito-demanda por categoria
    tec = 0.5 * (L1 - L0) @ (f0 + f1)
    return {"ano": ano, "dx": x1 - x0, "tec": tec, "dem_k": dem_k, "x0": x0,
            "categorias": d0["demanda_cols"],
            "residuo": float(np.abs((x1 - x0) - (tec + dem_k.sum(1))).max())}
