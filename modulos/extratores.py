import rarfile  # Importa o módulo para manipular arquivos .rar
from tqdm import tqdm

# Define o caminho para o unrar.exe no Windows
rarfile.UNRAR_TOOL = r"C:\Program Files (x86)\unrar\UnRAR.exe"

import glob, os, zipfile

def extrair_zip(caminho_zip, destino, progresso_callback, lista_callback):
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        lista = zip_ref.namelist()
        if lista_callback:
            lista_callback(lista)
        total = len(lista)

        for i, arquivo in enumerate(tqdm(lista, desc=f"Extraindo {os.path.basename(caminho_zip)}")):
            zip_ref.extract(arquivo, path=destino)
            if progresso_callback:
                progresso_callback(i + 1, total)
        print(f"Zip extraido para {destino}")

def extrair_rar_partes(caminho_rar, destino, progresso_callback, lista_callback):
    pasta = os.path.dirname(caminho_rar)
    nome_base = os.path.basename(caminho_rar).split('.part')[0]
    partes = sorted(glob.glob(os.path.join(pasta, f"{nome_base}.part*.rar")))

    if not partes:
        raise FileNotFoundError("Nenhuma parte encontrada do arquivo RAR dividido.")
    
    with rarfile.RarFile(partes[0]) as rar_ref:
        lista = rar_ref.namelist()
        if lista_callback:
            lista_callback(lista)
        total = len(lista)

        for i, arquivo in enumerate(tqdm(lista, desc=f"Extraindo {os.path.basename(caminho_rar)}")):
            rar_ref.extract(arquivo, path=destino)
            if progresso_callback:
                progresso_callback(i + 1, total)
        print(f"RAR extraído para: {destino}")