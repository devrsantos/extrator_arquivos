from __future__ import annotations

import logging
import zipfile
from pathlib import Path
from typing import Callable, Iterable, Optional, Protocol, Sequence

try:
    # tqdm exibe barras de progresso no console. Se não estiver instalado,
    # criamos uma função de mesma assinatura para manter o código funcional.
    from tqdm import tqdm
except ModuleNotFoundError:  # pragma: no cover - fallback when tqdm is absent

    def tqdm(iterable: Iterable, **_: object) -> Iterable:  # type: ignore[misc]
        return iterable


try:
    import rarfile

    # Para ambientes Windows, define o caminho para o executável `unrar`.
    rarfile.UNRAR_TOOL = r"C:\\Program Files (x86)\\unrar\\UnRAR.exe"
except ModuleNotFoundError:  # pragma: no cover - fallback when rarfile is absent
    # A extração de .rar ficará indisponível caso o pacote não exista.
    rarfile = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__all__ = ["extrair_zip", "extrair_rar_partes"]


class ArquivoExtraivel(Protocol):
    def namelist(self) -> Sequence[str]: ...

    def extract(self, member: str, path: Path) -> None: ...


def _extrair(
    arquivo: ArquivoExtraivel,
    destino: Path,
    descricao: str,
    progresso_callback: Optional[Callable[[int, int], None]],
    lista_callback: Optional[Callable[[Sequence[str]], None]],
) -> None:
    lista = arquivo.namelist()
    if lista_callback:
        lista_callback(lista)
    total = len(lista)
    for i, item in enumerate(tqdm(lista, desc=descricao), start=1):
        arquivo.extract(item, path=destino)
        if progresso_callback:
            progresso_callback(i, total)


def extrair_zip(
    caminho_zip: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Extrai arquivos de um ZIP."""
    caminho_zip = Path(caminho_zip)
    destino = Path(destino)
    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        _extrair(
            zip_ref,
            destino,
            f"Extraindo {caminho_zip.name}",
            progresso_callback,
            lista_callback,
        )
    logger.info("Zip extraído para %s", destino)


def extrair_rar_partes(
    caminho_rar: Path | str,
    destino: Path | str,
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Extrai arquivos de partes RAR."""
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
        _extrair(
            rar_ref,
            destino,
            f"Extraindo {caminho_rar.name}",
            progresso_callback,
            lista_callback,
        )
    logger.info("RAR extraído para %s", destino)
