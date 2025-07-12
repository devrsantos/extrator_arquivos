# Extrator de Arquivos

Este projeto fornece funções para extrair arquivos `.zip` ou conjuntos de arquivos `.rar` divididos em partes.
Também possui uma interface gráfica simples, desenvolvida com **Tkinter**, que
permite escolher o arquivo a ser extraído e o diretório de destino.

## Estrutura

- `main.py` — ponto de entrada com a função `extrair_arquivo` e um exemplo de uso.
- `extrator/core.py` — implementa as rotinas de extração.
- `extrator/utils.py` — verifica ou cria pastas de destino.
- `tests/` — contém testes automatizados com `pytest`.

## Como usar

1. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Para facilitar, utilize o `Makefile`:

```bash
make run   # executa a interface
make test  # roda a suíte de testes
```

2. Execute o script principal:

```bash
python main.py
```
Ao executar, uma janela do Tkinter será exibida para selecionar o arquivo e a
pasta de destino.

## Testes

Execute a suíte de testes com:

```bash
make test
```

## Formatação e Linting

O projeto sugere o uso das ferramentas [Black](https://black.readthedocs.io/) e [Flake8](https://flake8.pycqa.org/) ou [Ruff](https://docs.astral.sh/ruff/) para manter a formatação e a qualidade do código.
