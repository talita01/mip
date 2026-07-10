"""Testes do mipcore.cnt — Contas Nacionais Trimestrais do IBGE (SIDRA).

cnt.carregar é um leitor de API (tabelas 1846/1620 do SIDRA, classificação c11255).
Testar contra a rede viva deixaria o CI intermitente e dependente do IBGE; aqui o
urlopen é substituído por uma FIXTURE que reproduz o formato real da resposta SIDRA
(capturado da API em 2026-07-10: header dados[0] + linhas com chaves D3C/D4C/V).

Propriedades travadas (todas offline, rodam no CI limpo):
  (1) PARSING — o dict de saída mapeia (trimestre, setor) -> float exatamente como a
      fixture; a lista de trimestres vem ordenada e sem duplicatas.
  (2) FILTRAGEM DE AUSENTES — linhas com V em {"...", "..", "-", None} são descartadas,
      e um trimestre que só tenha valores ausentes NÃO entra na lista de trimestres.
  (3) CONSTRUÇÃO DA URL — a URL montada carrega tabela, variável e códigos certos, e o
      sufixo do filtro `d/` muda com a tabela (1846 -> "0" decimais; 1620 -> "2"). Guard
      contra troca de sufixo, que devolveria valores na precisão errada.
  (4) DEFAULT DE CÓDIGOS — sem `codigos`, consulta os 12 setores de atividade (SETORES_12).

Rodar:  source ~/.venvs/fgv-mip/bin/activate && pytest MIP/tests/test_cnt.py -v
"""
import io
import json

import pytest

import mipcore as m
from mipcore import cnt

# Fixture no formato real do SIDRA (t/1846): header + 4 linhas de dado, incluindo um
# trimestre (202601) cujo único setor tem valor ausente "..." — para exercitar (2).
_HEADER = {"V": "Valor", "D3C": "Trimestre (Código)", "D3N": "Trimestre",
           "D4C": "Setores e subsetores (Código)", "D4N": "Setores e subsetores"}
_FIXTURE = [
    _HEADER,
    {"D3C": "202504", "D3N": "4º trimestre 2025", "D4C": "90687", "D4N": "Agropecuária", "V": "101548"},
    {"D3C": "202504", "D3N": "4º trimestre 2025", "D4C": "90693", "D4N": "Indústrias",   "V": "382391"},
    {"D3C": "202503", "D3N": "3º trimestre 2025", "D4C": "90687", "D4N": "Agropecuária", "V": "98000"},
    {"D3C": "202601", "D3N": "1º trimestre 2026", "D4C": "90687", "D4N": "Agropecuária", "V": "..."},
]


@pytest.fixture
def mock_sidra(monkeypatch):
    """Substitui urlopen por um retorno de fixture; grava a URL solicitada em capturado."""
    capturado = {}

    def fake_urlopen(url, timeout=None):
        capturado["url"] = url
        return io.BytesIO(json.dumps(_FIXTURE).encode("utf-8"))

    monkeypatch.setattr(cnt.urllib.request, "urlopen", fake_urlopen)
    return capturado


def test_modulo_registrado():
    assert hasattr(m, "cnt")


def test_cnt_parsing(mock_sidra):
    """(1) dict fiel à fixture; trimestres ordenados e únicos."""
    val, tris = cnt.carregar(codigos=["90687", "90693"])
    assert val[("202504", "90687")] == 101548.0
    assert val[("202504", "90693")] == 382391.0
    assert val[("202503", "90687")] == 98000.0
    assert isinstance(val[("202504", "90687")], float)
    # 202601 tem só valor ausente -> não aparece nem no dict nem nos trimestres
    assert ("202601", "90687") not in val
    assert tris == ["202503", "202504"]
    assert len(tris) == len(set(tris))


def test_cnt_filtra_ausentes(mock_sidra):
    """(2) nenhuma chave com valor-sentinela sobrevive; trimestre só-ausente é omitido."""
    val, tris = cnt.carregar(codigos=["90687", "90693"])
    assert "202601" not in tris
    assert all(v not in ("...", "..", "-", None) for v in val.values())


def test_cnt_url_muda_sufixo_por_tabela(mock_sidra):
    """(3) a tabela seleciona o sufixo de decimais em d/v...: 1846->0, 1620->2."""
    cnt.carregar(codigos=["90687"], tabela=1846, variavel=585)
    u1846 = mock_sidra["url"]
    assert "/t/1846/" in u1846 and "/v/585/" in u1846 and "c11255/90687/" in u1846
    assert u1846.rstrip().endswith("v585%200")      # 1846 -> "0"

    cnt.carregar(codigos=["90687"], tabela=1620, variavel=583)
    u1620 = mock_sidra["url"]
    assert "/t/1620/" in u1620 and "/v/583/" in u1620
    assert u1620.rstrip().endswith("v583%202")      # 1620 -> "2"


def test_cnt_default_12_setores(mock_sidra):
    """(4) sem codigos, consulta os 12 setores de atividade (SETORES_12)."""
    assert len(cnt.SETORES_12) == 12
    cnt.carregar()
    url = mock_sidra["url"]
    for cod in cnt.SETORES_12:
        assert cod in url
    # agregados (VA, impostos, PIB) NÃO entram no default
    assert cnt.SETORES["PIB_mercado"] not in url.split("c11255/")[1]
