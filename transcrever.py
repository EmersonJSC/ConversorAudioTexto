import whisper
import os
from pathlib import Path  # Biblioteca para lidar com caminhos de arquivos de forma mais robusta
import moviepy.editor as mp # Biblioteca para extrair o áudio do vídeo

# Carrega o modelo do Whisper (pode escolher entre "tiny", "base", "small", "medium", "large")
# "base" é um bom equilíbrio entre velocidade e precisão.
try:
    model = whisper.load_model("base")
    print("Modelo Whisper carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o modelo Whisper: {e}")
    model = None

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
        # Usa pathlib para lidar com o caminho de forma mais segura
        p = Path(caminho_arquivo)
        extensao = p.suffix.lower()

        # Lista de extensões de vídeo comuns
        extensoes_video = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

        # 1. VERIFICA SE É VÍDEO E EXTRAI O ÁUDIO
        if extensao in extensoes_video:
            print(f"Arquivo de vídeo detectado: {p.name}. Extraindo o áudio...")
            arquivo_temporario = True
            
            # Define o caminho para o arquivo de áudio temporário (ex: video.mp4 -> video.mp3)
            caminho_final_audio = p.with_suffix(".mp3")

            # Carrega o clipe de vídeo
            video_clip = mp.VideoFileClip(str(p))
            
            # Extrai o áudio e salva no arquivo temporário
            video_clip.audio.write_audiofile(str(caminho_final_audio), logger=None)
            
            # Fecha os clipes para liberar memória
            video_clip.close()
            print(f"Áudio extraído com sucesso para: {caminho_final_audio.name}")
        else:
            # Se já for áudio, usa o caminho original
            print(f"Arquivo de áudio detectado: {p.name}")
            caminho_final_audio = p

        # 2. TRANSCREVE O ÁUDIO
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
        # 3. LIMPEZA: Apaga o arquivo de áudio temporário se ele foi criado
        if arquivo_temporario and caminho_final_audio and caminho_final_audio.exists():
            os.remove(caminho_final_audio)
            print(f"Arquivo temporário '{caminho_final_audio.name}' foi removido.")

# Se você quiser testar o script diretamente pelo terminal, pode usar este bloco
if __name__ == '__main__':
    # Exemplo de como chamar a função
    # Substitua pelo caminho de um vídeo ou áudio no seu PC
    caminho_do_teste = "caminho/para/seu/video.mp4" 
    if Path(caminho_do_teste).exists():
        texto = transcrever_audio(caminho_do_teste)
        print("\n--- TEXTO TRANSCRITO ---\n")
        print(texto)
    else:
        print(f"Arquivo de teste não encontrado em: {caminho_do_teste}")
        print("Por favor, edite o script para apontar para um arquivo válido.")
