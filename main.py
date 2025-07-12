from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional, Sequence

from modulos.verificacoes import verifica_tem_pasta

logger = logging.getLogger(__name__)

__all__ = ["extrair_arquivo", "main"]


def extrair_arquivo(
    caminho_arquivo: Path | str,
    destino: Path | str = ".",
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:

if __name__ == "__main__":  # pragma: no cover - execução direta
    logging.basicConfig(level=logging.INFO)
    main()
