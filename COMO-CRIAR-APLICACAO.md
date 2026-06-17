# Como aplicar a metodologia em outro trabalho (sem desorganizar)

Padrão único do projeto: **`mipcore` é a biblioteca compartilhada; cada trabalho é uma pasta
própria que a importa e escreve só dentro de si.** A dependência é de mão única: aplicações
dependem da `mip`; a `mip` nunca depende de aplicação. Exemplo vivo já funcionando:
[`../sda-brasil/`](../sda-brasil/) (`rodar_sda.py` importa o `mipcore`; `SDA-Brasil-2011-2021.md`
traz os resultados; tudo na própria pasta). **Copie essa forma.**

## Por que assim

O `mipcore` está instalado em modo editável no venv compartilhado `~/.venvs/fgv-mip`, então
`import mipcore` funciona de qualquer pasta, sem copiar nada. Conserto de método na `mip`
propaga na hora para todos os trabalhos. Fragmentar (um venv por projeto, ou copiar os `.py`)
só gera cópias que envelhecem em ritmos diferentes.

## Passo a passo para um trabalho novo

1. Crie a pasta do trabalho onde ele pertence (irmã da `mip`, ou em outra Área do vault),
   com uma subpasta de saída só dela (`resultados/`).
2. Escreva o script importando o `mipcore` e salvando **na própria pasta**:

   ```python
   from pathlib import Path
   import mipcore as m                          # vem do venv; não precisa estar na pasta mip

   SAIDA = Path(__file__).parent / "resultados"
   SAIDA.mkdir(exist_ok=True)

   mat = m.leontief.matrizes(m.tru.carregar(2019))   # dado de referência via mipcore
   sys = m.regional.carregar(2019)                   # matriz interestadual, idem
   # ... sua análise específica; salve em SAIDA ...
   print("mipcore", m.__version__)                   # registre a versão usada
   ```

3. Rode com o interpretador do venv compartilhado:

   ```bash
   ~/.venvs/fgv-mip/bin/python "<sua-pasta>/seu_script.py"
   ```

4. Escreva o relato em um `.md` na pasta, **citando o manual por link** (ex.: método híbrido
   §2.4, MPM §4.15) em vez de copiar o método. Receitas prontas em [COOKBOOK.md](COOKBOOK.md).

## Regras que evitam bagunça

- **Não copie** os arquivos do `mipcore` para a sua pasta; importe o pacote instalado.
- **Não escreva** saída dentro de `mip/`; resultado de aplicação mora na pasta da aplicação.
- **Dados próprios** do trabalho (conta-satélite, coeficientes de emprego etc.) ficam na pasta
  do trabalho e são passados às funções do `mipcore`; não entram na `mip`.
- **Registre `m.__version__`** (e, se a `mip` estiver versionada, o commit) no relato, para
  saber depois qual versão gerou cada resultado.
- **Venv sempre fora do OneDrive** (`~/.venvs/fgv-mip`); um só, compartilhado.

## Reaproveitar o método em outra máquina ou pasta

`import mipcore` só funciona se o venv tiver o pacote instalado e a pasta `mip` estiver
acessível (o editable aponta para ela). Em máquina nova: `pip install -e <caminho>/mip/MIP`
no venv. Se a `mip` mudar de lugar, reinstale do caminho novo.
