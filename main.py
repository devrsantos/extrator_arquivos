from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional, Sequence

from modulos.extratores import extrair_zip, extrair_rar_partes
from modulos.verificacoes import verifica_tem_pasta

logger = logging.getLogger(__name__)

__all__ = ["extrair_arquivo", "main"]


def extrair_arquivo(
    caminho_arquivo: Path | str,
    destino: Path | str = ".",
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Decide o método de extração com base na extensão do arquivo."""
    caminho_arquivo = Path(caminho_arquivo)
    destino = Path(destino)

    destino_final = verifica_tem_pasta(caminho_arquivo, destino)
    if destino_final is None:
        return

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo {caminho_arquivo} não foi encontrado")

    # Seleciona o método de extração com base na extensão
    if caminho_arquivo.suffix == ".zip":
        extrair_zip(caminho_arquivo, destino_final, progresso_callback, lista_callback)
    elif caminho_arquivo.suffix == ".rar":
        # Arquivos divididos em partes utilizam o extrator de RAR
        extrair_rar_partes(
            caminho_arquivo, destino_final, progresso_callback, lista_callback
        )
    else:
        raise ValueError("Formato de arquivo não suportado. Use .zip ou .rar")


def main() -> None:
    """Ponto de entrada para execução direta do módulo."""
    pasta_base = Path(__file__).parent
    destino_geral = pasta_base / "extraidos"
    destino_geral.mkdir(exist_ok=True)

    # Procura por todos os formatos suportados dentro da pasta do script
    arquivos = (
        list(pasta_base.glob("*.zip"))
        + list(pasta_base.glob("*.rar"))
        + list(pasta_base.glob("*.part1.rar"))
        + list(pasta_base.glob("*.parte1.rar"))
    )

    for arquivo in arquivos:
        try:
            extrair_arquivo(arquivo, destino_geral)
        except Exception as exc:  # pragma: no cover - apenas log
            logger.error("Erro ao extrair %s: %s", arquivo, exc)


if __name__ == "__main__":  # pragma: no cover - execução direta
    logging.basicConfig(level=logging.INFO)
    main()
