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


def fechar_familias(A, w, c, alpha=1.0):
    """Modelo fechado em relação às famílias → multiplicadores Tipo II (efeito-renda induzido).

    Endogeniza o consumo das famílias acrescentando a A uma linha de renda e uma coluna de
    consumo (MILLER; BLAIR, 2009, §2.5 e §6.2; fechamento padrão):
      A     — coeficientes técnicos n×n;
      w     — renda das famílias por unidade de produção (linha), ex.: remunerações/produção (n,);
      c     — cesta de consumo das famílias (coluna); normalizada aqui para somar 1 (n,);
      alpha — propensão a consumir (0..1; 1.0 = limite superior do efeito induzido).
    Retorna dict: Abar ((n+1)×(n+1)), Lbar = (I-Abar)⁻¹, rho (raio espectral; estável se <1), n.
    """
    A = np.asarray(A, float); n = A.shape[0]
    c = np.asarray(c, float); s = c.sum(); c = c / s if s else c
    Abar = np.zeros((n + 1, n + 1))
    Abar[:n, :n] = A
    Abar[:n, n] = alpha * c                      # consumo por unidade de renda
    Abar[n, :n] = np.asarray(w, float)           # renda por unidade de produção
    rho = float(np.abs(np.linalg.eigvals(Abar)).max())
    if rho >= 1.0:
        raise ValueError(f"fechamento instável: raio espectral {rho:.3f} >= 1")
    Lbar = np.linalg.inv(np.eye(n + 1) - Abar)
    return {"Abar": Abar, "Lbar": Lbar, "rho": rho, "n": n}


def producao_tipo2(fech):
    """Multiplicador de produção Tipo II por setor (soma de coluna do bloco setorial de Lbar).
    `fech` = retorno de fechar_familias. A razão Tipo II / Tipo I é o efeito-renda induzido."""
    n = fech["n"]
    return fech["Lbar"][:n, :n].sum(0)


def gerador_tipo2(fech, coef):
    """Gerador Tipo II (direto+indireto+induzido) de uma variável com coeficientes 'coef'
    (por unidade de produção, n,): G2_j = Σ_i coef_i · Lbar_ij, sobre o bloco setorial n×n da
    inversa aumentada do fechamento nas famílias. Estende `gerador` ao efeito-renda induzido;
    com coef unitário reproduz `producao_tipo2`. A parcela induzida é gerador_tipo2 − gerador."""
    n = fech["n"]
    return gerador(np.asarray(coef, float), fech["Lbar"][:n, :n])


def multiplicador_tipo2(fech, coef):
    """Multiplicador Tipo II de uma variável: gerador Tipo II / efeito direto (coef_j)."""
    coef = np.asarray(coef, float)
    return np.divide(gerador_tipo2(fech, coef), np.where(coef != 0, coef, np.nan))


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
    # Forma canônica GHS (GUILHOTO, 2011, eqs. 6.23-6.24; GUILHOTO et al., MIP-Nordeste,
    # 2010/2004, eqs. 109-110): PBL = Dr·Arj·Dj·Yj e PFL = Dj·Ajr·Dr·Yr, estruturalmente
    # simétricas. O fator Dj no PBL (antes ausente) é o multiplicador interno do próprio
    # setor j; sem ele o PBL subestima em 1/(1-Ajj). Ver auditoria 2026-07-08.
    PBL = float((Dr @ Arj @ Dj @ Yj).sum())   # ligação pura para trás
    PFL = float((Dj @ Ajr @ Dr @ Yr).sum())   # ligação pura para frente
    return {"PBL": PBL, "PFL": PFL, "PTL": PBL + PFL}


def ghs_todos(A, Y):
    """Ligações puras GHS para todos os setores, normalizadas pela média (PTLN)."""
    res = [ligacoes_puras_ghs(A, Y, j) for j in range(A.shape[0])]
    ptl = np.array([r["PTL"] for r in res]); m = ptl.mean()
    return {"PTL": ptl, "PTLN": ptl / m if m else ptl}
