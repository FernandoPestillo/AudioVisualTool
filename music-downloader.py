import os
import subprocess


def baixar_audio_yt_dlp(url, pasta_destino="musics"):
    try:
        # Cria a pasta de destino se ela não existir
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        # Comando yt-dlp para baixar apenas o áudio
        comando = [
            "yt-dlp",
            "-x", "--audio-format", "mp3",
            "-o", f"{pasta_destino}/%(title)s.%(ext)s",
            url
        ]

        # Executa o comando
        subprocess.run(comando, check=True)
        print("Download concluído!")
    except Exception as e:
        print(f"Erro ao baixar o áudio: {e}")


# Exemplo de uso
url_video = input("Digite a URL do vídeo do YouTube: ")
baixar_audio_yt_dlp(url_video)
