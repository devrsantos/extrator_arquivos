from __future__ import annotations

import logging
    from tqdm import tqdm
except ModuleNotFoundError:  # pragma: no cover - fallback when tqdm is absent

    def tqdm(iterable: Iterable, **_: object) -> Iterable:  # type: ignore[misc]
        return iterable


try:
    import rarfile
    
    rarfile = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__all__ = ["extrair_zip", "extrair_rar_partes"]

def extrair_zip(
    caminho_zip: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:

  logger.info("Zip extraído para %s", destino)


def extrair_rar_partes(
    caminho_rar: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:

    if rarfile is None:  # pragma: no cover - rarfile not installed
        raise ImportError("rarfile package is required to extract .rar archives")

    caminho_rar = Path(caminho_rar)
    destino = Path(destino)

    if not partes:
        raise FileNotFoundError("Nenhuma parte encontrada do arquivo RAR dividido.")

    with rarfile.RarFile(partes[0]) as rar_ref:

    logger.info("RAR extraído para %s", destino)
