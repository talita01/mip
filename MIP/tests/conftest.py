"""Configuracao de coleta do pytest para o mipcore.

Varios testes carregam dados brutos pesados (IIOAS_BRUF_2019.xlsx ~115 MB, TRU
68_tab*_20XX.xls, matriz IIOAS 2011) que NAO estao versionados no git (dado
grande fica fora do repo: cache local ~/.cache/mipcore e dados/brutos/). Numa
maquina de desenvolvimento com os dados, todos rodam; num runner limpo de CI os
que dependem de dado sao PULADOS na coleta — o CI valida a logica que independe
de dado externo (formas fechadas, GRAS sintetico de Lenzen, versao/modulos) sem
falhar por dado ausente.

A deteccao replica os caminhos reais de resolucao do mipcore (tru.DADOS,
regional._ARQ_2011, regional._XLSX_2019). Pular na coleta evita o problema de
cache de fixture de escopo modulo (uma fixture que falha por dado ausente
marcaria como ERROR todos os testes seguintes que a reusam). Defina
MIPCORE_EXIGIR_DADOS=1 para exigir os dados (a ausencia volta a ser erro).
"""
import os
import pytest

# Testes que dependem de dado bruto nao-versionado (derivado do que falha num
# checkout limpo). Mantido explicito para que o skip seja deterministico e nao
# dependa de capturar excecao em fase de fixture cacheada.
_REQUER_DADOS = {
    "test_tru_identidades", "test_leontief_controles", "test_precos_basicos_hibrido",
    "test_multiplicadores", "test_gras_estimar_2022", "test_regional_produtos",
    "test_regional_estrutura", "test_regional_autossuficiencia_vs_artigo",
    "test_regional_indices_e_blocos", "test_regional_extracao",
    "test_regional_2019_estrutura", "test_regional_demanda_final",
    "test_regional_extracao_usa_f_real", "test_regional_2019_autossuficiencia",
    "test_regional_contas", "test_tipo2_fechar_familias", "test_colapsar_sp_rb",
    "test_gerador_tipo2", "test_inserir_atividade",
}


def _dados_presentes():
    """Ha ALGUM dado bruto do mipcore acessivel? Replica a resolucao real de
    caminho dos modulos tru e regional. Se nenhum existir, estamos num checkout
    limpo (CI) e os testes que dependem de dado devem ser pulados."""
    try:
        import mipcore.tru as _tru
        import mipcore.regional as _reg
    except Exception:
        return False
    candidatos = [
        _tru.DADOS / "68_tab1_2019.xls",          # TRU nacional 2019
        _reg._ARQ_2011,                            # matriz IIOAS 2011
    ]
    candidatos += list(getattr(_reg, "_XLSX_2019", []))  # IIOAS 2019 (cache/tmp)
    return any(p.exists() for p in candidatos)


def pytest_collection_modifyitems(config, items):
    if os.environ.get("MIPCORE_EXIGIR_DADOS") == "1" or _dados_presentes():
        return  # dev com dados, ou exigencia explicita: roda tudo
    skip = pytest.mark.skip(reason="dado bruto nao-versionado ausente (checkout "
                                   "limpo de CI); MIPCORE_EXIGIR_DADOS=1 para exigir")
    for item in items:
        if item.originalname in _REQUER_DADOS or item.name.split("[")[0] in _REQUER_DADOS:
            item.add_marker(skip)
