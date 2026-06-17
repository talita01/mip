"""GRAS — atualização da matriz de usos para anos sem TRU nível 68 (2022+).

Método: RAS generalizado (admite células negativas, que existem em Z pelo método
híbrido de margens — ~1,9% da massa, concentradas na linha de comércio).

Fonte do algoritmo (leitura direta, 11 jun. 2026): LENZEN, M.; WOOD, R.; GALLEGO, B.
"Some Comments on the GRAS Method", Economic Systems Research, 19(4), 2007,
eqs. (3), (6a)-(9), p. 464-465 — exposição corrigida do GRAS de Junius & Oosterhaven
(2003). Decomposição A = P - N (P positivos, N módulos dos negativos); solução
x_ij = r_i a_ij s_j para a_ij >= 0 e x_ij = a_ij/(r_i s_j) para a_ij < 0, com r e s
obtidos iterativamente pelas quadráticas (8a)-(8b). Notas de leitura: (i) a eq. (9)
impressa tem typo de subscrito (p_j(s), n_j(s) onde o argumento é r) — usa-se a forma
coerente com as restrições (7a)-(7b); (ii) o caso-limite p_i = 0 (linha/coluna sem
elementos positivos) segue diretamente da restrição (7a): r_i = -n_i/u_i (relaxamento
tratado em Temurshoev, Miller & Bouwmeester, 2013, fonte não lida — aqui derivado).

Margens-alvo para o ano sem TRU 68: margens do ano-base escaladas pelo crescimento
dos 12 blocos da TRU nível 12 (CI por bloco de produto nas linhas, CI por atividade
nas colunas, VBP por atividade para g). Aproximações declaradas: CI nível 12 a preços
de consumidor (inclui importados) transferido a Z (básico, nacional); bloco de produto
~ bloco de atividade; fechamento sum(u)=sum(v) reescalando u; bloco com CI nulo
(adm. pública) usa o crescimento do VBP.

Validação retroativa (validar_ras.py, 11 jun. 2026): multiplicadores tipo I vs matriz
verdadeira de 2021 — base 2020: desvio médio 2,77% (máx 14,4%); base 2019: 2,99%
(máx 13,0%); teto do método com margens verdadeiras: 0,3-0,4%; baseline ingênuo
(A do ano-base sem ajuste): 4,0%. Erros concentrados em setores de choque de preço
(carvão, siderurgia, transporte aéreo); setores bio entre 0,1% e 6%.
"""
import numpy as np
import xlrd

from . import tru, leontief

D12 = None  # resolvido sob demanda a partir de tru.DADOS
N12 = 12
_PUBLICOS = {"8400", "8591", "8691"}  # adm. pública, educação pública, saúde pública


def _d12():
    return tru.DADOS.parent / "tru_n12"


# ---------------- nível 12 ----------------
def n12_matriz(ano, tab, aba):
    """Bloco 12 produtos x 12 atividades (linhas 5-16, colunas 2-13) da TRU nível 12."""
    ws = xlrd.open_workbook(str(_d12() / f"12_tab{tab}_{ano}.xls")).sheet_by_name(aba)
    cods = [str(ws.cell_value(r, 0)).strip()[:2] for r in range(5, 5 + N12)]
    assert cods == [f"{i:02d}" for i in range(1, 13)], f"códigos nível 12 {ano}/{aba}: {cods}"
    return np.array([[float(ws.cell_value(r, c) or 0) for c in range(2, 2 + N12)]
                     for r in range(5, 5 + N12)])


def n12_agregados(ano):
    prod = n12_matriz(ano, 1, "producao")   # produto x atividade, preços básicos
    ci = n12_matriz(ano, 2, "CI")           # produto x atividade, preços de consumidor
    return {"vbp_ativ": prod.sum(0), "ci_col": ci.sum(0), "ci_lin": ci.sum(1)}


def bloco12(cod68):
    """Bloco do nível 12 de cada atividade do nível 68 (por faixa de divisão CNAE)."""
    if cod68 in _PUBLICOS:
        return 12
    p = int(cod68[:2])
    for bloco, faixas in [(1, [(1, 3)]), (2, [(5, 9)]), (3, [(10, 33)]), (4, [(35, 39)]),
                          (5, [(41, 43)]), (6, [(45, 47)]), (7, [(49, 53)]),
                          (8, [(58, 63)]), (9, [(64, 66)]), (10, [(68, 68)]),
                          (11, [(55, 56), (69, 82), (85, 88), (90, 97)])]:
        if any(a <= p <= b for a, b in faixas):
            return bloco
    raise ValueError(f"código 68 sem bloco nível 12: {cod68}")


