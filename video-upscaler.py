import os
import subprocess
import re
import sys
import time

def list_videos(folder):
    """Lista todos os vídeos na pasta especificada."""
    videos = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    return videos

def get_video_duration(input_path):
    """Obtém a duração do vídeo em segundos usando o FFmpeg."""
    command = [
        "ffmpeg",
        "-i", input_path,
        "-hide_banner"
    ]
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    duration_match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if duration_match:
        hours, minutes, seconds = map(float, duration_match.groups())
        return hours * 3600 + minutes * 60 + seconds
    return 0

def upscale_video_with_progress(input_path, output_path, width, height):
    """Usa o FFmpeg para fazer o upscaled-videos e exibe o progresso."""
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"scale={width}:{height}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_path,
        "-progress", "-",  # Adiciona progresso na saída
        "-nostats"         # Remove outras estatísticas
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    duration = get_video_duration(input_path)

    print(f"Duração do vídeo: {duration:.2f} segundos")
    for line in process.stdout:
        # Captura a saída para progresso
        if "out_time_ms" in line:
            match = re.search(r"out_time_ms=(\d+)", line)
            if match:
                current_time = int(match.group(1)) / 1_000_000  # Converte microsegundos para segundos
                progress = (current_time / duration) * 100
                sys.stdout.write(f"\rProgresso: {progress:.2f}%")
                sys.stdout.flush()

    process.wait()
    print("\nProcessamento concluído!")

def choose_resolution():
    """Exibe as predefinições de resolução e permite a escolha do usuário."""
    print("Escolha uma resolução predefinida:")
    print("1. Full HD (1920x1080)")
    print("2. 4K (3840x2160)")
    print("3. Personalizado (Digite manualmente)")

    choice = input("Digite o número da opção desejada: ")

    if choice == "1":
        return 1920, 1080
    elif choice == "2":
        return 3840, 2160
    elif choice == "3":
        width = input("Digite a largura desejada (ex: 1920): ")
        height = input("Digite a altura desejada (ex: 1080): ")
        try:
            width = int(width)
            height = int(height)
            return width, height
        except ValueError:
            print("Resolução inválida. Use números inteiros.")
            return None, None
    else:
        print("Opção inválida!")
        return None, None

def main():
    videos_folder = "./videos"
    output_folder = "./upscaled-videos"
    os.makedirs(output_folder, exist_ok=True)

    # Listar vídeos disponíveis
    videos = list_videos(videos_folder)
    if not videos:
        print("Nenhum vídeo encontrado na pasta /videos.")
        return

    print("Vídeos disponíveis para upscaled-videos:")
    for i, video in enumerate(videos):
        print(f"{i + 1}. {video}")

    # Escolher um vídeo
    choice = input("Digite o número do vídeo que deseja fazer o upscaled-videos: ")
    try:
        video_index = int(choice) - 1
        if video_index < 0 or video_index >= len(videos):
            raise ValueError
    except ValueError:
        print("Escolha inválida.")
        return

    selected_video = videos[video_index]
    input_path = os.path.join(videos_folder, selected_video)
    output_path = os.path.join(output_folder, selected_video)

    # Escolher a resolução
    width, height = choose_resolution()
    if width is None or height is None:
        return

    print(f"Processando '{selected_video}' para resolução {width}x{height}...")

    start_time = time.time()

    upscale_video_with_progress(input_path, output_path, width, height)

    end_time = time.time()  # Finaliza a contagem do tempo
    total_time = end_time - start_time

    print(f"\nVídeo processado e salvo em: {output_path}")
    print(f"Tempo total de execução: {total_time:.2f} segundos")

if __name__ == "__main__":
    main()
