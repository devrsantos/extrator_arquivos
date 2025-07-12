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

    Se a pasta já existir e contiver arquivos, nenhuma ação é executada e
    ``None`` é retornado.
    """
    caminho_arquivo = Path(caminho_arquivo)
    destino = Path(destino)

    destino_final = destino / caminho_arquivo.stem
    if destino_final.exists() and any(destino_final.iterdir()):
        logger.info(
            "Pasta '%s' já existe e não está vazia. Pulando extração.", destino_final
        )
        return None

    destino_final.mkdir(parents=True, exist_ok=True)
    return destino_final
