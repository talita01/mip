"""
mipcore.tru — Leitura das Tabelas de Recursos e Usos (TRU) do IBGE, nível 68 (68 atividades × 128
produtos), qualquer ano disponível em dados/brutos/tru_anos/.

Fonte oficial: IBGE, Sistema de Contas Nacionais, nível 68. Estrutura validada por identidades
contábeis exatas (ver mipcore.tru.checar_identidades).
"""
from pathlib import Path
import numpy as np
import xlrd

DADOS = Path(__file__).resolve().parent.parent / "dados" / "brutos" / "tru_anos"
R0, R1 = 5, 133            # 128 produtos
N_ATIV = 68


def _num(ws, r0, r1, c0, c1):
    o = np.zeros((r1 - r0, c1 - c0))
    for i, r in enumerate(range(r0, r1)):
        for j, c in enumerate(range(c0, c1)):
            v = ws.cell_value(r, c)
            o[i, j] = v if isinstance(v, (int, float)) else 0.0
    return o


def _cod(v, largura):
    """Normaliza código de produto/atividade: em alguns anos (ex.: 2016) a célula vem numérica
    (1911.0) em vez de texto ('01911'); zero-padding restaura o código oficial."""
    if isinstance(v, (int, float)):
        return f"{int(v):0{largura}d}"
    return str(v).split("\n")[0].strip()


def codigos_atividades(ano=2019):
    ws = xlrd.open_workbook(DADOS / f"68_tab1_{ano}.xls").sheet_by_name("producao")
    return [_cod(ws.cell_value(3, c), 4) for c in range(2, 2 + N_ATIV)]


def carregar(ano=2019):
    """Retorna dict com as matrizes/vetores básicos da TRU (R$ milhões a preço corrente/consumidor)."""
    t1 = xlrd.open_workbook(DADOS / f"68_tab1_{ano}.xls")
    t2 = xlrd.open_workbook(DADOS / f"68_tab2_{ano}.xls")
    prod_ws = t1.sheet_by_name("producao")
    produtos = [_cod(prod_ws.cell_value(r, 0), 5) for r in range(R0, R1)]
    of = t1.sheet_by_name("oferta")
    oferta = {k: _num(of, R0, R1, c, c + 1).ravel() for k, c in
              [("oferta_pc", 2), ("MGC", 3), ("MGT", 4), ("II", 5), ("IPI", 6),
               ("ICMS", 7), ("OUTROS", 8), ("IMPOSTOS", 9), ("oferta_pb", 10)]}
    va = t2.sheet_by_name("VA")
    def varow(lbl):
        for i in range(5, va.nrows):
            if isinstance(va.cell_value(i, 0), str) and lbl in va.cell_value(i, 0):
                return _num(va, i, i + 1, 1, 1 + N_ATIV).ravel()
        raise KeyError(lbl)
    return {
        "ano": ano, "produtos": produtos, "atividades": codigos_atividades(ano),
        "oferta": oferta,
        "V_pa": _num(prod_ws, R0, R1, 2, 2 + N_ATIV),                       # produção produto×atividade
        "importacao": _num(t1.sheet_by_name("importacao"), R0, R1, 2, 3).ravel(),
        "U_pa": _num(t2.sheet_by_name("CI"), R0, R1, 2, 2 + N_ATIV),        # consumo interm. (preço consumidor)
        "DF": _num(t2.sheet_by_name("demanda"), R0, R1, 2, 8),             # demanda final (6 categorias)
        "demanda_cols": ["exportacao", "governo", "isflsf", "familias", "fbcf", "estoque"],
        "VA": {"VAB": varow("Valor adicionado bruto"), "valor_prod": varow("Valor da produção")},
        "g": varow("Valor da produção"),                                   # produção por atividade (básico)
        "q": _num(prod_ws, R0, R1, 2 + N_ATIV, 3 + N_ATIV).ravel(),        # total por produto
    }


def codigos_produtos(ano=2019):
    return carregar(ano)["produtos"]


def checar_identidades(ano=2019):
    """Identidades contábeis de controle (devem fechar exatamente)."""
    d = carregar(ano); U, DF, of, VAB, g = d["U_pa"], d["DF"], d["oferta"], d["VA"]["VAB"], d["g"]
    return {
        "CI+DF=oferta_pc": abs((U.sum() + DF.sum()) - of["oferta_pc"].sum()),
        "g=CI_col+VAB(max)": float(np.abs(g - (U.sum(0) + VAB)).max()),
        "PIB_mercado": float(VAB.sum() + of["IMPOSTOS"].sum()),
    }


if __name__ == "__main__":
    print("Anos disponíveis:", sorted(int(p.stem.split("_")[-1]) for p in DADOS.glob("68_tab1_*.xls")))
    for k, v in checar_identidades(2019).items():
        print(f"  {k}: {v:,.3f}")
