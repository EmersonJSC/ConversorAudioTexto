import whisper
import os
from pathlib import Path
import subprocess # <--- Módulo nativo para rodar comandos do terminal

# Carrega o modelo do Whisper
try:
    model = whisper.load_model("base")
    print("Modelo Whisper carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o modelo Whisper: {e}")
    model = None

def extrair_audio_com_ffmpeg(caminho_video, caminho_saida_audio):
    """
    Usa o FFmpeg diretamente para extrair o áudio de um vídeo.
    Retorna True se for bem-sucedido, False caso contrário.
    """
    print("Executando o FFmpeg para extrair o áudio...")
    
    # O comando que será executado no terminal.
    # -i: arquivo de entrada
    # -vn: ignora o vídeo (não processa o vídeo)
    # -acodec libmp3lame: codec de áudio para MP3
    # -ab 192k: bitrate do áudio para 192 kbps (boa qualidade)
    # -y: sobrescreve o arquivo de saída se ele já existir (evita que o script trave)
    command = [
        "ffmpeg",
        "-i", str(caminho_video),
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-y",
        str(caminho_saida_audio)
    ]

    try:
        # Roda o comando. check=True faz com que um erro seja lançado se o ffmpeg falhar.
        # capture_output=True esconde a saída do ffmpeg e a captura para depuração.
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Áudio extraído com sucesso pelo FFmpeg.")
        return True
    except FileNotFoundError:
        print("\nERRO: O comando 'ffmpeg' não foi encontrado.")
        print("Verifique se o FFmpeg está instalado e configurado no PATH do seu sistema.")
        return False
    except subprocess.CalledProcessError as e:
        # Se o FFmpeg retornar um erro (ex: arquivo de vídeo inválido)
        print("\nERRO: O FFmpeg encontrou um problema.")
        print(f"Comando: {' '.join(command)}")
        print(f"Erro retornado:\n{e.stderr}") # Mostra a mensagem de erro exata do FFmpeg
        return False


def transcrever_audio(caminho_arquivo):
    """
    Transcreve o conteúdo de um arquivo de áudio ou vídeo.
    Se for um vídeo, extrai o áudio primeiro e depois transcreve.
    """
    if not model:
        return "Erro: Modelo Whisper não foi carregado. A transcrição não pode continuar."

    caminho_final_audio = None
    arquivo_temporario = False

    try:
        p = Path(caminho_arquivo)
        extensao = p.suffix.lower()
        extensoes_video = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

        if extensao in extensoes_video:
            arquivo_temporario = True
            caminho_final_audio = p.with_suffix(".mp3")
            
            # CHAMA A NOSSA NOVA FUNÇÃO USANDO SUBPROCESS
            sucesso = extrair_audio_com_ffmpeg(p, caminho_final_audio)
            
            if not sucesso:
                return "Falha ao extrair o áudio do vídeo com FFmpeg."
        else:
            print(f"Arquivo de áudio detectado: {p.name}")
            caminho_final_audio = p

        print("Iniciando a transcrição com o Whisper...")
        if caminho_final_audio and caminho_final_audio.exists():
            resultado = model.transcribe(str(caminho_final_audio), fp16=False)
            texto_transcrito = resultado['text']
            print("Transcrição concluída.")
            return texto_transcrito
        else:
            return "Erro: Arquivo de áudio não foi encontrado para transcrição."

    except Exception as e:
        print(f"Ocorreu um erro durante o processo: {e}")
        return f"Erro: {e}"

    finally:
        if arquivo_temporario and caminho_final_audio and caminho_final_audio.exists():
            os.remove(caminho_final_audio)
            print(f"Arquivo temporário '{caminho_final_audio.name}' foi removido.")
