"""Suíte de testes do mipcore (pytest).

Trava a correção do pacote: identidades contábeis das TRU, controles de Leontief, método
híbrido de preços básicos, GRAS (com o exemplo numérico de Lenzen et al. 2007) e o sistema
inter-regional IIOAS, incluindo validações EXTERNAS contra resultados publicados (ranking de
autossuficiência por UF do artigo do IIOAS; preservação da estimativa perfeita no GRAS).

Rodar:  source ~/.venvs/fgv-mip/bin/activate && pytest MIP/tests/ -v
(ou:    ~/.venvs/fgv-mip/bin/python -m pytest MIP/tests/ -v)
"""
import warnings

import numpy as np
import pytest

import mipcore as m

ANO_NAC = 2019   # ano com TRU nível 68 para os testes nacionais


# ---------------- pacote ----------------
def test_versao_e_modulos():
    assert m.__version__ >= "1.3.0"
    for mod in ("tru", "precos_basicos", "leontief", "multiplicadores", "sda", "cnt",
                "gras", "regional"):
        assert hasattr(m, mod), f"módulo ausente: {mod}"


# ---------------- TRU / Leontief ----------------
def test_tru_identidades():
    ids = m.tru.checar_identidades(ANO_NAC)
    assert ids["CI+DF=oferta_pc"] < 1e-3
    assert ids["g=CI_col+VAB(max)"] < 1e-3


def test_leontief_controles():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d = m.tru.carregar(ANO_NAC)
        chk = m.leontief.checar(d)
    assert chk["colunas_A>=1"] == 0, "coluna de A com soma >= 1"
    assert chk["max|Ly-g|"] < 1e-6, "L·f não reproduz g"


def test_precos_basicos_hibrido():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d = m.tru.carregar(ANO_NAC)
        U = m.precos_basicos.uso_basico_hibrido(d)
    assert U.ndim == 2 and U.shape[0] == 128, f"forma inesperada: {U.shape}"
    assert not np.isnan(U).any() and not np.isinf(U).any()


def test_multiplicadores():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        d = m.tru.carregar(ANO_NAC)
        mat = m.leontief.matrizes(d)
    mp = m.multiplicadores.producao_tipo1(mat["L"])
    assert (mp >= 1 - 1e-9).all(), "multiplicador de produção tipo I < 1"
    assert mp.max() < 6, "multiplicador implausivelmente alto"
    tras, frente = m.multiplicadores.rasmussen_hirschman(mat["L"])
    assert tras.shape == frente.shape == (len(mat["atividades"]),)


# ---------------- GRAS ----------------
def test_gras_exemplo_lenzen():
    """Lenzen, Wood & Gallego (2007), eq. (2), p. 463: estimativa que já satisfaz as
    margens deve ser devolvida intacta pelo GRAS correto."""
    A = np.array([[-1.0, 2.0], [2.0, 3.0]])
    X = m.gras.gras(A, np.array([1.0, 5.0]), np.array([1.0, 5.0]))
    assert np.abs(X - A).max() < 1e-6


def test_gras_estimar_2022():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        est = m.gras.estimar(2022, 2021)
        base = m.leontief.matrizes(m.tru.carregar(2021))
    assert (est["A"].sum(0) < 1).all(), "coluna de A >= 1 na projeção GRAS"
    r = np.corrcoef(est["A"].ravel(), base["A"].ravel())[0, 1]
    assert r > 0.99, f"continuidade r(A) baixa: {r:.4f}"


# ---------------- regional (IIOAS) ----------------
@pytest.fixture(scope="module")
def sys_reg():
    return m.regional.carregar(2011)


def test_regional_estrutura(sys_reg):
    assert sys_reg["A"].shape == (m.regional.N, m.regional.N)
    assert len(sys_reg["uf"]) == 27 and len(sys_reg["setores"]) == 68
    I = np.eye(m.regional.N)
    with np.errstate(all="ignore"):
        resid = np.abs((I - sys_reg["A"]) @ sys_reg["L"] - I).max()
    assert resid < 1e-6, f"L não é inv(I-A): {resid:.2e}"


