from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional, Sequence


from extrator.core import extrair_rar_partes, extrair_zip
from extrator.utils import verifica_tem_pasta

import tkinter as tk
from tkinter import filedialog, messagebox

logger = logging.getLogger(__name__)

__all__ = ["extrair_arquivo", "main"]


def extrair_arquivo(
    caminho_arquivo: Path | str,
    destino: Path | str = ".",
    progresso_callback: Optional[Callable[[int, int], None]] = None,
    lista_callback: Optional[Callable[[Sequence[str]], None]] = None,
) -> None:
    """Determina o tipo de arquivo e delega para o extrator adequado.

    Levanta:
        FileNotFoundError: se ``caminho_arquivo`` não existir.
        ValueError: se a extensão do arquivo não for suportada.
    """

    caminho_arquivo = Path(caminho_arquivo)
    destino = Path(destino)

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não encontrado")

    destino_final = verifica_tem_pasta(caminho_arquivo, destino)
    if destino_final is None:  # pasta já existente e não vazia
        return

    if caminho_arquivo.suffix.lower() == ".zip":
        extrair_zip(caminho_arquivo, destino_final, progresso_callback, lista_callback)
    elif caminho_arquivo.suffix.lower() == ".rar":
        extrair_rar_partes(
            caminho_arquivo, destino_final, progresso_callback, lista_callback
        )
    else:
        raise ValueError("Formato de arquivo não suportado")


def main() -> None:  # pragma: no cover - interface gráfica
    """
    Inicializa a interface gráfica para o extrator de arquivos, permitindo ao usuário selecionar um arquivo compactado
    (.zip ou .rar) e um diretório de destino para extração. Fornece botões para seleção dos caminhos e executa a extração,
    exibindo mensagens de sucesso ou erro conforme apropriado.

    Levanta:
        RuntimeError: Se o Tkinter não estiver disponível na instalação atual.
    """
    if tk is None:
        raise RuntimeError("Tkinter não está disponível nesta instalação")

    root = tk.Tk()
    root.title("Extrator de Arquivos")

    arquivo_var = tk.StringVar()
    destino_var = tk.StringVar()

    def escolher_arquivo() -> None:
        caminho = filedialog.askopenfilename(
            title="Arquivo a extrair",
            filetypes=[("Arquivos compactados", "*.zip *.rar")],
        )
        if caminho:
            arquivo_var.set(caminho)

    def escolher_destino() -> None:
        caminho = filedialog.askdirectory(title="Destino")
        if caminho:
            destino_var.set(caminho)

    def iniciar() -> None:
        if not arquivo_var.get() or not destino_var.get():
            messagebox.showerror("Erro", "Arquivo e destino devem ser selecionados.")
            return
        try:
            extrair_arquivo(Path(arquivo_var.get()), Path(destino_var.get()))
            messagebox.showinfo("Sucesso", f"Arquivo extraído em {destino_var.get()}")
        except Exception as exc:  # pragma: no cover - feedback de erro
            messagebox.showerror("Erro", str(exc))

    tk.Label(root, text="Arquivo:").grid(row=0, column=0, sticky="w")
    tk.Entry(root, textvariable=arquivo_var, width=50).grid(row=0, column=1)
    tk.Button(root, text="Selecionar", command=escolher_arquivo).grid(row=0, column=2)

    tk.Label(root, text="Destino:").grid(row=1, column=0, sticky="w")
    tk.Entry(root, textvariable=destino_var, width=50).grid(row=1, column=1)
    tk.Button(root, text="Selecionar", command=escolher_destino).grid(row=1, column=2)

    tk.Button(root, text="Extrair", command=iniciar).grid(row=2, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":  # pragma: no cover - execução direta
    logging.basicConfig(level=logging.INFO)
    main()
