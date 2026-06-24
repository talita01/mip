"""mipcore.cadeia — Cadeia de valor por extração de efeitos (Harthoorn 1989).

Isola a produção de uma cadeia (setor de interesse + setor complementar) numa matriz
insumo-produto, decompondo o efeito total em quatro parcelas aninhadas. Método de
Harthoorn (1989), aplicado por Tetere e Peerlings (2024, eq. 3-8) à bioeconomia florestal.
Fonte: 20_Recursos/referencias/tetereMeasuringForestbased2024 · método: extracao-cadeia-harthoorn.

Vetores de seleção (s) e residual (r) como interruptores 0/1:
  s0 = interesse;        r0 = complemento de interesse
  s1 = complementar;     r1 = complemento de (interesse uniao complementar)
Efeitos (S = diag(s), L = (I-A)^-1, Lr0 = (I - r0.A.r0)^-1, Lr1 = (I - r1.A.r1)^-1):
  EF1 = S0 . L                 producao direta+indireta do interesse           (eq. 3)
  EF2 = Lr0 . r0 . A . EF1     demais setores atribuiveis ao interesse          (eq. 4)
  EF3 = S1 . Lr0               complementar, liquido do interesse               (eq. 5)
  EF4 = Lr1 . r1 . A . EF3     demais setores atribuiveis ao complementar       (eq. 6)
  ET  = EF1 + EF2 + EF3 + EF4  a cadeia inteira                                 (eq. 7)
Propriedade: quando interesse uniao complementar cobre todos os setores, ET = L (a
decomposicao e completa). A producao da cadeia para a demanda final f e y = ET . f;
a pegada de qualquer conta (VA, emprego, emissoes) e diag(coef) . y, com coef = conta/producao (eq. 8).
"""
import numpy as np


def _sel(n, idx):
    v = np.zeros(n)
    v[list(idx)] = 1.0
    return v


def extracao_cadeia(A, interesse, complementar=None):
    """Extração de efeitos EF1-EF4 da cadeia (Harthoorn 1989).

    A           matriz de coeficientes técnicos n×n (atividade × atividade, A = Z/produção).
    interesse   índices do setor de interesse (s0).
    complementar índices do setor complementar (s1); vazio = só interesse (EF1+EF2).

    Retorna dict: EF1, EF2, EF3, EF4, ET (n×n), L, Lr0, Lr1, e os índices usados.
    """
    A = np.asarray(A, float)
    n = A.shape[0]
    I = np.eye(n)
    interesse = list(interesse)
    complementar = list(complementar or [])
    if set(interesse) & set(complementar):
        raise ValueError("interesse e complementar devem ser disjuntos")
    L = np.linalg.inv(I - A)
    s0 = _sel(n, interesse)
    s1 = _sel(n, complementar)
    r0 = 1.0 - s0                       # complemento do interesse
    r1 = 1.0 - s0 - s1                  # complemento de interesse uniao complementar
    S0, S1, R0, R1 = np.diag(s0), np.diag(s1), np.diag(r0), np.diag(r1)
    Lr0 = np.linalg.inv(I - R0 @ A @ R0)
    Lr1 = np.linalg.inv(I - R1 @ A @ R1)
    EF1 = S0 @ L
    EF2 = Lr0 @ R0 @ A @ EF1
    EF3 = S1 @ Lr0
    EF4 = Lr1 @ R1 @ A @ EF3
    ET = EF1 + EF2 + EF3 + EF4
    return dict(EF1=EF1, EF2=EF2, EF3=EF3, EF4=EF4, ET=ET, L=L, Lr0=Lr0, Lr1=Lr1,
                interesse=interesse, complementar=complementar)


def pegada(ET, f, coef):
    """Pegada de uma conta-satélite na cadeia (eq. 8): coef * (ET . f).

    ET    efeito total (n×n) de extracao_cadeia.
    f     vetor de demanda final (n).
    coef  coeficiente da conta por unidade de produção (n): VA/produção, emprego/produção,
          emissão/produção, água/produção, etc.

    Retorna o vetor de pegada por setor; .sum() é o total da cadeia.
    """
    return np.asarray(coef, float) * (np.asarray(ET, float) @ np.asarray(f, float))
