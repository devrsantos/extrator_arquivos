import os
def verifica_tem_pasta(caminho_arquivo, destino):
    nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0].split('.part')[0]
    destino_final = os.path.join(destino, nome_base)

    if os.path.exists(destino_final) and os.listdir(destino_final):
        print(f"Pasta '{destino_final}' já existe e não está vazia. Pulando extração.")
        return None
    
    os.makedirs(destino_final, exist_ok=True)
    return destino_final