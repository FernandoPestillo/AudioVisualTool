import os
from PIL import Image


def listar_arquivos(pasta):
    """Lista os arquivos na pasta especificada."""
    return [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]


def obter_resolucao(opcao):
    """Retorna a resolução correspondente à opção escolhida."""
    resolucoes = {
        1: (1920, 1080),  # Full HD
        2: (3840, 2160),  # 4K
    }
    return resolucoes.get(opcao, None)


def upscale_imagem(caminho_entrada, caminho_saida, resolucao):
    """Realiza o upscale da imagem para a resolução especificada."""
    try:
        with Image.open(caminho_entrada) as img:
            img_upscaled = img.resize(resolucao, Image.LANCZOS)
            img_upscaled.save(caminho_saida)
            print(f"Imagem salva em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")


# Diretórios de entrada e saída
pasta_entrada = "./images"
pasta_saida = "./upscale-images"

# Certifica-se de que os diretórios de entrada e saída existem
os.makedirs(pasta_entrada, exist_ok=True)
os.makedirs(pasta_saida, exist_ok=True)

# Lista os arquivos disponíveis na pasta de entrada
arquivos = listar_arquivos(pasta_entrada)
if not arquivos:
    print("Nenhuma imagem encontrada na pasta ./imagens.")
else:
    print("Imagens disponíveis:")
    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i}. {arquivo}")

    # Pergunta ao usuário qual imagem deseja processar
    escolha = int(input("Digite o número da imagem que deseja fazer upscale: "))
    if 1 <= escolha <= len(arquivos):
        arquivo_escolhido = arquivos[escolha - 1]
        caminho_arquivo = os.path.join(pasta_entrada, arquivo_escolhido)

        # Pergunta a resolução desejada
        print("Escolha a resolução de saída:")
        print("1. Full HD (1920x1080)")
        print("2. 4K (3840x2160)")
        opcao_resolucao = int(input("Digite o número da resolução desejada: "))

        resolucao = obter_resolucao(opcao_resolucao)
        if resolucao:
            caminho_saida = os.path.join(pasta_saida, f"upscaled_{arquivo_escolhido}")
            upscale_imagem(caminho_arquivo, caminho_saida, resolucao)
        else:
            print("Opção de resolução inválida.")
    else:
        print("Escolha inválida de imagem.")
