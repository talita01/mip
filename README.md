# MIP — Base metodológica de Insumo-Produto (FGV-Bioeconomia)

Base de referência **genérica** de análise de insumo-produto, para reutilizar em problemas
de pesquisa distintos (multiplicadores, setores-chave, impacto de demanda, decomposição
estrutural, regionalização por UF, comércio em valor adicionado). **Diretriz de escopo:**
tudo relacionado a **conta-satélite** (ambiental, bioeconomia) fica **fora desta pasta**;
aqui mora só o ferramental MIP geral.

## O que tem aqui

| Camada | Onde | O quê |
|---|---|---|
| **Metodologia** | [`Manual-Metodologico-Insumo-Produto.md`](Manual-Metodologico-Insumo-Produto.md) | Documento de referência, verificado por leitura direta das fontes (convenção ✅/⚠️/🔁). Mapeia pergunta → método → fonte (§9). **Leia a advertência de vigência no §1** (transição SCN 2010→2021). |
| **Código** | [`MIP/mipcore/`](MIP/mipcore/) | Pacote Python `mipcore` (v1.3.0): `tru`, `precos_basicos`, `leontief`, `multiplicadores`, `sda`, `gras`, `regional`, `cnt`. |
| **Geradores** | [`MIP/`](MIP/) | `gerar_matrizes_estimadas.py` (MIP nacional, anos com TRU 68), `gerar_matriz_gras.py` (2022+ via GRAS), `validar_ras.py`. |
| **Receitas** | [`COOKBOOK.md`](COOKBOOK.md) | Pergunta de pesquisa → comando rodável → resultado. |
| **Reuso em outros trabalhos** | [`COMO-CRIAR-APLICACAO.md`](COMO-CRIAR-APLICACAO.md) | Padrão para aplicar a metodologia em outra pasta sem desorganizar (biblioteca compartilhada + aplicação irmã). Exemplo: `../sda-brasil/`. |
| **Testes** | [`MIP/tests/`](MIP/tests/) | Suíte pytest (controles + validações externas). |
| **Dados** | `MIP/dados/` e raiz | TRU 68 (2010–2021), MIP oficial 2015/2010, matrizes estimadas, matrizes interestaduais IIOAS 2011/2019. Inventário completo na §1.4 do manual. |
| **Skill** | `.claude/skills/estimar-mip/` | `/estimar-mip <ano>` no Claude Code: roda o ciclo completo (verifica → gera → double check → relatório). |

## Setup (uma vez)

O `venv` fica **FORA do OneDrive** (milhares de arquivos quebram a sincronização):

```bash
python3 -m venv ~/.venvs/fgv-mip
~/.venvs/fgv-mip/bin/pip install -e "/Users/talitapinto/Library/CloudStorage/OneDrive-FGV/Obsidian-Vault/30_Areas/FGV-Bioeconomia/mip/MIP"
~/.venvs/fgv-mip/bin/pip install pytest        # para a suíte de testes
```

Dependências: numpy, scipy, openpyxl, xlrd (instaladas pelo editable install). Se
`import mipcore` falhar por caminho, reinstale do caminho atual (o vault já migrou de pasta).

**Matriz interestadual 2019** (uma vez): o `.xlsx` (~115 MB) vem compactado; extraia-o para o
cache, fora do OneDrive, para `m.regional.carregar(2019)` encontrá-lo:

```bash
unar -o ~/.cache/mipcore "/Users/talitapinto/Library/CloudStorage/OneDrive-FGV/Obsidian-Vault/30_Areas/FGV-Bioeconomia/mip/IIOAS_BRUF_2019 (1).rar"
```

A matriz 2011 funciona sem esse passo (o arquivo já está na raiz da pasta).

## Uso rápido

```python
import mipcore as m
d   = m.tru.carregar(2019)                 # TRU nível 68 a preços básicos (método híbrido)
mat = m.leontief.matrizes(d)               # A, L=(I-A)^-1, Z, g, VAB, atividades
mp  = m.multiplicadores.producao_tipo1(mat["L"])         # multiplicador de produção tipo I
sys = m.regional.carregar(2019)            # sistema interestadual IIOAS (27 UFs × 68 setores; 2019 ou 2011)
```

Receitas completas em [`COOKBOOK.md`](COOKBOOK.md).

## Testes

```bash
~/.venvs/fgv-mip/bin/python -m pytest MIP/tests/ -v
```

Cobrem identidades contábeis das TRU, controles de Leontief, método híbrido de preços,
GRAS (exemplo de Lenzen et al. 2007) e o sistema regional, com **validações externas**
contra resultados publicados (ranking de autossuficiência por UF do artigo do IIOAS).

## Estado das fontes e honestidade

O manual declara, ponto a ponto, o que foi verificado por leitura direta da fonte primária
(✅), o que é lacuna (⚠️) e o que é analogia (🔁), com registro de erros corrigidos. Ver a
"Nota de honestidade" ao fim do manual. **Nada é afirmado sem origem rastreável.**
