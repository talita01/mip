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


def test_ligacoes_puras_ghs_forma_fechada():
    """Ligações puras GHS (Guilhoto-Sonis-Hewings) contra a forma fechada de 2 setores.
    Para j=0: PBL = Y0*A10/(1-A11); PFL = A01/(1-A00) * 1/(1-A11) * Y1.
    Referência: Guilhoto, Sonis, Hewings, Martins (índices de ligação, eqs. 14-15);
    Sonis, Hewings & Guo (linkages/key sectors)."""
    A = np.array([[0.2, 0.3], [0.4, 0.1]]); Y = [100.0, 50.0]
    got = m.multiplicadores.ligacoes_puras_ghs(A, Y, 0)
    PBL = Y[0] * A[1, 0] / (1 - A[1, 1])
    PFL = A[0, 1] / (1 - A[0, 0]) * 1 / (1 - A[1, 1]) * Y[1]
    assert abs(got["PBL"] - PBL) < 1e-9
    assert abs(got["PFL"] - PFL) < 1e-9
    assert abs(got["PTL"] - (PBL + PFL)) < 1e-9
    # PTLN normaliza pela média -> media(PTLN) == 1 por construção
    g = m.multiplicadores.ghs_todos(A, Y)
    assert abs(g["PTLN"].mean() - 1) < 1e-9


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


# ---------------- contas regionais, Tipo II e produtos (suporte ao estudo BEVAP) ----------------
def test_regional_contas(sys_reg, sys_reg19):
    c = sys_reg19["contas"]
    assert c is not None and {"x", "vab", "remun", "eob", "imp_prod", "imp_produto", "emp"} <= set(c)
    assert abs(c["imp_prod"].sum() - 91071) < 100      # impostos s/ produção (base BEVAP: ~R$ 91 bi)
    assert 100e6 < c["emp"].sum() < 115e6              # ~106 milhões de ocupações em 2019
    assert sys_reg["contas"] is None                   # 2011 não expõe esse bloco


def test_tipo2_fechar_familias(sys_reg19):
    """Modelo fechado (Tipo II) reproduz o fechamento verificado do motor BEVAP."""
    c = sys_reg19["contas"]
    x = c["x"]
    w = np.divide(c["remun"], np.where(x > 0, x, 1.0))
    hh = sys_reg19["f_categorias"]["Famílias"]
    fech = m.multiplicadores.fechar_familias(sys_reg19["A"], w, hh, alpha=1.0)
    assert 0 < fech["rho"] < 1 and abs(fech["rho"] - 0.706) < 0.005    # raio espectral (BEVAP: 0,71)
    mI = sys_reg19["L"].sum(0)
    mII = m.multiplicadores.producao_tipo2(fech)
    assert (mII >= mI - 1e-9).all()                                    # Tipo II ≥ Tipo I
    i = m.regional.idx(sys_reg19, "SP", "S20")
    assert abs(mII[i] - 3.232) < 0.01                                  # S20/SP Tipo II (BEVAP)


def test_regional_produtos():
    p = m.regional.produtos(2019)
    assert len(p) == 128
    assert "P054" in {cod for cod, _ in p}             # "Adubos e fertilizantes" (desambigua S21)


def test_colapsar_sp_rb(sys_reg19):
    """Colapsador 27 UFs -> SP × RB: identidades preservadas e VBP conservado (suporte BEVAP)."""
    NS = m.regional.NS
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s2 = m.regional.colapsar_sp_rb(sys_reg19, "SP")
    assert s2["A"].shape == (2 * NS, 2 * NS) and s2["uf"] == ["SP", "RB"]
    assert s2["A"].sum(0).max() < 1, "coluna de A2 com soma >= 1"
    I = np.eye(2 * NS)
    with np.errstate(all="ignore"):
        assert np.abs((I - s2["A"]) @ s2["L"] - I).max() < 1e-6, "L2 != inv(I-A2)"
        x2 = s2["L"] @ s2["f"]
    xc = s2["contas"]["x"]
    assert np.abs(x2 - xc).sum() / xc.sum() < 1e-3, "L2·f2 não reproduz o VBP agregado"
    xf = sys_reg19["contas"]["x"]; sp = sys_reg19["uf"].index("SP")
    assert abs(xc.sum() - xf.sum()) / xf.sum() < 1e-9, "VBP total não conservado"
    assert abs(xc[:NS].sum() - xf[sp * NS:(sp + 1) * NS].sum()) / xf.sum() < 1e-9, "VBP de SP não conservado"
    # o sistema colapsado também fecha nas famílias e dá Tipo II >= Tipo I
    fech2 = m.regional.fechar_familias_regional(s2, alpha=1.0)
    assert 0 < fech2["rho"] < 1
    mII = m.multiplicadores.producao_tipo2(fech2); mI = s2["L"].sum(0)
    assert (mII >= mI - 1e-9).all(), "Tipo II < Tipo I no sistema SP×RB"


def test_gerador_tipo2(sys_reg19):
    """Geradores Tipo II: consistência com producao_tipo2 e induzido não-negativo (suporte BEVAP)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fech = m.regional.fechar_familias_regional(sys_reg19, alpha=1.0)
        n = fech["n"]
        g1 = m.multiplicadores.gerador_tipo2(fech, np.ones(n))
        assert np.allclose(g1, m.multiplicadores.producao_tipo2(fech), atol=1e-9), \
            "gerador Tipo II com coef unitário deveria reproduzir producao_tipo2"
        c = sys_reg19["contas"]; x = c["x"]
        e = np.divide(c["emp"], np.where(x > 0, x, 1.0))       # emprego por unidade de produção
        gI = m.multiplicadores.gerador(e, sys_reg19["L"])
        gII = m.multiplicadores.gerador_tipo2(fech, e)
    assert (gII >= gI - 1e-9).all(), "gerador de emprego Tipo II < Tipo I"
    assert gII.sum() > gI.sum(), "efeito induzido de emprego deveria ser positivo no agregado"


def test_inserir_atividade(sys_reg19):
    """Inserção de atividade sintética: sistema válido, satélite estendido e fechamento compõe."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s2 = m.regional.colapsar_sp_rb(sys_reg19, "SP")
        N = s2["A"].shape[0]
        compras = np.zeros(N); compras[0] = 0.3; compras[68] = 0.2   # 0,3 de SP-S1; 0,2 de RB-S1
        s3 = m.regional.inserir_atividade(
            s2, compras, satelite={"remun": 0.25, "emp": 1e-5, "vab": 0.5, "imp_prod": 0.02},
            nome="etanol_milho")
        fech = m.regional.fechar_familias_regional(s3, alpha=1.0)
        mII = m.multiplicadores.producao_tipo2(fech)
        gI = m.multiplicadores.gerador(s3["coef_satelite"]["emp"], s3["L"])
        gII = m.multiplicadores.gerador_tipo2(fech, s3["coef_satelite"]["emp"])
    assert s3["A"].shape == (N + 1, N + 1)
    assert s3["A"][:, N].sum() < 1 and abs(s3["A"][:, N].sum() - 0.5) < 1e-12
    I = np.eye(N + 1)
    with np.errstate(all="ignore"):
        assert np.abs((I - s3["A"]) @ s3["L"] - I).max() < 1e-6, "L != inv(I-A) após inserção"
    assert s3["coef_satelite"]["remun"].shape == (N + 1,)
    assert s3["coef_satelite"]["remun"][N] == 0.25
    assert 0 < fech["rho"] < 1 and (mII >= s3["L"].sum(0) - 1e-9).all()
    assert gII[N] >= gI[N] - 1e-12, "Tipo II < Tipo I na atividade inserida"
