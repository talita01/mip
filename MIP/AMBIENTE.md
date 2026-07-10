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
pytest tests/ -v          # esperado: 40 passed
```

## Estado verificado (2026-07-06)

- Python 3.13.14; numpy 2.5.1, scipy 1.18.0, pandas 3.0.3, openpyxl 3.1.5, xlrd 2.0.2
- mipcore 1.9.0
- Suíte: 27/27 testes passam, incluindo validação externa contra Lenzen et al. (2007, GRAS)
  e Haddad et al. (2017, ranking de autossuficiência por UF no IIOAS).
- Log: `20_Recursos/metodologias/log-suite-mipcore-2026-07-06.txt` no vault.

## Estado verificado (2026-07-08, `.venv` do repo)

Verificação no `.venv` de `~/FGV-Dev/mip/MIP` (não o venv oficial `~/.venvs/fgv-mip`):

- Python 3.11.15; numpy 2.4.6, scipy 1.17.1, pandas 2.3.3
- mipcore 1.9.0
- Suíte: 28/28 testes passam em ~3s (o 28º, `test_ligacoes_puras_ghs_forma_fechada`, entrou no commit bf7efae de 06/07, mesmo dia do carimbo acima).
- As versões de pacotes acima diferem do `requirements.lock` (dentro das faixas do `pyproject`, fora do lock); a reprodução exata do lock só é garantida no venv oficial.

## Auditoria de método (2026-07-08)

- **Correção GHS** em `multiplicadores.ligacoes_puras_ghs`: o termo PBL (ligação pura
  para trás) estava sem o fator interno `Dj = 1/(1-Ajj)`, subestimando a ligação. Forma
  canônica reposta: `PBL = Dr·Arj·Dj·Yj` (GUILHOTO, 2011, eqs. 6.23-6.24; GUILHOTO et al.,
  MIP-Nordeste, eqs. 109-110). Verificado por aritmética racional exata em caso 3×3.
  Novo teste `test_ligacoes_puras_ghs_propriedades_independentes` blinda a propriedade por
  via externa ao código (valores racionais exatos, reconstituição de Guilhoto eq. 6.22,
  invariância a permutação de rótulos).
- **Cobertura de `sda.py`** (antes sem teste): novo `tests/test_sda.py` com 6 testes —
  aditividade, formas polares independentes (Dietzenbacher & Los, 1998), consistência
  Leontief `L·f=g`, reconciliação por categoria (caminho independente) e encadeamento da
  série. Dados TRU "ano anterior" versionados: roda no CI limpo.
- Suíte: **35/35** testes passam em ~3s.

## Auditoria de método (2026-07-10)

- **Cobertura de `cnt.py`** (antes sem teste): novo `tests/test_cnt.py` com 5 testes do
  leitor das Contas Nacionais Trimestrais (SIDRA). O `urlopen` é substituído por FIXTURE
  no formato real da API (capturado do SIDRA em 2026-07-10) — sem dependência de rede,
  roda no CI limpo. Trava: parsing fiel, filtragem de valores ausentes ("...", "..", "-"),
  construção da URL (sufixo `d/` muda com a tabela: 1846→0 decimais, 1620→2) e default de
  12 setores. `cnt.py` fonte não foi alterado.
- **CI em matriz de dois jobs** (`.github/workflows/testes.yml`): `faixas` (Python 3.11,
  instala das faixas abstratas do `pyproject`) e `lock` (Python 3.13, instala do
  `MIP/requirements.lock`). O verde do job `lock` significa que o ambiente fixado ainda
  reproduz; o do job `faixas`, que o pacote instala do zero no Python mínimo suportado.
  O lock oficial (numpy 2.5.1, scipy 1.18.0) reproduz a suíte em Python 3.13 — verificado
  em venv limpo; **exige Python ≥3.12** (numpy 2.5.1 não tem wheel para 3.11).
- **Golden regression no núcleo** (`tests/test_golden_multiplicadores.py` +
  `tests/golden/`): congela o vetor de multiplicadores de produção Tipo I e os índices
  de Rasmussen-Hirschman da TRU nacional 2019 num `.npz` versionado, com SHA-256 no
  manifesto `.sha256.json`. Dois contratos: integridade (checksum do arquivo) e reprodução
  (np.allclose rtol 1e-9 — não byte-exato, pois numpy 2.4.6 e 2.5.1 batem a ~1e-15 mas com
  bytes distintos). Pega regressão silenciosa que preserve as identidades mas mude os
  valores. Verificado por mutação (`L.sum(0)`→`L.sum(1)` derruba o teste).
- Contagem: **44/44** local (dados regionais presentes); **30/30** num runner limpo de CI,
  onde o `conftest` pula os 14 testes regionais (matrizes IIOAS não-versionadas).

## Auditoria de método (2026-07-10, golden estendido)

- **Golden Tipo II + geradores** (`tests/test_golden_tipo2.py` +
  `tests/golden/multiplicadores_tipo2_2019.npz`): estende o golden ao modelo fechado nas
  famílias. Congela o multiplicador de produção Tipo II e os geradores de VA e renda (2019).
  O `w` do fechamento (remunerações/produção) é lido da aba VA da `68_tab2` (offset de
  coluna 1, alinhado contra o VAB); o `c` (cesta de consumo) vem da coluna "familias" da DF
  via market-share. Fechamento estável (rho≈0,71, igual ao BEVAP); II/I médio ≈1,63.
  Verificado por mutação (fatiar Lbar errado derruba o teste).
- **Golden multi-ano**: `test_golden_multiplicadores.py` agora é parametrizado em
  **2015 e 2019** (`.npz` + manifesto por ano). Congelar mais de um ano guarda regressão no
  carregamento por ano — bug que afete só a leitura de um ano passaria despercebido com um
  único ano congelado.
- Contagem: **52/52** local; **38/38** num runner limpo de CI (14 regionais pulados).

## Regenerar o lock (após mudar dependências)

Com o ambiente atualizado e a suíte passando, refazer o fechamento transitivo das deps
de runtime e regravar `requirements.lock` com `pkg==versao` exatos. Atualizar a data e o
estado verificado acima.
