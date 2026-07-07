"""Configuracao de coleta do pytest para o mipcore.

Dois grupos de dado, com disponibilidade diferente:

1. TRU nacional nivel 68 do IBGE (68_tab*_20XX.xls, ~3,5 MB, publica) — VERSIONADA
   no git. Os testes nacionais (identidades TRU, Leontief, precos basicos,
   multiplicadores, GRAS) rodam sempre, inclusive no CI.

2. Matrizes IIOAS regionais (RBERU 2011 ~124 MB, BRUF 2019 ~99 MB) — NAO
   versionadas (grandes; ficam no cache local / raiz do repo, fora do git). Os
   testes regionais sao PULADOS num runner limpo de CI e rodam so na maquina de
   desenvolvimento que tem as matrizes.

A deteccao replica os caminhos reais de resolucao do mipcore. Pular na coleta
evita o problema de cache de fixture de escopo modulo. MIPCORE_EXIGIR_DADOS=1
exige TUDO (a ausencia de qualquer dado vira erro).
"""
import os
import pytest

# Testes que dependem das MATRIZES IIOAS REGIONAIS (nao-versionadas). Os demais
# dependem so da TRU nacional, que e versionada e esta sempre presente.
_REQUER_IIOAS_REGIONAL = {
    "test_regional_produtos", "test_regional_estrutura",
    "test_regional_autossuficiencia_vs_artigo", "test_regional_indices_e_blocos",
    "test_regional_extracao", "test_regional_2019_estrutura",
    "test_regional_demanda_final", "test_regional_extracao_usa_f_real",
    "test_regional_2019_autossuficiencia", "test_regional_contas",
    "test_tipo2_fechar_familias", "test_colapsar_sp_rb", "test_gerador_tipo2",
    "test_inserir_atividade",
}


def _iioas_regional_presente():
    """As matrizes IIOAS regionais (2011 e/ou 2019) existem? Replica a resolucao
    real de caminho do mipcore.regional."""
    try:
        import mipcore.regional as _reg
    except Exception:
        return False
    candidatos = [_reg._ARQ_2011]
    candidatos += list(getattr(_reg, "_XLSX_2019", []))
    return any(p.exists() for p in candidatos)


def pytest_collection_modifyitems(config, items):
    if os.environ.get("MIPCORE_EXIGIR_DADOS") == "1" or _iioas_regional_presente():
        return  # dev com as matrizes, ou exigencia explicita: roda tudo
    skip = pytest.mark.skip(reason="matriz IIOAS regional nao-versionada ausente "
                                   "(checkout limpo de CI); MIPCORE_EXIGIR_DADOS=1 para exigir")
    for item in items:
        nome = getattr(item, "originalname", None) or item.name.split("[")[0]
        if nome in _REQUER_IIOAS_REGIONAL:
            item.add_marker(skip)
