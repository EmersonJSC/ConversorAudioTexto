# Programa de Transcrição de Áudio Automática (Script Python)

Este repositório contém um script em Python que transcreve múltiplos arquivos de áudio para texto de forma automática. Ele utiliza a tecnologia de reconhecimento de fala [Whisper da OpenAI](https://openai.com/research/whisper) para gerar transcrições de alta precisão.

Este guia destina-se a usuários que executarão o script diretamente usando um ambiente Python.

## ✨ Funcionalidades

* **Processamento em Lote:** Transcreve todos os arquivos de uma pasta de uma só vez.
* **Suporte a Múltiplos Formatos:** Compatível com os formatos de áudio mais comuns (`.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`).
* **Multiplataforma:** Funciona em Windows, macOS e Linux.
* **Saída Organizada:** Cria arquivos de texto (`.txt`) com o mesmo nome dos áudios originais em uma pasta separada.
* **Configurável:** Permite a fácil alteração do modelo do Whisper para ajustar a precisão vs. velocidade.

## ⚙️ Requisitos

Antes de começar, você precisa ter os seguintes programas instalados no seu sistema:

1.  **[Python](https://www.python.org/downloads/) (versão 3.9 ou superior)**
    * Durante a instalação no Windows, marque a caixa **"Add Python to PATH"**.
2.  **[Git](https://git-scm.com/downloads/)**
    * Necessário para clonar este repositório.
3.  **[FFmpeg](https://ffmpeg.org/download.html)**
    * É uma dependência crucial que o Whisper usa para processar os áudios. Ele precisa estar instalado e acessível no PATH do seu sistema.
        * **Windows:** A maneira mais fácil é usar um gerenciador de pacotes como [Chocolatey](https://chocolatey.org/) (`choco install ffmpeg`) ou [Scoop](https://scoop.sh/) (`scoop install ffmpeg`). Alternativamente, baixe o binário, descompacte-o e adicione a pasta `bin` ao PATH do sistema manualmente.
        * **macOS (com Homebrew):** `brew install ffmpeg`
        * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`
        * **Linux (Arch):** `sudo pacman -S ffmpeg`

## 🚀 Instalação e Configuração

Siga estes passos no seu terminal para configurar o projeto.

**1. Clone o repositório:**
```bash
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
cd SEU_REPOSITORIO
```

**2. Crie e ative um ambiente virtual:**
É altamente recomendado usar um ambiente virtual (`venv`) para isolar as dependências do projeto.
```bash
# Cria o ambiente
python -m venv env

# Ativa o ambiente
# (No Windows)
.\env\Scripts\activate
# (No Linux ou macOS)
source env/bin/activate
```
Seu terminal deverá agora mostrar um `(env)` no início da linha.

**3. Instale as dependências:**
O arquivo `requirements.txt` contém a lista de todas as bibliotecas Python necessárias.
```bash
pip install -r requirements.txt
```

## ▶️ Como Usar

Com a instalação concluída, siga os passos abaixo para transcrever seus áudios.

1.  **Certifique-se de que seu ambiente virtual está ativo.** (Você deve ver `(env)` no prompt do terminal).

2.  **Crie uma pasta chamada `audios`** na raiz do projeto (se ela ainda não existir).

3.  **Copie seus arquivos de áudio** (`.mp3`, `.wav`, etc.) para dentro da pasta `audios`.

4.  **Execute o script principal** a partir da pasta raiz do projeto:
    ```bash
    python transcrever.py
    ```

> **Atenção:** Na **primeira vez** que você executar, o script precisará baixar o modelo de IA do Whisper (por padrão, o modelo "base", com ~150MB). Isso pode demorar um pouco e só acontece uma vez.

5.  Aguarde o processo terminar. O progresso será exibido no terminal.

## 📄 Resultado

Ao final do processo, uma nova pasta chamada `transcricoes` será criada. Dentro dela, você encontrará um arquivo `.txt` para cada áudio processado, contendo a transcrição.

## ⚠️ Solução de Problemas (FAQ)

* **Erro `ModuleNotFoundError: No module named 'whisper'`**
    * **Causa:** Você esqueceu de ativar o ambiente virtual antes de rodar o script.
    * **Solução:** Ative o ambiente com `source env/bin/activate` (ou `.\env\Scripts\activate` no Windows) e tente novamente.

* **Erro `ffmpeg not found` ou similar**
    * **Causa:** O FFmpeg não está instalado ou o sistema não consegue encontrá-lo.
    * **Solução:** Volte à seção de **Requisitos** e garanta que o FFmpeg foi instalado corretamente e está acessível no PATH do seu sistema. Você pode testar isso digitando `ffmpeg -version` no terminal; se ele não for reconhecido, não está no PATH.

* **A qualidade da transcrição está baixa.**
    * **Causa:** A qualidade do áudio original é ruim ou o modelo padrão ("base") não é preciso o suficiente.
    * **Solução:** Você pode usar um modelo maior e mais preciso do Whisper. Abra o arquivo `transcrever.py`, encontre a linha `modelo_whisper: "base"` dentro do dicionário `CONFIG` e mude para `"small"`, `"medium"` ou `"large"`. Modelos maiores exigem mais VRAM e poder de processamento.

## 📄 Licença

Este projeto é distribuído sob a licença MIT.