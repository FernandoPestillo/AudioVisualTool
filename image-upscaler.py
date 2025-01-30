import os
from PIL import Image


def listar_arquivos(pasta):
    """Lista apenas os arquivos de imagem na pasta especificada."""
    extensoes_validas = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
    return [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f)) and os.path.splitext(f)[1].lower() in extensoes_validas]


def obter_resolucao(opcao):
    """Retorna a resolução correspondente à opção escolhida."""
    resolucoes = {
        1: (3840, 2160),  # 4K
        2: (1920, 1080),  # Full HD
        3: (1280, 720),   # HD
        4: (7680, 4320),  # 8k
    }
    return resolucoes.get(opcao, None)


def upscale_imagem(caminho_entrada, caminho_saida, resolucao):
    """Realiza o upscaled-videos da imagem para a resolução especificada mantendo a proporção."""
    try:
        with Image.open(caminho_entrada) as img:
            largura_original, altura_original = img.size
            largura_alvo, altura_alvo = resolucao

            # Calcular nova largura e altura mantendo a proporção
            proporcao_original = largura_original / altura_original
            proporcao_alvo = largura_alvo / altura_alvo

            if proporcao_original > proporcao_alvo:
                # Ajustar com base na largura
                nova_largura = largura_alvo
                nova_altura = int(largura_alvo / proporcao_original)
            else:
                # Ajustar com base na altura
                nova_altura = altura_alvo
                nova_largura = int(altura_alvo * proporcao_original)

            img_upscaled = img.resize((nova_largura, nova_altura), Image.LANCZOS)
            img_upscaled.save(caminho_saida)
            print(f"Imagem salva em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")


# Diretórios de entrada e saída
pasta_entrada = "./images"
pasta_saida = "./upscaled-images"

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
    escolha = int(input("Digite o número da imagem que deseja fazer upscaled-videos: "))
    if 1 <= escolha <= len(arquivos):
        arquivo_escolhido = arquivos[escolha - 1]
        caminho_arquivo = os.path.join(pasta_entrada, arquivo_escolhido)

        # Pergunta a resolução desejada
        print("Escolha a resolução de saída:")
        print("1. 4K (3840x2160)")
        print("2. Full HD (1920x1080)")
        print("3. HD (1280x720)")
        print("4. 8k (7680x4320)")
        opcao_resolucao = int(input("Digite o número da resolução desejada: "))

        resolucao = obter_resolucao(opcao_resolucao)
        if resolucao:
            caminho_saida = os.path.join(pasta_saida, f"upscaled_{arquivo_escolhido}")
            upscale_imagem(caminho_arquivo, caminho_saida, resolucao)
        else:
            print("Opção de resolução inválida.")
    else:
        print("Escolha inválida de imagem.")
