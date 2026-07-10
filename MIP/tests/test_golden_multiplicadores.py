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
_NPZ = _GOLDEN_DIR / "multiplicadores_tipo1_2019.npz"
_MANIFESTO = _GOLDEN_DIR / "multiplicadores_tipo1_2019.sha256.json"
_ANO = 2019
_RTOL = 1e-9


@pytest.fixture(scope="module")
def golden():
    return np.load(_NPZ, allow_pickle=True)


@pytest.fixture(scope="module")
def computado():
    d = tru.carregar(_ANO)
    L = leontief.matrizes(d)["L"]
    bt, bf = mult.rasmussen_hirschman(L)
    return {"tipo1": mult.producao_tipo1(L), "rh_para_tras": bt, "rh_para_frente": bf,
            "atividades": np.array(d["atividades"])}


def test_golden_integridade():
    """(A) o .npz versionado confere com o SHA-256 do manifesto."""
    manifesto = json.loads(_MANIFESTO.read_text(encoding="utf-8"))
    sha = hashlib.sha256(_NPZ.read_bytes()).hexdigest()
    assert sha == manifesto["sha256_arquivo"], (
        "golden .npz diverge do checksum registrado — arquivo corrompido, trocado, ou "
        "regenerado sem atualizar o manifesto")
    assert manifesto["ano"] == _ANO
    assert manifesto["n_atividades"] == 68


def test_golden_reproduz_tipo1(golden, computado):
    """(B) o multiplicador Tipo I recomputado reproduz o golden (tolerância, não bytes)."""
    assert computado["tipo1"].shape == (68,)
    assert list(computado["atividades"]) == list(golden["atividades"])
    assert np.allclose(computado["tipo1"], golden["tipo1"], rtol=_RTOL, atol=0)


def test_golden_reproduz_rasmussen_hirschman(golden, computado):
    """(B) os índices de ligação R-H (trás e frente) reproduzem o golden."""
    assert np.allclose(computado["rh_para_tras"], golden["rh_para_tras"], rtol=_RTOL, atol=0)
    assert np.allclose(computado["rh_para_frente"], golden["rh_para_frente"], rtol=_RTOL, atol=0)


def test_golden_propriedades_economicas(golden):
    """Sanidade do próprio golden: Tipo I >= 1 (o setor produz ao menos a si);
    R-H para trás média ~1 por construção (normalizada pela média de L)."""
    assert (golden["tipo1"] >= 1.0 - 1e-9).all()
    assert golden["tipo1"].max() < 10.0                      # nenhum multiplicador absurdo
    assert abs(golden["rh_para_tras"].mean() - 1.0) < 1e-6   # média dos índices = 1
