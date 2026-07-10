"""Golden regression dos multiplicadores de produção — TRU nacional 68 setores, 2019.

Congela a saída numérica completa do núcleo (não só invariantes de forma) contra um
artefato de referência versionado, para pegar regressão silenciosa: uma mudança que
preserve as identidades contábeis mas altere os valores dos multiplicadores.

O golden `tests/golden/multiplicadores_tipo1_2019.npz` guarda, para o ano 2019
(TRU 68 versionada, presente no CI):
  - tipo1          : multiplicador de produção Tipo I por atividade (soma de coluna de L);
  - rh_para_tras   : índice de ligação para trás (Rasmussen-Hirschman);
  - rh_para_frente : índice de ligação para frente;
  - atividades     : rótulos dos 68 setores.

Dois níveis de verificação, com contratos distintos:
  (A) INTEGRIDADE — SHA-256 do arquivo .npz confere com o registrado no manifesto
      .sha256.json. Garante que o golden versionado não foi corrompido nem trocado.
  (B) REPRODUÇÃO — recomputa tipo1/R-H da TRU real e compara ao golden por np.allclose
      (rtol=1e-9). NÃO se usa igualdade byte-exata de propósito: entre numpy 2.4.6
      (job `faixas`/3.11) e 2.5.1 (job `lock`/3.13) os valores batem a ~1e-15, mas o
      SHA-256 dos arrays recomputados difere (BLAS). O checksum valida o arquivo; a
      igualdade da computação é por tolerância — robusta a versão, sensível a método.

Gerado com numpy 2.4.6 / mipcore 1.9.0 (ver manifesto). Regenerar após mudança
INTENCIONAL de método: rodar o bloco de geração em tests/golden/ e atualizar o .json.

Rodar:  source ~/.venvs/fgv-mip/bin/activate && pytest MIP/tests/test_golden_multiplicadores.py -v
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from mipcore import tru, leontief, multiplicadores as mult

_GOLDEN_DIR = Path(__file__).parent / "golden"
_RTOL = 1e-9
# Dois anos de referência: 2015 (ano-base da MIP) e 2019 (ano da matriz interestadual).
# Congelar mais de um ano guarda regressão no CARREGAMENTO por ano — um bug que afete só
# a leitura de um ano específico passaria despercebido com um único ano congelado.
_ANOS = [2015, 2019]


def _npz(ano):
    return _GOLDEN_DIR / f"multiplicadores_tipo1_{ano}.npz"


def _manifesto(ano):
    return _GOLDEN_DIR / f"multiplicadores_tipo1_{ano}.sha256.json"


def _computar(ano):
    d = tru.carregar(ano)
    L = leontief.matrizes(d)["L"]
    bt, bf = mult.rasmussen_hirschman(L)
    return {"tipo1": mult.producao_tipo1(L), "rh_para_tras": bt, "rh_para_frente": bf,
            "atividades": np.array(d["atividades"])}


@pytest.mark.parametrize("ano", _ANOS)
def test_golden_integridade(ano):
    """(A) o .npz versionado confere com o SHA-256 do manifesto."""
    manifesto = json.loads(_manifesto(ano).read_text(encoding="utf-8"))
    sha = hashlib.sha256(_npz(ano).read_bytes()).hexdigest()
    assert sha == manifesto["sha256_arquivo"], (
        f"golden {ano} .npz diverge do checksum registrado — arquivo corrompido, trocado, "
        "ou regenerado sem atualizar o manifesto")
    assert manifesto["ano"] == ano
    assert manifesto["n_atividades"] == 68


@pytest.mark.parametrize("ano", _ANOS)
def test_golden_reproduz_tipo1(ano):
    """(B) o multiplicador Tipo I recomputado reproduz o golden (tolerância, não bytes)."""
    golden = np.load(_npz(ano), allow_pickle=True)
    computado = _computar(ano)
    assert computado["tipo1"].shape == (68,)
    assert list(computado["atividades"]) == list(golden["atividades"])
    assert np.allclose(computado["tipo1"], golden["tipo1"], rtol=_RTOL, atol=0)


@pytest.mark.parametrize("ano", _ANOS)
def test_golden_reproduz_rasmussen_hirschman(ano):
    """(B) os índices de ligação R-H (trás e frente) reproduzem o golden."""
    golden = np.load(_npz(ano), allow_pickle=True)
    computado = _computar(ano)
    assert np.allclose(computado["rh_para_tras"], golden["rh_para_tras"], rtol=_RTOL, atol=0)
    assert np.allclose(computado["rh_para_frente"], golden["rh_para_frente"], rtol=_RTOL, atol=0)


@pytest.mark.parametrize("ano", _ANOS)
def test_golden_propriedades_economicas(ano):
    """Sanidade do próprio golden: Tipo I >= 1 (o setor produz ao menos a si);
    R-H para trás média ~1 por construção (normalizada pela média de L)."""
    golden = np.load(_npz(ano), allow_pickle=True)
    assert (golden["tipo1"] >= 1.0 - 1e-9).all()
    assert golden["tipo1"].max() < 10.0                      # nenhum multiplicador absurdo
    assert abs(golden["rh_para_tras"].mean() - 1.0) < 1e-6   # média dos índices = 1
