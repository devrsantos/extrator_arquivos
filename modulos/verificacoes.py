from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

__all__ = ["verifica_tem_pasta"]


def verifica_tem_pasta(
    caminho_arquivo: Path | str, destino: Path | str
) -> Optional[Path]:
    """Garante que existe uma pasta para extração.

    Args:
        caminho_arquivo: Caminho do arquivo a ser extraído.
        destino: Diretório base para criação da pasta.

    Returns:
        Caminho da pasta criada ou ``None`` se a pasta já existia e possuía arquivos.
    """
    caminho_arquivo = Path(caminho_arquivo)
    destino = Path(destino)
    nome_base = caminho_arquivo.stem.split(".part")[0]
    destino_final = destino / nome_base

    if destino_final.exists() and any(destino_final.iterdir()):
        logger.info(
            "Pasta '%s' já existe e não está vazia. Pulando extração.", destino_final
        )
        return None

    destino_final.mkdir(parents=True, exist_ok=True)
    return destino_final
