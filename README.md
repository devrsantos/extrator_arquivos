# Extrator de Arquivos

Este projeto fornece funções para extrair arquivos `.zip` ou conjuntos de arquivos `.rar` divididos em partes.

## Estrutura

- `main.py` — ponto de entrada com a função `extrair_arquivo` e um exemplo de uso.
- `modulos/extratores.py` — implementa as rotinas de extração.
- `modulos/verificacoes.py` — verifica a existência de pastas de destino.
- `tests/` — contém testes automatizados com `pytest`.

## Como usar

1. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Execute o script principal:

```bash
python main.py
```

## Testes

Execute a suíte de testes com:

```bash
pytest
```

## Formatação e Linting

O projeto sugere o uso das ferramentas [Black](https://black.readthedocs.io/) e [Flake8](https://flake8.pycqa.org/) ou [Ruff](https://docs.astral.sh/ruff/) para manter a formatação e a qualidade do código.
