from pathlib import Path

from modulos.verificacoes import verifica_tem_pasta


def test_cria_pasta(tmp_path: Path) -> None:
    arquivo = tmp_path / "exemplo.zip"
    arquivo.touch()

    destino = tmp_path / "dest"
    destino.mkdir()

    resultado = verifica_tem_pasta(arquivo, destino)
    assert resultado == destino / "exemplo"
    assert resultado.exists()


def test_pula_quando_pasta_nao_vazia(tmp_path: Path) -> None:
    arquivo = tmp_path / "exemplo.rar"
    arquivo.touch()

    destino_final = tmp_path / "dest" / "exemplo"
    destino_final.mkdir(parents=True)
    (destino_final / "arquivo.txt").write_text("conteudo")

    resultado = verifica_tem_pasta(arquivo, tmp_path / "dest")
    assert resultado is None