def verificar_mapeamento(m, ano):
    """Confere o mapeamento 68->12 contra o VBP publicado no nível 12 (preços básicos)."""
    blocos = np.array([bloco12(c.strip()) for c in m["atividades"]])
    vbp68 = np.array([m["g"][blocos == b].sum() for b in range(1, 13)])
    desv = np.abs(vbp68 / n12_agregados(ano)["vbp_ativ"] - 1).max()
    assert desv < 0.005, f"mapeamento 68->12 não confere com o nível 12 de {ano}: {desv:.4f}"
    return blocos


# ---------------- GRAS ----------------
def _fator(P, N, s, alvo):
    p = P @ s
    n = N @ (1.0 / s)
    f = np.ones_like(alvo)
    pos = p > 0
    f[pos] = (alvo[pos] + np.sqrt(alvo[pos] ** 2 + 4 * p[pos] * n[pos])) / (2 * p[pos])
    lim = (~pos) & (n > 0)
    assert (alvo[lim] < 0).all(), "linha/coluna só com negativos exige margem negativa"
    f[lim] = -n[lim] / alvo[lim]
    return f


def gras(A0, u, v, eps=1e-9, max_iter=10000):
    """Balanceia A0 (com negativos) às margens u (linhas) e v (colunas)."""
    assert abs(u.sum() - v.sum()) < 1e-6 * abs(u).sum(), "margens inconsistentes"
    P = np.where(A0 > 0, A0, 0.0)
    N = np.where(A0 < 0, -A0, 0.0)
    r = np.ones(A0.shape[0])
    with np.errstate(all="ignore"):
        for _ in range(max_iter):
            s = _fator(P.T, N.T, r, v)
            r_novo = _fator(P, N, s, u)
            if np.abs(r_novo - r).max() < eps:
                r = r_novo
                break
            r = r_novo
    X = r[:, None] * P * s[None, :] - (1 / r)[:, None] * N * (1 / s)[None, :]
    assert max(np.abs(X.sum(1) - u).max(), np.abs(X.sum(0) - v).max()) < 1e-4 * abs(u).max(), \
        "GRAS não convergiu"
    return X


# ---------------- estimação de ano sem TRU 68 ----------------
def estimar(ano_alvo, ano_base):
    """Projeta Z, A, L e g do ano_alvo a partir do ano_base via GRAS + nível 12."""
    mb = leontief.matrizes(tru.carregar(ano_base))
    blocos = verificar_mapeamento(mb, ano_base)
    agb, aga = n12_agregados(ano_base), n12_agregados(ano_alvo)
    with np.errstate(invalid="ignore", divide="ignore"):
        f_lin = aga["ci_lin"] / agb["ci_lin"]
        f_col = aga["ci_col"] / agb["ci_col"]
        f_g = aga["vbp_ativ"] / agb["vbp_ativ"]
    f_lin = np.where(np.isfinite(f_lin), f_lin, f_g)
    f_col = np.where(np.isfinite(f_col), f_col, f_g)
    u = mb["Z"].sum(1) * f_lin[blocos - 1]
    v = mb["Z"].sum(0) * f_col[blocos - 1]
    fator = v.sum() / u.sum()
    u = u * fator
    g = mb["g"] * f_g[blocos - 1]
    Z = gras(mb["Z"], u, v)
    A = Z / g[None, :]
    assert (A.sum(0) < 1).all(), "coluna de A >= 1 na projeção GRAS"
    L = np.linalg.inv(np.eye(len(A)) - A)
    return {"Z": Z, "A": A, "L": L, "g": g, "atividades": mb["atividades"],
            "ano_base": ano_base, "fator_fechamento": fator,
            # aproximação declarada: VAB do ano-base escalado pelo crescimento
            # do VBP do bloco nível 12 (a TRU 68 do alvo não existe)
            "VAB": mb["VAB"] * f_g[blocos - 1]}
