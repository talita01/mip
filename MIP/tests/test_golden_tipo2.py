"""Golden regression dos multiplicadores Tipo II e geradores — TRU nacional 2019.

Estende o golden do núcleo (test_golden_multiplicadores.py cobre o Tipo I) ao modelo
FECHADO nas famílias e aos geradores de valor adicionado e renda. Congela três vetores
por atividade contra um artefato versionado, para pegar regressão silenciosa no
fechamento (fechar_familias) e nos geradores.

O fechamento Tipo II precisa de dois insumos que NÃO vêm de tru.carregar:
  w (renda por unidade de produção) = remunerações / produção. As remunerações estão na
    aba "VA" da 68_tab2 (componentes do valor adicionado); lidas aqui por _remuneracoes,
    com offset de coluna 1 (col 0 = rótulo, col 1 = 1ª atividade), alinhado contra o VAB.
  c (cesta de consumo das famílias) = coluna "familias" da demanda final, levada ao espaço
    de atividades pelo market-share D.
Nota de dado: remun ≤ VAB falha em alguns setores (salários acima do VA por subsídios),
característica da TRU, não erro de leitura. O fechamento é estável (rho ~0,71, igual ao
verificado pelo motor BEVAP).

O golden `tests/golden/multiplicadores_tipo2_2019.npz` guarda:
  - tipo2         : multiplicador de produção Tipo II por atividade (producao_tipo2);
  - gerador_va    : gerador (direto+indireto) de valor adicionado (coef VAB/g);
  - gerador_renda : gerador de renda/remunerações (coef remun/g);
  - atividades    : rótulos dos 68 setores; rho: raio espectral do fechamento.

Contratos (iguais ao golden do Tipo I):
  (A) INTEGRIDADE — SHA-256 do .npz confere com o manifesto .sha256.json.
  (B) REPRODUÇÃO  — recomputa e compara por np.allclose (rtol 1e-9), robusto a numpy
      2.4.6 (job faixas) / 2.5.1 (job lock); não byte-exato de propósito.

Gerado com numpy 2.4.6 / mipcore 1.9.0. Regenerar após mudança INTENCIONAL de método.

Rodar:  source ~/.venvs/fgv-mip/bin/activate && pytest MIP/tests/test_golden_tipo2.py -v
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
import xlrd

from mipcore import tru, leontief, multiplicadores as mult

_GOLDEN_DIR = Path(__file__).parent / "golden"
_NPZ = _GOLDEN_DIR / "multiplicadores_tipo2_2019.npz"
_MANIFESTO = _GOLDEN_DIR / "multiplicadores_tipo2_2019.sha256.json"
_ANO = 2019
_RTOL = 1e-9


def _remuneracoes(ano):
    """Remunerações por atividade (68,) da aba VA da 68_tab2; offset de coluna 1."""
    ws = xlrd.open_workbook(tru.DADOS / f"68_tab2_{ano}.xls").sheet_by_name("VA")
    rem_row = next(r for r in range(ws.nrows)
                   if str(ws.cell_value(r, 0)).strip() == "Remunerações")
    return np.array([ws.cell_value(rem_row, c) for c in range(1, 1 + tru.N_ATIV)], float)


@pytest.fixture(scope="module")
def golden():
    return np.load(_NPZ, allow_pickle=True)


@pytest.fixture(scope="module")
def computado():
    d = tru.carregar(_ANO)
    m = leontief.matrizes(d)
    g = m["g"]
    gd = np.where(g > 0, g, 1.0)
    remun = _remuneracoes(_ANO)
    DF = np.asarray(d["DF"])
    fam = d["demanda_cols"].index("familias")
    cesta = m["D"] @ DF[:, fam]
    fech = mult.fechar_familias(m["A"], remun / gd, cesta, alpha=1.0)
    return {
        "tipo2": mult.producao_tipo2(fech),
        "gerador_va": mult.gerador(m["VAB"] / gd, m["L"]),
        "gerador_renda": mult.gerador(remun / gd, m["L"]),
        "atividades": np.array(d["atividades"]),
        "rho": fech["rho"],
        "tipo1": m["L"].sum(0),
    }


def test_golden_tipo2_integridade():
    """(A) o .npz versionado confere com o SHA-256 do manifesto."""
    manifesto = json.loads(_MANIFESTO.read_text(encoding="utf-8"))
    sha = hashlib.sha256(_NPZ.read_bytes()).hexdigest()
    assert sha == manifesto["sha256_arquivo"], (
        "golden .npz diverge do checksum — corrompido, trocado, ou regenerado sem "
        "atualizar o manifesto")
    assert manifesto["ano"] == _ANO and manifesto["n_atividades"] == 68


def test_golden_tipo2_reproduz(golden, computado):
    """(B) multiplicador Tipo II recomputado reproduz o golden (tolerância)."""
    assert computado["tipo2"].shape == (68,)
    assert list(computado["atividades"]) == list(golden["atividades"])
    assert np.allclose(computado["tipo2"], golden["tipo2"], rtol=_RTOL, atol=0)


def test_golden_geradores_reproduzem(golden, computado):
    """(B) geradores de VA e renda reproduzem o golden."""
    assert np.allclose(computado["gerador_va"], golden["gerador_va"], rtol=_RTOL, atol=0)
    assert np.allclose(computado["gerador_renda"], golden["gerador_renda"], rtol=_RTOL, atol=0)


def test_golden_tipo2_propriedades(golden, computado):
    """Sanidade econômica: Tipo II ≥ Tipo I (efeito-renda induzido é não-negativo);
    fechamento estável (rho<1); geradores em [0,1] (fração da produção que é VA/renda)."""
    assert (golden["tipo2"] >= computado["tipo1"] - 1e-9).all()
    assert 0 < float(golden["rho"]) < 1
    assert (golden["gerador_va"] >= -1e-9).all() and (golden["gerador_va"] <= 1 + 1e-9).all()
    assert (golden["gerador_renda"] >= -1e-9).all() and (golden["gerador_renda"] <= 1 + 1e-9).all()
