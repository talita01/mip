"""
mipcore.multiplicadores — Indicadores de insumo-produto: multiplicadores de produção e geradores
(renda/emprego/VA), encadeamentos de Rasmussen-Hirschman e ligações puras GHS.

Referência: Miller & Blair (2009); Guilhoto & Sesso Filho (2005). L = inversa de Leontief.
"""
import numpy as np


def producao_tipo1(L):
    """Multiplicador de produção tipo I: soma de coluna da inversa de Leontief."""
    return L.sum(0)


def gerador(coef, L):
    """Gerador (direto+indireto) de uma variável com coeficientes 'coef' (por unidade de produção):
    G_j = Σ_i coef_i · L_ij. Use coef = VA/g, emprego/g, renda/g, etc."""
    return coef @ L


def multiplicador(coef, L):
    """Multiplicador (gerador / efeito direto). MV_j = G_j / coef_j."""
    G = gerador(coef, L)
    return np.divide(G, np.where(coef != 0, coef, np.nan))


def rasmussen_hirschman(L):
    """Índices de ligação. Retorna (para_tras, para_frente); >1 indica setor-chave."""
    n = L.shape[0]; Lstar = L.mean()
    para_tras = (L.sum(0) / n) / Lstar      # poder de dispersão (coluna)
    para_frente = (L.sum(1) / n) / Lstar    # sensibilidade da dispersão (linha)
    return para_tras, para_frente


def ligacoes_puras_ghs(A, Y, j):
    """Ligações puras GHS do setor j (Guilhoto-Sonis-Hewings). Retorna dict PBL, PFL, PTL.
    A = coef técnicos atividade×atividade; Y = demanda final por atividade; j = índice do setor."""
    n = A.shape[0]
    r = [k for k in range(n) if k != j]
    Ajj = A[np.ix_([j], [j])]; Arr = A[np.ix_(r, r)]
    Ajr = A[np.ix_([j], r)]; Arj = A[np.ix_(r, [j])]
    Dj = np.linalg.inv(np.eye(1) - Ajj)
    Dr = np.linalg.inv(np.eye(n - 1) - Arr)
    Yj = np.array([[Y[j]]]); Yr = np.array(Y)[r].reshape(-1, 1)
    PBL = float((Dr @ Arj @ Yj).sum())        # ligação pura para trás
    PFL = float((Dj @ Ajr @ Dr @ Yr).sum())   # ligação pura para frente
    return {"PBL": PBL, "PFL": PFL, "PTL": PBL + PFL}


def ghs_todos(A, Y):
    """Ligações puras GHS para todos os setores, normalizadas pela média (PTLN)."""
    res = [ligacoes_puras_ghs(A, Y, j) for j in range(A.shape[0])]
    ptl = np.array([r["PTL"] for r in res]); m = ptl.mean()
    return {"PTL": ptl, "PTLN": ptl / m if m else ptl}
