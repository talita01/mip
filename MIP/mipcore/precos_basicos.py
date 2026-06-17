"""
mipcore.precos_basicos — Passagem do uso a preço de consumidor para preço básico nacional.

MÉTODO PADRÃO (desde 10/jun/2026): HÍBRIDO — participações de destino célula a célula das
tabelas oficiais 04–10 da MIP 2015 (IBGE) aplicadas aos TOTAIS do próprio ano (margens,
impostos e importações da aba `oferta` da TRU), com fallback nos coeficientes α_ij de
Guilhoto–Sesso (2005) onde a estrutura de 2015 é vazia, e realocação das margens às linhas
de comércio (45001/46801) e transporte (49001/50001).

Justificativa empírica (benchmark fora da amostra, reconstruindo a Tabela 03 oficial de 2010;
ver Manual, §2.3-bis): WMAPE de 5,5% vs 8,1% (Guilhoto–Sesso puro) vs 16,4% (método anterior,
razão r_int por produto — descontinuado como padrão por erro de 63% nas linhas de margem).

O método anterior (r_int) permanece disponível via uso_nacional_basico(d, r_int=...) apenas
para reprodutibilidade de resultados antigos.
"""
from pathlib import Path
import numpy as np
import xlrd

ARQ = Path(__file__).resolve().parent.parent / "dados" / "brutos" / "Matriz_de_Insumo_Produto_2015_Nivel_67.xls"
_NI67 = 67          # atividades no nível 67
_cache = {}


def _num(wb, sh, r0, r1, c0, c1):
    ws = wb.sheet_by_name(sh); o = np.zeros((r1 - r0, c1 - c0))
    for i, r in enumerate(range(r0, r1)):
        for j, c in enumerate(range(c0, c1)):
            v = ws.cell_value(r, c); o[i, j] = v if isinstance(v, (int, float)) else 0.0
    return o


def _bloco(wb, sh, c0):
    """Bloco 127 produtos × (67 atividades + 6 categorias de demanda final)."""
    ws = wb.sheet_by_name(sh)
    cols = list(range(c0, c0 + _NI67)) + list(range(c0 + _NI67 + 1, c0 + _NI67 + 7))
    return np.array([[ws.cell_value(r, c) if isinstance(ws.cell_value(r, c), (int, float)) else 0.0
                      for c in cols] for r in range(5, 132)])


def estrutura_2015():
    """Tabelas de destino da MIP 2015 (127 × 73) e metadados. Cacheado."""
    if "e15" in _cache:
        return _cache["e15"]
    wb = xlrd.open_workbook(ARQ)
    prod = [str(wb.sheet_by_name("02").cell_value(r, 0)).strip() for r in range(5, 132)]
    ativ = [str(wb.sheet_by_name("14").cell_value(r, 0)).strip() for r in range(5, 72)]
    T = {s: _bloco(wb, s, 2 if s == "02" else 3) for s in
         ["02", "03", "04", "05", "06", "07", "08", "09", "10"]}
    comp = {"imp": T["04"], "tax": T["05"] + T["06"], "mgc": T["07"] + T["08"], "mgt": T["09"] + T["10"]}
    # fração da margem de transporte realocada ao transporte terrestre (49001), por coluna
    dif = T["02"] - sum(T[s] for s in ["03", "04", "05", "06", "07", "08", "09", "10"])
    iTER = prod.index("49001")
    mgt_col = comp["mgt"].sum(0)
    frac_ter = np.clip(np.where(np.abs(mgt_col) > 1e-9,
                                dif[iTER] / -np.where(mgt_col == 0, 1.0, mgt_col), 1.0), 0, 1)
    _cache["e15"] = {"prod": prod, "ativ": ativ, "comp": comp, "frac_ter": frac_ter}
    return _cache["e15"]


def _shares(M, alpha_fb):
    rt = M.sum(1)
    s = np.divide(M, rt[:, None], out=np.zeros_like(M), where=np.abs(rt[:, None]) > 1e-9)
    vazio = np.abs(rt) < 1e-9
    s[vazio] = alpha_fb[vazio]
    return s


def _expandir(M67, d, e15):
    """127×73 (nível 67) → 128×74 (nível TRU 68): ponte de produtos (45001/46801 ← 45801)
    e split da coluna de comércio 4580 → 4500/4680 proporcional ao uso do próprio ano."""
    prod_t, ativ_t = d["produtos"], [a.strip() for a in d["atividades"]]
    lin = [e15["prod"].index(p) if p in e15["prod"] else e15["prod"].index("45801") for p in prod_t]
    M = M67[lin]                                            # 128 × 73
    j45, j46 = ativ_t.index("4500"), ativ_t.index("4680")
    c4580 = e15["ativ"].index("4580")
    out = np.zeros((len(prod_t), 68 + 6))
    w = np.divide(d["U_pa"][:, j45], d["U_pa"][:, j45] + d["U_pa"][:, j46],
                  out=np.full(len(prod_t), 0.5), where=(d["U_pa"][:, j45] + d["U_pa"][:, j46]) > 0)
    k67 = 0
    for k68, a in enumerate(ativ_t):
        if a == "4500":
            out[:, k68] = M[:, c4580] * w
        elif a == "4680":
            out[:, k68] = M[:, c4580] * (1 - w)
        else:
            out[:, k68] = M[:, e15["ativ"].index(a)]
    out[:, 68:] = M[:, _NI67:]
    return out


