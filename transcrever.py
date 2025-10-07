import os
import ffmpeg # Nova biblioteca importada
import sys

# Importe aqui a biblioteca que você usa para transcrição, por exemplo:
# import speech_recognition as sr

def transcrever_audio(caminho_do_audio):
    """
    Substitua o conteúdo desta função pela sua lógica de transcrição.
    """
    print(f"Iniciando a transcrição para o arquivo: {caminho_do_audio}")
    
    # --- COLOQUE SUA LÓGICA DE TRANSCRIÇÃO AQUI ---
    
    texto_transcrito = "Este é o texto transcrito do áudio."
    print("Transcrição concluída.")
    return texto_transcrito

def processar_arquivo(caminho_do_arquivo):
    """
    Processa um arquivo de áudio ou vídeo, extrai o áudio se necessário,
    e chama a função de transcrição.
    """
    nome_base, extensao = os.path.splitext(caminho_do_arquivo)
    extensoes_video = ['.mp4', '.mov', '.avi', '.mkv']
    
    caminho_do_audio = caminho_do_arquivo
    audio_temporario = False

    if extensao.lower() in extensoes_video:
        print(f"Arquivo de vídeo detectado: {caminho_do_arquivo}")
        print("Extraindo o áudio com FFmpeg...")
        caminho_do_audio = nome_base + ".wav"
        audio_temporario = True
        
        try:
            # --- LÓGICA DE CONVERSÃO COM FFMPEG ---
            (
                ffmpeg
                .input(caminho_do_arquivo)
                .output(caminho_do_audio, acodec='pcm_s16le', ac=1, ar='16000') # Converte para WAV padrão
                .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            )
            print(f"Áudio extraído com sucesso para: {caminho_do_audio}")
            # --- FIM DA LÓGICA DE CONVERSÃO ---
        except ffmpeg.Error as e:
            print("Ocorreu um erro ao extrair o áudio.", file=sys.stderr)
            # A linha abaixo imprime a saída de erro do ffmpeg, que é muito útil para depuração
            print(e.stderr.decode(), file=sys.stderr)
            return

    transcrever_audio(caminho_do_audio)
    
    if audio_temporario:
        print(f"Removendo arquivo de áudio temporário: {caminho_do_audio}")
        os.remove(caminho_do_audio)

if __name__ == "__main__":
    caminho_arquivo_input = input("Arraste o arquivo de áudio/vídeo para cá ou digite o caminho: ").strip().replace("'", "").replace('"', '')
    
    if os.path.exists(caminho_arquivo_input):
        processar_arquivo(caminho_arquivo_input)
    else:
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
