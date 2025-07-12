import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

import main


def test_extrair_arquivo_zip(monkeypatch, tmp_path: Path) -> None:
    arquivo = tmp_path / "arquivo.zip"
    arquivo.touch()

    destino = tmp_path / "dest"
    destino.mkdir()

    called = {}
    monkeypatch.setattr(main, "verifica_tem_pasta", lambda *a, **k: destino / "arquivo")
    monkeypatch.setattr(
        main, "extrair_zip", lambda *a, **k: called.setdefault("zip", True)
    )
    monkeypatch.setattr(
        main, "extrair_rar_partes", lambda *a, **k: called.setdefault("rar", True)
    )

    main.extrair_arquivo(arquivo, destino)
    assert called.get("zip")
    assert not called.get("rar")


def test_extrair_arquivo_rar(monkeypatch, tmp_path: Path) -> None:
    arquivo = tmp_path / "arquivo.rar"
    arquivo.touch()

    destino = tmp_path / "dest"
    destino.mkdir()

    called = {}
    monkeypatch.setattr(main, "verifica_tem_pasta", lambda *a, **k: destino / "arquivo")
    monkeypatch.setattr(
        main, "extrair_zip", lambda *a, **k: called.setdefault("zip", True)
    )
    monkeypatch.setattr(
        main, "extrair_rar_partes", lambda *a, **k: called.setdefault("rar", True)
    )

    main.extrair_arquivo(arquivo, destino)
    assert called.get("rar")
    assert not called.get("zip")


def test_extrair_arquivo_invalido(tmp_path: Path) -> None:
    arquivo = tmp_path / "arquivo.txt"
    arquivo.touch()
    destino = tmp_path / "dest"
    destino.mkdir()
    with pytest.raises(ValueError):
        main.extrair_arquivo(arquivo, destino)
