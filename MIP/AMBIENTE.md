# Ambiente reproduzível — mipcore

O `requirements.lock` fixa as versões exatas verificadas contra a suíte de testes.
O `pyproject.toml` traz faixas abstratas para desenvolvimento; o lock é a fonte da
reprodução exata.

## Recriar o ambiente oficial (`~/.venvs/fgv-mip`, fora do OneDrive)

```
python -m venv ~/.venvs/fgv-mip
source ~/.venvs/fgv-mip/bin/activate
cd ~/FGV-Dev/mip/MIP
pip install -r requirements.lock
pip install -e .
pytest tests/ -v          # esperado: 27 passed
```

## Estado verificado (2026-07-06)

- Python 3.13.14; numpy 2.5.1, scipy 1.18.0, pandas 3.0.3, openpyxl 3.1.5, xlrd 2.0.2
- mipcore 1.9.0
- Suíte: 27/27 testes passam, incluindo validação externa contra Lenzen et al. (2007, GRAS)
  e Haddad et al. (2017, ranking de autossuficiência por UF no IIOAS).
- Log: `20_Recursos/metodologias/log-suite-mipcore-2026-07-06.txt` no vault.

## Regenerar o lock (após mudar dependências)

Com o ambiente atualizado e a suíte passando, refazer o fechamento transitivo das deps
de runtime e regravar `requirements.lock` com `pkg==versao` exatos. Atualizar a data e o
estado verificado acima.
