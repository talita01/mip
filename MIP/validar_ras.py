"""
Validação retroativa (backcast) do método GRAS para projetar a MIP 68 setores além de 2021.

Pergunta decisiva: se eu só tivesse a estrutura de um ano-base e os agregados do nível 12
do ano-alvo (situação real de 2022+), quão perto eu chegaria da matriz verdadeira?

Desenho (fora da amostra, mesma filosofia do benchmark do método híbrido — manual §2.4):
  alvo = 2021 (matriz verdadeira conhecida via mipcore/TRU 68)
  A) GRAS com margens VERDADEIRAS de 2021 (cota superior da qualidade do método);
  B) GRAS com margens REALISTAS: margens do ano-base escaladas pelo crescimento dos
     12 blocos da TRU nível 12 (exatamente a informação disponível para 2022) —
     implementação de produção em mipcore.gras.estimar;
  C) baseline ingênuo: A(ano-base) usada sem ajuste.
Bases testadas: 2020 (salto de 1 ano ~ 2021→2022) e 2019 (salto de 2 ~ 2021→2023).

Algoritmo, fontes e aproximações declaradas: docstring de mipcore/gras.py.
Resultados de 11 jun. 2026 (registrados no manual, §2.5):
  base 2020: A 0,29% | B 2,77% (máx 14,4%) | C 4,02%   (desvio dos multiplicadores tipo I)
  base 2019: A 0,36% | B 2,99% (máx 13,0%) | C 4,01%

Uso: source ~/.venvs/fgv-mip/bin/activate && python validar_ras.py
"""
import warnings
import numpy as np
import mipcore as mip
from mipcore.gras import gras, estimar


def _teste_gras():
    """Exemplo numérico de Lenzen et al. (2007), eq. (2), p. 463: a estimativa inicial
    já satisfaz as margens (u=v=(1,5)); o GRAS correto deve devolvê-la intacta."""
    A = np.array([[-1.0, 2.0], [2.0, 3.0]])
    X = gras(A, np.array([1.0, 5.0]), np.array([1.0, 5.0]))
    assert np.abs(X - A).max() < 1e-6, f"teste GRAS falhou: {X}"
    print("teste GRAS (exemplo Lenzen et al. 2007, p. 463): ok — estimativa perfeita preservada")


def avaliar(A_est, m_alvo, rotulo):
    L_est = np.linalg.inv(np.eye(len(A_est)) - A_est)
    mp_est = mip.multiplicadores.producao_tipo1(L_est)
    mp_real = mip.multiplicadores.producao_tipo1(m_alvo["L"])
    dev = np.abs(mp_est / mp_real - 1)
    rL = np.corrcoef(L_est.ravel(), m_alvo["L"].ravel())[0, 1]
    wmape_Z = np.abs(A_est * m_alvo["g"][None, :] - m_alvo["Z"]).sum() / m_alvo["Z"].sum()
    print(f"  {rotulo:36s} desv.mult médio {dev.mean()*100:5.2f}%  "
          f"máx {dev.max()*100:5.2f}%  r(L) {rL:.4f}  WMAPE(Z) {wmape_Z*100:5.2f}%")
    return dev


def backcast(ano_base, ano_alvo):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mb = mip.leontief.matrizes(mip.tru.carregar(ano_base))
        ma = mip.leontief.matrizes(mip.tru.carregar(ano_alvo))
        est = estimar(ano_alvo, ano_base)

    print(f"\n== base {ano_base} -> alvo {ano_alvo} ==")
    avaliar(mb["A"], ma, "C ingênuo: A(base) sem ajuste")
    Zr = gras(mb["Z"], ma["Z"].sum(1), ma["Z"].sum(0))
    avaliar(Zr / ma["g"][None, :], ma, "A GRAS margens verdadeiras")
    dev = avaliar(est["A"], ma, "B GRAS margens nível 12 (realista)")

    ats = [c.strip() for c in ma["atividades"]]
    piores = np.argsort(dev)[::-1][:5]
    print("  piores setores (B):", ", ".join(f"{ats[k]} {dev[k]*100:.1f}%" for k in piores))


if __name__ == "__main__":
    _teste_gras()
    backcast(2020, 2021)
    backcast(2019, 2021)
