from modulos.extratores import extrair_zip, extrair_rar_partes
from modulos.verificacoes import verifica_tem_pasta

def extrair_arquivo(caminho_arquivo, destino='.', progresso_callback=None, lista_callback=None):

    destino_final = verifica_tem_pasta(caminho_arquivo, destino)

    if destino_final is None:
        return
    
    destino = destino_final

    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo {caminho_arquivo} não foi encontrado")
    if caminho_arquivo.endswith('.zip'):
        extrair_zip(caminho_arquivo, destino, progresso_callback, lista_callback)
    elif caminho_arquivo.endswith('.rar'):
        extrair_rar_partes(caminho_arquivo, destino, progresso_callback, lista_callback)
    else:
        raise ValueError("Formato de arquivo não suportado. Use .zip ou .rar")

if __name__ == '__main__':
    import os, glob
    
    pasta_base = os.path.dirname(__file__)
    destino_geral = os.path.join(pasta_base, 'extraidos')
    os.makedirs(destino_geral, exist_ok=True)
    arquivos = (
        glob.glob(os.path.join(pasta_base, '*.zip')) +
        glob.glob(os.path.join(pasta_base, '*.rar')) +
        glob.glob(os.path.join(pasta_base, '*.part1.rar')) +
        glob.glob(os.path.join(pasta_base, '*.parte1.rar'))
    )

    for arquivo in arquivos:
        try:
            extrair_arquivo(arquivo, destino_geral)
        except Exception as e:
            print(f"Erro ao extrair {arquivo}: {e}")