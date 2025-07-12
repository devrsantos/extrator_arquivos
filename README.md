# Extrator de Arquivos

Este projeto fornece funcoes para extrair arquivos `.zip` ou conjuntos de `.rar` divididos em partes. A aplicacao inclui uma interface grafica simples em **Tkinter** para selecionar o arquivo a ser extraido e o diretorio de destino.

## Estrutura

- `main.py` — ponto de entrada com a funcao `extrair_arquivo` e um exemplo de uso.
- `extrator/core.py` — implementa as rotinas de extracao.
- `extrator/utils.py` — verifica ou cria pastas de destino.
- `tests/` — contem testes automatizados com `pytest`.

## Requisitos e ambiente

Recomenda-se o uso de um ambiente virtual para isolar as dependencias. Este repositorio utiliza `requirements.txt` para o versionamento dos pacotes.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como usar

O `Makefile` contem tarefas utilitarias:

```bash
make run      # executa a interface
make test     # roda a suite de testes
make format   # aplica o Black
make lint     # roda o Ruff
make ci       # executa formatacao, lint e testes
```

Para iniciar manualmente a aplicacao:

```bash
python main.py
```

Ao executar, uma janela do Tkinter sera exibida para selecionar o arquivo e a pasta de destino.

## Testes

Execute a suite com:

```bash
make test
```

Sempre que adicionar novos recursos, inclua testes unitarios ou de integracao para manter a qualidade do projeto.

## Integracao continua

Este repositorio possui um workflow do GitHub Actions que valida formacao, lint e testes a cada `push` ou `pull request`.

## Contribuindo

Formate o codigo com [Black](https://black.readthedocs.io/) e verifique eventuais problemas com [Ruff](https://docs.astral.sh/ruff/). Utilize `make ci` antes de enviar as alteracoes e mantenha as boas praticas descritas neste README.
