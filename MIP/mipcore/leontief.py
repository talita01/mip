"""
mipcore.leontief — Matrizes de insumo-produto a partir da TRU: market-share D, coeficientes técnicos
Bn, matriz atividade×atividade A = D·Bn, e a inversa de Leontief L = (I-A)^-1.

Modelo: tecnologia do setor (IBGE). Trabalha a preços básicos, uso nacional (mipcore.precos_basicos).
"""
import numpy as np
from . import precos_basicos


def matrizes(d, r_int=None):
    """Retorna dict com D, Bn, Z (atividade×atividade), A, L, e os vetores g, VAB, v (coef de VA)."""
    Un = precos_basicos.uso_nacional_basico(d, r_int)          # produto × atividade, nacional básico
    V, q, g, VAB = d["V_pa"], d["q"], d["g"], d["VA"]["VAB"]
    qs = np.where(q > 0, q, 1.0)
    D = np.nan_to_num((V / qs[:, None]).T)                     # market share: atividade × produto
    Z = D @ Un                                                # fluxo atividade × atividade (origem × destino)
    gd = np.where(g > 0, g, 1.0)
    A = Z / gd[None, :]                                        # coef técnicos atividade × atividade
    L = np.linalg.inv(np.eye(len(g)) - A)                     # inversa de Leontief
    Bn = np.nan_to_num(Un / gd[None, :])                      # coef técnicos produto × atividade
    return {"D": D, "Bn": Bn, "Z": Z, "A": A, "L": L,
            "g": g, "VAB": VAB, "v": VAB / gd, "atividades": d["atividades"]}


def inversa(A):
    return np.linalg.inv(np.eye(A.shape[0]) - A)


def demanda_final(d, r_int=None):
    """Demanda final por atividade (resíduo do balanço: g - vendas intermediárias)."""
    m = matrizes(d, r_int)
    return m["g"] - m["Z"].sum(1)


def checar(d, r_int=None):
    """Controles: A sem coluna≥1; x=L·y reproduz g; v'·L·y = ΣVAB."""
    m = matrizes(d, r_int); A, L, g, v = m["A"], m["L"], m["g"], m["v"]
    y = g - m["Z"].sum(1)
    return {
        "colunas_A>=1": int((A.sum(0) >= 1).sum()),
        "max_soma_coluna_A": float(A.sum(0).max()),
        "max|Ly-g|": float(np.abs(L @ y - g).max()),
        "v'Ly_vs_VAB": (float(v @ L @ y), float(m["VAB"].sum())),
    }
