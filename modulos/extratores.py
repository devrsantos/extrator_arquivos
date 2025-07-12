from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Iterable, Optional, Sequence

try:
    from tqdm import tqdm
except ModuleNotFoundError:  # pragma: no cover - fallback when tqdm is absent

    def tqdm(iterable: Iterable, **_: object) -> Iterable:  # type: ignore[misc]
        return iterable


try:
    import rarfile
except ModuleNotFoundError:  # pragma: no cover - rarfile might not be installed
    rarfile = None  # type: ignore[assignment]

import zipfile

logger = logging.getLogger(__name__)

__all__ = ["extrair_zip", "extrair_rar_partes"]


def extrair_zip(
    caminho_zip: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Extrai um arquivo ZIP para o destino informado."""
    caminho_zip = Path(caminho_zip)
    destino = Path(destino)

    with zipfile.ZipFile(caminho_zip) as zip_ref:
        nomes = zip_ref.namelist()
        if lista_callback:
            lista_callback(nomes)
        total = len(nomes)
        for idx, nome in enumerate(tqdm(nomes, desc="Extraindo ZIP")):
            zip_ref.extract(nome, destino)
            if progresso_callback:
                progresso_callback(idx + 1, total)

    logger.info("Zip extraído para %s", destino)


def extrair_rar_partes(
    caminho_rar: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Extrai um conjunto de arquivos RAR divididos em partes."""
    if rarfile is None:  # pragma: no cover - rarfile not installed
        raise ImportError("rarfile package is required to extract .rar archives")

    caminho_rar = Path(caminho_rar)
    destino = Path(destino)

    # identifica todas as partes do rar (ex: .part1.rar, .part2.rar)
    base = caminho_rar.stem.split(".part")[0]
    partes = sorted(caminho_rar.parent.glob(f"{base}*.rar"))
    if not partes:
        partes = [caminho_rar]

    with rarfile.RarFile(partes[0]) as rar_ref:
        nomes = rar_ref.namelist()
        if lista_callback:
            lista_callback(nomes)
        total = len(nomes)
        for idx, nome in enumerate(tqdm(nomes, desc="Extraindo RAR")):
            rar_ref.extract(nome, destino)
            if progresso_callback:
                progresso_callback(idx + 1, total)

    logger.info("RAR extraído para %s", destino)
