"""Testes do mipcore.cadeia — extração de cadeia de valor (Harthoorn 1989).

Trava as propriedades do método: aditividade dos efeitos, telescopagem (a cadeia que
cobre toda a economia reproduz a inversa de Leontief), limite (produção da cadeia <=
produção total) e a pegada de conta-satélite (eq. 8). Validação estrutural; a reprodução
dos números publicados de Tetere e Peerlings (2024) exige as tabelas IO bálticas, ausentes.

Rodar:  source ~/.venvs/fgv-mip/bin/activate && pytest MIP/tests/test_cadeia.py -v
"""
import numpy as np
import pytest

import mipcore as m

# Economia sintética produtiva (somas de coluna de A < 1).
A = np.array([[0.20, 0.10, 0.00],
              [0.30, 0.20, 0.10],
              [0.10, 0.20, 0.30]])
F = np.array([100.0, 50.0, 80.0])


def test_modulo_registrado():
    assert hasattr(m, "cadeia")


def test_aditividade():
    r = m.cadeia.extracao_cadeia(A, interesse=[0], complementar=[1])
    assert np.abs(r["ET"] - (r["EF1"] + r["EF2"] + r["EF3"] + r["EF4"])).max() < 1e-12


def test_telescopagem_cadeia_cobre_tudo():
    # interesse uniao complementar = todos os setores -> ET deve reproduzir L
    r = m.cadeia.extracao_cadeia(A, interesse=[0], complementar=[1, 2])
    assert np.abs(r["ET"] - r["L"]).max() < 1e-10


def test_producao_cadeia_nao_excede_total():
    r = m.cadeia.extracao_cadeia(A, interesse=[0], complementar=[1])  # residual = {2}
    y = r["ET"] @ F            # produção da cadeia por setor
    x = r["L"] @ F             # produção total por setor
    assert (y >= -1e-9).all()
    assert (y <= x + 1e-9).all()


def test_pegada_cobre_tudo_reproduz_total():
    # coef de VA = 1 - soma da coluna de A; cadeia = toda a economia -> pegada = VA total
    coef = 1.0 - A.sum(0)
    r = m.cadeia.extracao_cadeia(A, interesse=[0], complementar=[1, 2])
    va_total = float(coef @ (r["L"] @ F))
    va_cadeia = float(m.cadeia.pegada(r["ET"], F, coef).sum())
    assert abs(va_cadeia - va_total) < 1e-7


def test_interesse_complementar_disjuntos():
    with pytest.raises(ValueError):
        m.cadeia.extracao_cadeia(A, interesse=[0, 1], complementar=[1])