def uso_basico_hibrido(d):
    """Uso NACIONAL a preços BÁSICOS (produto × [68 atividades | 6 categorias DF]) pelo método
    híbrido. Retorna a matriz completa 128×74; o bloco intermediário é [:, :68]."""
    e15 = estrutura_2015()
    of = d["oferta"]
    Z = np.hstack([d["U_pa"], d["DF"]])                     # 128 × 74, preço consumidor
    rs = Z.sum(1)
    alpha = np.divide(Z, rs[:, None], out=np.zeros_like(Z), where=rs[:, None] != 0)
    Zx = Z.copy(); Zx[:, 68] = 0.0                          # zera exportação (1ª categoria DF)
    rsx = Zx.sum(1)
    alphax = np.divide(Zx, rsx[:, None], out=np.zeros_like(Zx), where=rsx[:, None] != 0)

    S = {k: _expandir(_shares(e15["comp"][k], np.zeros_like(e15["comp"][k])), d, e15)
         for k in ("mgc", "mgt", "tax")}
    Simp = _expandir(_shares(e15["comp"]["imp"], np.zeros_like(e15["comp"]["imp"])), d, e15)
    # fallback α onde a estrutura 2015 é vazia
    for k in S:
        vazio = np.abs(S[k]).sum(1) < 1e-12
        S[k][vazio] = alpha[vazio]
    vazio = np.abs(Simp).sum(1) < 1e-12
    Simp[vazio] = alphax[vazio]

    tot = {"mgc": of["MGC"], "mgt": of["MGT"], "tax": of["IPI"] + of["ICMS"] + of["OUTROS"],
           "imp": d["importacao"] + of["II"]}
    dist = {k: tot[k][:, None] * (Simp if k == "imp" else S[k]) for k in tot}

    Ub = Z - dist["mgc"] - dist["mgt"] - dist["tax"] - dist["imp"]
    # realocação das margens às linhas de comércio e transporte
    prod = d["produtos"]
    i45, i46 = prod.index("45001"), prod.index("46801")
    iTER, iAQU = prod.index("49001"), prod.index("50001")
    q45, q46 = d["q"][i45], d["q"][i46]
    w45 = q45 / (q45 + q46) if (q45 + q46) > 0 else 0.5
    mgc_col, mgt_col = dist["mgc"].sum(0), dist["mgt"].sum(0)
    # frac_ter de 2015 por coluna, com ponte 67→68 (colunas de comércio recebem o valor de 4580)
    ft67 = e15["frac_ter"]
    ft = np.zeros(74)
    ativ_t = [a.strip() for a in d["atividades"]]
    for k68, a in enumerate(ativ_t):
        ft[k68] = ft67[e15["ativ"].index("4580")] if a in ("4500", "4680") else ft67[e15["ativ"].index(a)]
    ft[68:] = ft67[_NI67:]
    Ub[i45] += mgc_col * w45
    Ub[i46] += mgc_col * (1 - w45)
    Ub[iTER] += mgt_col * ft
    Ub[iAQU] += mgt_col * (1 - ft)
    return Ub


# ------------------------- método anterior (r_int), mantido p/ reprodutibilidade -------------------------

def taxa_basico_2015():
    """{codigo_produto_2015: r_int} — razão (uso básico / uso consumidor) no intermediário, 2015.
    DESCONTINUADO como padrão (ver docstring do módulo); mantido para reprodutibilidade."""
    wb = xlrd.open_workbook(ARQ)
    pc = [str(wb.sheet_by_name("02").cell_value(r, 0)).strip() for r in range(5, 132)]
    U = _num(wb, "02", 5, 132, 2, 69)
    Ubas = U - _num(wb, "05", 5, 132, 3, 70) - _num(wb, "07", 5, 132, 3, 70) - _num(wb, "09", 5, 132, 3, 70)
    C, B = U.sum(1), Ubas.sum(1)
    r = np.clip(np.divide(B, C, out=np.ones_like(B), where=C != 0), 0.3, 1.0)
    return dict(zip(pc, r))


def r_int_para(codigos_produtos):
    m = taxa_basico_2015()
    return np.array([m.get(c, 1.0) for c in codigos_produtos])


def uso_nacional_basico(d, r_int=None):
    """Matriz de uso intermediário NACIONAL a preços BÁSICOS (produto × atividade).
    Padrão: método HÍBRIDO. Se r_int for passado, usa o método antigo (descontinuado)."""
    if r_int is None:
        return np.nan_to_num(uso_basico_hibrido(d)[:, :68])
    of, U, imp = d["oferta"], d["U_pa"], d["importacao"]
    frac_nac = np.clip(np.divide(of["oferta_pb"] - imp, of["oferta_pb"],
                                 out=np.ones_like(imp), where=of["oferta_pb"] > 0), 0, 1)
    return np.nan_to_num(U * r_int[:, None] * frac_nac[:, None])
