"""Testes do mipcore.sda — Análise de Decomposição Estrutural (SDA).

Trava as propriedades da decomposição da variação da produção entre anos consecutivos
em mudança tecnológica (ΔL) e de demanda final (Δf), pela média das formas polares
(MILLER & BLAIR, 2009, §13.1, eq. 13.7, p. 595). A eficiência da média das duas formas
polares como aproximação da média de todas as decomposições é de DIETZENBACHER & LOS
(1998, Economic Systems Research, v. 10, n. 4, p. 307-324, doi:10.1080/09535319800000023)
— referência acrescida por esta suíte; o docstring de sda.py cita apenas Miller & Blair:

    Δx = ½·(ΔL)·(f0 + f1) + ½·(L0 + L1)·(Δf)

Invariantes verificadas (dado nacional TRU versionado; rodam no CI limpo):

  (1) ADITIVIDADE — tec + dem reconstitui Δx à precisão de máquina. Guard de regressão;
      é algebricamente forçada quando x = L·f, logo depende de (3) valer.
  (2) FORMAS POLARES — recomputa tec/dem a partir das primitivas (L0,L1,f0,f1) pela via
      das DUAS formas polares separadas (½(ΔL·f0)+½(ΔL·f1) e ½(L1·Δf)+½(L0·Δf)) e exige
      que cada forma polar isolada reconstitua Δx e que a média bata com o código. Pega
      erro de transcrição no assembler (sinal trocado, L0↔L1, f0 repetido).
  (3) CONSISTÊNCIA LEONTIEF — f é o resíduo g − Z·i, de modo que L·f = g é exato; sem isso
      a aditividade de (1) não seria à precisão de máquina.
  (4) RECONCILIAÇÃO POR CATEGORIA — guard forte e independente do código de decompor_par:
      decompor_par_categorias monta a demanda final por CAMINHO DISTINTO (híbrido de preços
      básicos + market-share D + reescala), abre o efeito-demanda nas 6 categorias da TRU e,
      mesmo assim, dem_k somado nas categorias tem de bater com o dem agregado (resíduo
      observado ~1e-10, tolerância 1e-6) e tec tem de ser idêntico (resíduo 0.0). É o
      análogo, aqui, do teste de propriedade externa da auditoria GHS.

Não reproduz números publicados de SDA (não há série de referência canônica embutida);
a validação é estrutural, sobre a TRU nacional nível 68 do IBGE.

Rodar:  source ~/.venvs/fgv-mip/bin/activate && pytest MIP/tests/test_sda.py -v
"""
import numpy as np
import pytest

import mipcore as m
from mipcore import sda, tru

ANO = 2012           # par 2011→2012: TRU nacional versionada, presente no CI
_TOL_ABS = 1e-6      # magnitudes ~1e4–1e5; resíduos observados ~1e-10 (folga de ~4 ordens)


@pytest.fixture(scope="module")
def par():
    """Decomposição do par ANO-1 → ANO e as primitivas do sistema, uma vez por módulo."""
    r = sda.decompor_par(ANO)
    A0, L0, f0, g0 = sda._sistema(tru.carregar(ANO - 1))
    A1, L1, f1, g1 = sda._sistema(sda.carregar_ano_anterior(ANO))
    return r, (L0, f0, g0), (L1, f1, g1)


def test_modulo_registrado():
    assert hasattr(m, "sda")


def test_sda_aditividade_exata(par):
    """(1) tec + dem = Δx à precisão de máquina (resíduo relativo à escala de Δx)."""
    r = par[0]
    escala = np.abs(r["dx"]).max()
    assert r["residuo"] / escala < 1e-9
    assert np.abs(r["dx"] - (r["tec"] + r["dem"])).max() < _TOL_ABS


def test_sda_formas_polares_independentes(par):
    """(2) Reconstrói tec/dem pelas duas formas polares (via independente do assembler)."""
    r, (L0, f0, _), (L1, f1, _) = par
    dL, df = L1 - L0, f1 - f0
    # forma polar 1 (L primeiro) e forma polar 2 (f primeiro): cada uma é exata em Δx
    tec_p1, dem_p1 = dL @ f0, L1 @ df
    tec_p2, dem_p2 = dL @ f1, L0 @ df
    assert np.abs((tec_p1 + dem_p1) - r["dx"]).max() < _TOL_ABS
    assert np.abs((tec_p2 + dem_p2) - r["dx"]).max() < _TOL_ABS
    # a média das formas polares é a decomposição do código
    assert np.abs(0.5 * (tec_p1 + tec_p2) - r["tec"]).max() < _TOL_ABS
    assert np.abs(0.5 * (dem_p1 + dem_p2) - r["dem"]).max() < _TOL_ABS


def test_sda_consistencia_leontief(par):
    """(3) f é o resíduo que torna L·f = g exato; x0 devolvido = g do ano-base."""
    r, (L0, f0, g0), _ = par
    assert np.abs(L0 @ f0 - g0).max() < 1e-6
    assert np.array_equal(r["x0"], g0)


def test_sda_categorias_reconciliam(par):
    """(4) decompor_par_categorias (caminho independente) soma de volta ao agregado."""
    r = par[0]
    rc = sda.decompor_par_categorias(ANO)
    assert rc["dem_k"].shape[1] == 6
    assert list(rc["categorias"]) == ["exportacao", "governo", "isflsf",
                                      "familias", "fbcf", "estoque"]
    # soma das 6 categorias = efeito-demanda agregado; tecnologia idêntica
    assert np.abs(rc["dem_k"].sum(1) - r["dem"]).max() < _TOL_ABS
    assert np.abs(rc["tec"] - r["tec"]).max() < _TOL_ABS
    # e a própria decomposição por categoria é aditiva
    escala = np.abs(rc["dx"]).max()
    assert rc["residuo"] / escala < 1e-9


def test_sda_serie_encadeia():
    """serie() devolve um par por ano, na ordem, todos com resíduo desprezível."""
    anos = range(2012, 2015)
    s = sda.serie(anos)
    assert [p["ano"] for p in s] == list(anos)
    escalas = [np.abs(p["dx"]).max() for p in s]
    assert all(p["residuo"] / e < 1e-9 for p, e in zip(s, escalas))
