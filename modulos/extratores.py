from __future__ import annotations

import logging
from pathlib import Path
import zipfile
from typing import Callable, Iterable, Optional, Sequence

try:
    from tqdm import tqdm
except ModuleNotFoundError:  # pragma: no cover - fallback when tqdm is absent

    def tqdm(iterable: Iterable, **_: object) -> Iterable:  # type: ignore[misc]
        return iterable


try:
    import rarfile

    # Path to unrar tool for Windows environments
    rarfile.UNRAR_TOOL = r"C:\\Program Files (x86)\\unrar\\UnRAR.exe"
except ModuleNotFoundError:  # pragma: no cover - fallback when rarfile is absent
    rarfile = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__all__ = ["extrair_zip", "extrair_rar_partes"]


def extrair_zip(
    caminho_zip: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Extrai arquivos de um arquivo ZIP."""
    caminho_zip = Path(caminho_zip)
    destino = Path(destino)

    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        lista = zip_ref.namelist()
        if lista_callback:
            lista_callback(lista)
        total = len(lista)
        for i, arquivo in enumerate(tqdm(lista, desc=f"Extraindo {caminho_zip.name}")):
            zip_ref.extract(arquivo, path=destino)
            if progresso_callback:
                progresso_callback(i + 1, total)
    logger.info("Zip extraído para %s", destino)


def extrair_rar_partes(
    caminho_rar: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Extrai arquivos de um RAR dividido em partes."""
    if rarfile is None:  # pragma: no cover - rarfile not installed
        raise ImportError("rarfile package is required to extract .rar archives")

    caminho_rar = Path(caminho_rar)
    destino = Path(destino)

    pasta = caminho_rar.parent
    nome_base = caminho_rar.name.split(".part")[0]
    partes = sorted(pasta.glob(f"{nome_base}.part*.rar"))

    if not partes:
        raise FileNotFoundError("Nenhuma parte encontrada do arquivo RAR dividido.")

    with rarfile.RarFile(partes[0]) as rar_ref:
        lista = rar_ref.namelist()
        if lista_callback:
            lista_callback(lista)
        total = len(lista)
        for i, arquivo in enumerate(tqdm(lista, desc=f"Extraindo {caminho_rar.name}")):
            rar_ref.extract(arquivo, path=destino)
            if progresso_callback:
                progresso_callback(i + 1, total)
    logger.info("RAR extraído para %s", destino)
