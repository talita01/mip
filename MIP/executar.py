#!/usr/bin/env python3
"""
executar.py — Master script de reprodução do módulo de impactos MIP do BEVAP.

Ponto de entrada único (DCAS): reproduz, do dado bruto ao resultado final e à figura,
o pipeline de impacto econômico do complexo BEVAP por Matriz Insumo-Produto:

    carregar(2019) -> colapsar SP x RB -> inserir vertente sintetica -> fechar nas
    familias (Tipo II) -> choque de demanda final -> decompor Tipo I / Tipo II / induzido
    -> figura e tabelas em saidas/

Uso (a partir de MIP/, com o venv do repo):

    python executar.py

Requer: a matriz interestadual IIOAS 2019 (Haddad et al., 2025) no cache
`~/.cache/mipcore/IIOAS_BRUF_2019.xlsx` (nao versionada; ver README e o catalogo
40_Dados/). Sem ela o script para com instrucao de como obte-la.

ATENCAO — coeficientes da vertente ILUSTRATIVOS. O build-up de custos/VA/CAPEX da
Targa (viabilidade) ainda nao foi recebido. Os coeficientes em VERTENTE_ILUSTRATIVA
abaixo sao um placeholder plausivel para demonstrar o mecanismo; NAO sao a estimativa
de impacto do BEVAP. Quando o build-up chegar, substituir esse unico dict.

Determinístico: sem estocasticidade, sem semente a fixar.

Mapa de reproducao (figura/tabela -> este script):
    saidas/bevap_decomposicao.png      <- fig_decomposicao()  (secao 6)
    saidas/bevap_decomposicao.csv      <- exportar()          (secao 6)
    saidas/bevap_resumo.txt            <- main()              (secao 7)
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path
import numpy as np

import mipcore.regional as reg
import mipcore.multiplicadores as mm

# --------------------------------------------------------------------------- #
# Configuracao
# --------------------------------------------------------------------------- #
ANO = 2019
UF_ALVO = "SP"
ALPHA = 1.0                       # propensao a consumir no fechamento Tipo II
CHOQUE_RS_MILHOES = 1000.0        # venda externa (demanda final) a nova vertente
SAIDAS = Path(__file__).resolve().parent / "saidas"

# --- VERTENTE ILUSTRATIVA (placeholder — substituir pelo build-up da Targa) --- #
# compras: coeficiente de compra por R$ de producao da vertente, por (regiao, setor)
# de origem. Chave = (uf, codigo_setor). O que nao soma vira vazamento/importacao.
# satelite: coeficientes de conta-satelite por R$ de producao da vertente.
VERTENTE_ILUSTRATIVA = {
    "nome": "etanol_milho (ILUSTRATIVO)",
    "compras": {                 # Sigma < 1 (o resto e valor adicionado + importacao)
        ("SP", "S01"): 0.42,     # milho (agropecuaria SP)
        ("RB", "S01"): 0.06,     # milho (resto do Brasil)
        ("SP", "S38"): 0.05,     # eletricidade/utilidades
        ("SP", "S33"): 0.04,     # quimicos
        ("SP", "S23"): 0.03,     # transporte
    },
    "satelite": {                # por R$ de producao da vertente
        "remun": 0.11,
        "eob": 0.24,
        "imp_prod": 0.02,
        "emp": 8e-6,             # ocupacoes por R$ milhao -> ver escala em fig
    },
    "consumo_familias": 0.0,
}
# vab e derivado: 1 - Sigma(compras). Nao se fixa a mao.


# --------------------------------------------------------------------------- #
# 1. Carregar e colapsar
# --------------------------------------------------------------------------- #
def carregar_colapsado():
    """Sistema inter-regional 2019 colapsado em SP x Resto do Brasil (136 = 2*68)."""
    try:
        s = reg.carregar(ANO)
    except FileNotFoundError as e:
        _sys.exit(f"\nERRO: base regional {ANO} ausente.\n{e}\n")
    return reg.colapsar_sp_rb(s, UF_ALVO)


# --------------------------------------------------------------------------- #
# 2. Montar o vetor de compras da vertente na ordem do sistema
# --------------------------------------------------------------------------- #
def montar_compras(s2):
    """Traduz o dict {(uf, setor): coef} no vetor (N,) na ordem do sistema colapsado."""
    n = s2["A"].shape[0]
    compras = np.zeros(n)
    for (uf, setor), coef in VERTENTE_ILUSTRATIVA["compras"].items():
        i = reg.idx(s2, uf, setor)
        compras[i] = coef
    total = compras.sum()
    if total >= 1:
        _sys.exit(f"ERRO: Sigma compras = {total:.3f} >= 1 (coluna invalida)")
    return compras


# --------------------------------------------------------------------------- #
# 3. Inserir a vertente e 4. fechar nas familias
# --------------------------------------------------------------------------- #
def inserir_e_fechar(s2, compras):
    s3 = reg.inserir_atividade(
        s2, compras,
        satelite=VERTENTE_ILUSTRATIVA["satelite"],
        consumo_familias=VERTENTE_ILUSTRATIVA["consumo_familias"],
        nome=VERTENTE_ILUSTRATIVA["nome"],
    )
    fech = reg.fechar_familias_regional(s3, alpha=ALPHA)
    return s3, fech


# --------------------------------------------------------------------------- #
# 5. Choque e 6. decomposicao Tipo I / Tipo II / induzido
# --------------------------------------------------------------------------- #
def decompor(s3, fech):
    """Choque de demanda final (venda externa) a nova vertente; decompoe os impactos."""
    n = s3["A"].shape[0]
    y = np.zeros(n)
    y[-1] = CHOQUE_RS_MILHOES                  # a nova atividade e o ultimo indice
    L = s3["L"]
    Lbar = fech["Lbar"][:n, :n]                # bloco setorial do sistema fechado

    x_I = L @ y                                # producao Tipo I
    x_II = Lbar @ y                            # producao Tipo II (com induzido)

    coef = s3["coef_satelite"]
    contas = {
        "producao": np.ones(n),
        "valor_adicionado": _vab(s3),
        "remuneracoes": coef.get("remun", np.zeros(n)),
        "impostos_producao": coef.get("imp_prod", np.zeros(n)),
        "emprego": coef.get("emp", np.zeros(n)),
    }
    linhas = {}
    for nome, c in contas.items():
        tI = float(c @ x_I)
        tII = float(c @ x_II)
        linhas[nome] = {"tipo_I": tI, "tipo_II": tII, "induzido": tII - tI}
    return linhas, fech["rho"]


def _vab(s3):
    """Coeficiente de valor adicionado por R$ de producao = 1 - Sigma coluna de A."""
    return 1.0 - s3["A"].sum(0)


# --------------------------------------------------------------------------- #
# 6b. Figura
# --------------------------------------------------------------------------- #
def fig_decomposicao(linhas, rho):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    monet = ["producao", "valor_adicionado", "remuneracoes", "impostos_producao"]
    rot = {"producao": "Produção", "valor_adicionado": "Valor\nadicionado",
           "remuneracoes": "Remune-\nrações", "impostos_producao": "Impostos\ns/ produção"}
    tI = [linhas[k]["tipo_I"] for k in monet]
    ind = [linhas[k]["induzido"] for k in monet]
    xpos = np.arange(len(monet))

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.bar(xpos, tI, 0.6, label="Tipo I (direto+indireto)", color="#4C72B0")
    ax.bar(xpos, ind, 0.6, bottom=tI, label="Induzido (Tipo II − I)", color="#DD8452")
    for i, (a, b) in enumerate(zip(tI, ind)):
        ax.text(i, a + b, f"{a + b:,.0f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(xpos); ax.set_xticklabels([rot[k] for k in monet], fontsize=8)
    ax.set_ylabel("R$ milhões")
    ax.set_title(f"Impacto de R$ {CHOQUE_RS_MILHOES:,.0f} mi de venda externa — "
                 f"vertente ILUSTRATIVA\nSP × RB, fechamento Tipo II (ρ={rho:.4f})",
                 fontsize=9, loc="left")
    ax.legend(frameon=False, fontsize=8)
    fig.text(0.01, -0.02, "Coeficientes da vertente ILUSTRATIVOS (build-up da Targa não "
             "recebido). Base: matriz interestadual 2019 (Haddad et al., 2025). mipcore.",
             fontsize=6, style="italic", color="#555")
    fig.tight_layout()
    SAIDAS.mkdir(exist_ok=True)
    out = SAIDAS / "bevap_decomposicao.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


def exportar(linhas):
    SAIDAS.mkdir(exist_ok=True)
    out = SAIDAS / "bevap_decomposicao.csv"
    with open(out, "w", encoding="utf-8") as f:
        f.write("conta,tipo_I,tipo_II,induzido\n")
        for k, v in linhas.items():
            f.write(f"{k},{v['tipo_I']:.4f},{v['tipo_II']:.4f},{v['induzido']:.4f}\n")
    return out


# --------------------------------------------------------------------------- #
# 7. Orquestracao
# --------------------------------------------------------------------------- #
def main():
    s2 = carregar_colapsado()
    compras = montar_compras(s2)
    s3, fech = inserir_e_fechar(s2, compras)
    linhas, rho = decompor(s3, fech)
    fig = fig_decomposicao(linhas, rho)
    csv = exportar(linhas)

    SAIDAS.mkdir(exist_ok=True)
    resumo = SAIDAS / "bevap_resumo.txt"
    with open(resumo, "w", encoding="utf-8") as f:
        f.write("BEVAP — decomposicao de impacto (VERTENTE ILUSTRATIVA)\n")
        f.write(f"Base {ANO} | SP x RB | choque R$ {CHOQUE_RS_MILHOES:,.0f} mi | "
                f"alpha={ALPHA} | rho={rho:.6f}\n\n")
        f.write(f"{'conta':<20}{'Tipo I':>14}{'Tipo II':>14}{'induzido':>14}\n")
        for k, v in linhas.items():
            f.write(f"{k:<20}{v['tipo_I']:>14.2f}{v['tipo_II']:>14.2f}{v['induzido']:>14.2f}\n")

    print("Reproducao concluida. Saidas em saidas/:")
    for p in (fig, csv, resumo):
        print(f"  - {p.name}")
    print(f"\nrho (fechamento Tipo II) = {rho:.6f}")
    print("Coeficientes da vertente ILUSTRATIVOS — nao e a estimativa de impacto do BEVAP.")
    return linhas


if __name__ == "__main__":
    main()
