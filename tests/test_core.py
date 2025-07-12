from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
import zipfile
from types import SimpleNamespace

from extrator.core import extrair_zip, extrair_rar_partes


def test_extrair_zip(tmp_path: Path) -> None:
    # prepara arquivos de origem
    origem = tmp_path / "orig"
    origem.mkdir()
    (origem / "a.txt").write_text("um")
    (origem / "b.txt").write_text("dois")

    zip_path = tmp_path / "teste.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for arq in origem.iterdir():
            zf.write(arq, arq.name)

    destino = tmp_path / "dest"
    destino.mkdir()
    extrair_zip(zip_path, destino)

    assert (destino / "a.txt").read_text() == "um"
    assert (destino / "b.txt").read_text() == "dois"


def test_extrair_rar_partes(monkeypatch, tmp_path: Path) -> None:
    extracted = []

    class DummyRarFile:
        def __init__(self, *_: object) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc: object) -> None:
            pass

        def namelist(self):
            return ["arquivo.txt"]

        def extract(self, nome: str, destino: Path) -> None:
            (Path(destino) / nome).write_text("conteudo")
            extracted.append(nome)

    dummy_module = SimpleNamespace(RarFile=DummyRarFile)
    monkeypatch.setattr("extrator.core.rarfile", dummy_module, raising=False)

    rar_path = tmp_path / "arq.rar"
    rar_path.touch()
    destino = tmp_path / "dest"
    destino.mkdir()

    extrair_rar_partes(rar_path, destino)

    assert extracted == ["arquivo.txt"]
    assert (destino / "arquivo.txt").read_text() == "conteudo"
