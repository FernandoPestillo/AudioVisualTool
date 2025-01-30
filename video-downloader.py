import os
import yt_dlp

def baixar_video_rapido():
    try:
        # Solicita a URL ao usuário
        url = input("Cole a URL do vídeo: ").strip()
        if not url:
            print("Nenhuma URL foi fornecida.")
            return

        # Define o caminho de saída
        pasta_saida = "videos"
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        # Configurações otimizadas para velocidade
        ydl_opts = {
            'outtmpl': os.path.join(pasta_saida, '%(title)s.%(ext)s'),  # Caminho de saída
            'format': 'bestvideo+bestaudio/best',  # Melhor qualidade disponível
            'n_threads': 8,  # Aumenta as conexões simultâneas para fragmentos
            'external_downloader': 'aria2c',  # Usa aria2c como downloader externo
            'external_downloader_args': ['-x16', '-k1M'],  # 16 conexões por arquivo e tamanho do bloco de 1MB
            'merge_output_format': 'mp4',  # Formato de saída final
            'nocheckcertificate': True,  # Ignorar verificação de certificado para evitar atrasos
        }

        # Executa o download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Download concluído! Arquivo salvo em: {pasta_saida}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chama a função
baixar_video_rapido()
