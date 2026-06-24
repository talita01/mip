"""mipcore — toolkit de Matriz Insumo-Produto (IBGE) reutilizável.

Submódulos:
  tru             — leitura das Tabelas de Recursos e Usos (qualquer ano).
  precos_basicos  — passagem a preços básicos (estrutura oficial 2015).
  leontief        — matrizes A, D, Bn e inversa de Leontief.
  multiplicadores — produção, geradores, Rasmussen-Hirschman, ligações puras GHS.
  sda             — decomposição estrutural (tecnologia × demanda) a preços constantes.
  cnt             — Contas Nacionais Trimestrais (SIDRA).
  gras            — projeção de anos sem TRU 68 (2022+) via GRAS + TRU nível 12.
  regional        — sistema inter-regional IIOAS (27 UFs × 68 setores, anos 2011 e 2019):
                    multiplicadores, R-H, autossuficiência, demanda final e extração por UF.
  cadeia          — cadeia de valor por extração de efeitos EF1-EF4 (Harthoorn 1989).
"""
from . import tru, precos_basicos, leontief, multiplicadores, sda, cnt, gras, regional, cadeia
__all__ = ["tru", "precos_basicos", "leontief", "multiplicadores", "sda", "cnt", "gras",
           "regional", "cadeia"]
__version__ = "1.7.0"
