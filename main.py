from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional, Sequence

from modulos.extratores import extrair_rar_partes, extrair_zip
from modulos.verificacoes import verifica_tem_pasta

logger = logging.getLogger(__name__)

__all__ = ["extrair_arquivo", "main"]


def extrair_arquivo(
    caminho_arquivo: Path | str,
    destino: Path | str = ".",
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Escolhe o extrator conforme a extensão."""
    caminho = Path(caminho_arquivo)
    destino = Path(destino)

    destino_final = verifica_tem_pasta(caminho, destino)
    if destino_final is None:
        return
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo {caminho} não foi encontrado")

    extratores = {".zip": extrair_zip, ".rar": extrair_rar_partes}
    extrator = extratores.get(caminho.suffix)
    if not extrator:
        raise ValueError("Formato de arquivo não suportado. Use .zip ou .rar")
    extrator(caminho, destino_final, progresso_callback, lista_callback)


PADROES = ["*.zip", "*.rar", "*.part1.rar", "*.parte1.rar"]


def listar_arquivos(pasta: Path) -> list[Path]:
    return [f for p in PADROES for f in pasta.glob(p)]


def main() -> None:
    """Busca arquivos e os extrai."""
    base = Path(__file__).parent
    destino = base / "extraidos"
    destino.mkdir(exist_ok=True)

    for arquivo in listar_arquivos(base):
        try:
            extrair_arquivo(arquivo, destino)
        except Exception as exc:  # pragma: no cover - log
            logger.error("Erro ao extrair %s: %s", arquivo, exc)


if __name__ == "__main__":  # pragma: no cover - execução direta
    logging.basicConfig(level=logging.INFO)
    main()
