import time
from pathlib import Path
import whisper

# --- CONFIGURAÇÕES GERAIS ---
# Todas as configurações foram agrupadas neste dicionário para fácil acesso.
CONFIG = {
    "pasta_entrada": "audios",
    "pasta_saida": "transcricoes",
    "modelo_whisper": "base",  # Opções: "tiny", "base", "small", "medium", "large"
    "extensoes_aceitas": ['.wav', '.mp3', '.m4a', '.ogg', '.flac']
}

def carregar_modelo(nome_modelo: str):
    """
    Carrega o modelo Whisper especificado. Na primeira vez, o modelo será baixado.
    Retorna o modelo carregado ou None se ocorrer um erro.
    """
    try:
        print(f"\nCarregando o modelo '{nome_modelo}' do Whisper...")
        modelo = whisper.load_model(nome_modelo)
        print("Modelo carregado com sucesso!")
        return modelo
    except Exception as e:
        print(f"ERRO FATAL: Não foi possível carregar o modelo Whisper. Detalhes: {e}")
        return None

def transcrever_arquivo(modelo, caminho_audio: Path, pasta_saida: Path):
    """
    Transcreve um único arquivo de áudio e salva o resultado em um arquivo .txt.

    Args:
        modelo: O modelo Whisper carregado.
        caminho_audio (Path): O caminho para o arquivo de áudio.
        pasta_saida (Path): A pasta onde o .txt será salvo.

    Returns:
        str: O status da operação ('processado', 'pulado', 'erro').
    """
    nome_base = caminho_audio.stem  # Pega o nome do arquivo sem a extensão
    caminho_txt = pasta_saida / f"{nome_base}.txt"

    if caminho_txt.exists():
        print(f"--- Já existe: '{caminho_txt.name}'. Pulando.")
        return "pulado"

    print(f"[+] Processando: '{caminho_audio.name}'...")
    try:
        resultado = modelo.transcribe(str(caminho_audio))
        texto_transcrito = resultado.get('text', '').strip()

        if not texto_transcrito:
            print(f"   -> Atenção: Nenhum texto detectado no arquivo.")
        
        with open(caminho_txt, 'w', encoding='utf-8') as f:
            f.write(texto_transcrito)
        
        print(f"   -> Salvo em: '{caminho_txt.name}'")
        return "processado"

    except Exception as e:
        print(f"   *** ERRO ao processar '{caminho_audio.name}': {e} ***")
        return "erro"

def main():
    """
    Função principal que orquestra todo o processo.
    """
    print(">>> Iniciando script de transcrição de áudio <<<")
    inicio_total = time.time()
    
    # Converte os nomes das pastas de string para objetos Path
    pasta_entrada = Path(CONFIG["pasta_entrada"])
    pasta_saida = Path(CONFIG["pasta_saida"])

    # Verificação inicial das pastas
    if not pasta_entrada.is_dir():
        print(f"ERRO: A pasta de entrada '{pasta_entrada}' não foi encontrada.")
        return

    pasta_saida.mkdir(exist_ok=True) # Cria a pasta de saída se não existir

    modelo = carregar_modelo(CONFIG["modelo_whisper"])
    if not modelo:
        return # Encerra o script se o modelo não puder ser carregado

    # Dicionário para guardar as estatísticas
    stats = {"processado": 0, "pulado": 0, "erro": 0}

    print("\nIniciando a varredura e transcrição dos arquivos...")
    
    # Itera sobre todos os arquivos na pasta de entrada
    for arquivo in pasta_entrada.iterdir():
        # Verifica se é um arquivo e se a extensão é suportada
        if arquivo.is_file() and arquivo.suffix.lower() in CONFIG["extensoes_aceitas"]:
            status = transcrever_arquivo(modelo, arquivo, pasta_saida)
            stats[status] += 1
    
    duracao_total = time.time() - inicio_total
    
    # Resumo final
    print("\n" + "="*40)
    print(">>> PROCESSO CONCLUÍDO <<<")
    print(f"Tempo total de execução: {duracao_total:.2f} segundos")
    print(f"Arquivos processados com sucesso: {stats['processado']}")
    print(f"Arquivos pulados (transcrição já existia): {stats['pulado']}")
    print(f"Arquivos que resultaram em erro: {stats['erro']}")
    print("="*40)

if __name__ == "__main__":
    main()