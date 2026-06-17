"""
mipcore.cnt — Contas Nacionais Trimestrais do IBGE via API SIDRA.

Tabela 1846 (valores correntes, var 585) e 1620 (índice de volume encadeado, var 583), classificação
c11255 (setores e subsetores). Frequência trimestral.
"""
import json
import urllib.request

# Setores (c11255): 12 atividades + agregados
SETORES = {
    "agropecuaria": "90687", "ind_extrativas": "90692", "ind_transformacao": "90693",
    "eletricidade_agua": "90695", "construcao": "90694", "comercio": "90697",
    "transporte": "90698", "informacao": "90699", "financeiras": "90700",
    "imobiliarias": "90702", "outros_servicos": "90701", "adm_publica": "90703",
    "VA_precos_basicos": "90705", "impostos": "90706", "PIB_mercado": "90707",
}
SETORES_12 = [SETORES[k] for k in list(SETORES)[:12]]


def carregar(codigos=None, tabela=1846, variavel=585, periodos="all", timeout=90):
    """Retorna ({(trimestre, setor): valor}, [trimestres ordenados]). Trimestre = 'AAAATT' (ex. 202101)."""
    if codigos is None:
        codigos = SETORES_12
    url = (f"https://apisidra.ibge.gov.br/values/t/{tabela}/n1/1/v/{variavel}/p/{periodos}/"
           f"c11255/{','.join(codigos)}/d/v{variavel}%20{'0' if tabela == 1846 else '2'}")
    dados = json.load(urllib.request.urlopen(url, timeout=timeout))
    val, tris = {}, []
    for r in dados[1:]:
        if r["V"] in ("...", "..", "-", None):
            continue
        val[(r["D3C"], r["D4C"])] = float(r["V"])
        if r["D3C"] not in tris:
            tris.append(r["D3C"])
    return val, sorted(tris)


if __name__ == "__main__":
    val, tris = carregar()
    print(f"CNT: {len(tris)} trimestres, de {tris[0]} a {tris[-1]}")
    ult = tris[-1]
    print(f"Último trimestre ({ult}): VA agropecuária = {val.get((ult, SETORES['agropecuaria'])):,.0f}")