def test_regional_autossuficiencia_vs_artigo(sys_reg):
    """Validação externa: HADDAD; GONÇALVES JUNIOR; NASCIMENTO (2017) reportam SP e RJ como
    os mais autossuficientes e RR e TO entre os menos. O ranking deve reproduzir isso."""
    aut = m.regional.autossuficiencia_uf(sys_reg)
    ranking = [uf for uf, _ in sorted(aut.items(), key=lambda kv: kv[1], reverse=True)]
    assert ranking.index("SP") < 3, "SP deveria estar no topo da autossuficiência"
    assert ranking.index("RJ") < 6, "RJ deveria estar entre os mais autossuficientes"
    assert ranking.index("RR") >= 24, "RR deveria estar entre os menos autossuficientes"
    assert ranking.index("TO") >= 22, "TO deveria estar entre os menos autossuficientes"


def test_regional_indices_e_blocos(sys_reg):
    assert m.regional.idx(sys_reg, "SP", 1) == 19 * 68          # SP é R20 (índice 19), setor 1
    bl = m.regional.bloco(sys_reg["L"], 19, 19)                 # SP -> SP
    assert bl.shape == (68, 68) and np.diag(bl).mean() > 1.0


def test_regional_extracao(sys_reg):
    sp = m.regional.extracao_regiao(sys_reg, "SP")["impacto_relativo"]
    rr = m.regional.extracao_regiao(sys_reg, "RR")["impacto_relativo"]
    assert sp > rr, "extração de SP deveria impactar mais que a de RR"


# ---------------- regional 2019 (A derivada dos fluxos) ----------------
@pytest.fixture(scope="module")
def sys_reg19():
    return m.regional.carregar(2019)


def test_regional_2019_estrutura(sys_reg19):
    assert sys_reg19["ano"] == 2019
    assert sys_reg19["A"].shape == (m.regional.N, m.regional.N)
    assert len(sys_reg19["uf"]) == 27 and len(sys_reg19["setores"]) == 68
    assert sys_reg19["A"].sum(0).max() < 1, "coluna de A com soma >= 1"
    I = np.eye(m.regional.N)
    with np.errstate(all="ignore"):
        resid = np.abs((I - sys_reg19["A"]) @ sys_reg19["L"] - I).max()
    assert resid < 1e-6, f"L não é inv(I-A): {resid:.2e}"


def test_regional_demanda_final(sys_reg, sys_reg19):
    """A demanda final reproduz o VBP (L·f = produção) e tem composição econômica plausível."""
    for s in (sys_reg, sys_reg19):
        df = m.regional.demanda_final(s)
        assert df["total"].shape == (m.regional.N,)
        with np.errstate(all="ignore"):
            x = s["L"] @ df["total"]
        # alguns (UF,setor) têm VBP=0 (setor sem produção na UF) -> produção nula, legítimo
        assert (x >= -1e-6).all() and np.isfinite(x).all(), "L·f com produção negativa/inf"
        assert x.sum() > df["total"].sum(), "produção bruta deveria exceder a demanda final"
    # 2019 traz as 5 categorias somando (quase) o total; famílias é a maior
    cat = m.regional.demanda_final(sys_reg19)["categorias"]
    assert cat is not None and len(cat) == 5
    assert max(cat, key=lambda k: cat[k].sum()) == "Famílias"
    assert m.regional.demanda_final(sys_reg)["categorias"] is None     # 2011: só total


def test_regional_extracao_usa_f_real(sys_reg19):
    """Sem f explícito, a extração usa a demanda final real (não o choque unitário)."""
    er = m.regional.extracao_regiao(sys_reg19, "SP")
    assert er["nota"] == "demanda final real"
    assert 0 < er["impacto_relativo"] < 1


def test_regional_2019_autossuficiencia(sys_reg19):
    """Em 2019, SP segue no topo e TO/AP no fundo da autossuficiência (estrutura consistente
    com 2011 e com o padrão do artigo, com a mobilidade esperada em 8 anos)."""
    aut = m.regional.autossuficiencia_uf(sys_reg19)
    ranking = [uf for uf, _ in sorted(aut.items(), key=lambda kv: kv[1], reverse=True)]
    assert ranking.index("SP") < 3, "SP deveria estar no topo em 2019"
    assert ranking.index("TO") >= 24, "TO deveria estar no fundo em 2019"
    assert ranking.index("AP") >= 24, "AP deveria estar no fundo em 2019"
