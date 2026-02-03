# TVBox Streaming Server

Servidor Flask para streaming de conteúdo M3U8 com player integrado. Inclui interface web para visualização e servidor de streaming para integração com Jellyfin.

## Requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Criar ambiente virtual

```bash
python3 -m venv venv
```

### 2. Ativar o ambiente virtual

**No Linux/Mac:**
```bash
source venv/bin/activate
```

**No Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install flask requests yt-dlp
```

Opcionalmente, instale `ffmpeg` se pretende usar funcionalidades de processamento/recorte ou download com `yt-dlp`:

- No Debian/Ubuntu:

```bash
sudo apt update && sudo apt install ffmpeg -y
```

- No Fedora/CentOS:

```bash
sudo dnf install ffmpeg -y
```

- No Windows (chocolatey):

```powershell
choco install ffmpeg
```

## Como usar

### Opção 1: Interface Web (main.py)

```bash
python3 main.py
```

Acesse `http://localhost:8085` no navegador.

### Opção 2: Servidor de Streaming (app/streaming.py)

```bash
cd app
python3 streaming.py
```

O servidor escuta na porta `5000`.

### Opção 3: StreamHub Player (app/streamhub.py)

Player profissional de TVBox com suporte a IPTV (API Xtream), Live TV, Filmes e Séries. Funciona independente e com interface completa estilo Smart TV.

```bash
cd app
python3 streamhub.py
```

Acesse `http://localhost:8085` no navegador.

**Como usar:**

1. Na tela inicial, clique em **CONFIG** (ícone de ferramentas).
2. Preencha os dados do seu servidor IPTV:
   - **Servidor**: URL base (ex: `http://iptv-provider.com:80`)
   - **Usuário**: Seu username
   - **Senha**: Sua password
3. Clique em **SALVAR**.
4. Volte e escolha uma categoria: **TV AO VIVO**, **FILMES** ou **SÉRIES**.
5. Navegue pelas categorias e streams disponíveis.

**Funcionalidades:**

- Proxy de vídeo para streams em tempo real (live MPEG-TS e VoD MP4)
- Suporte a API Xtream completa
- Player de vídeo com controles HLS e MPEG-TS
- Interface responsiva tipo Smart TV
- Salva configurações no localStorage do navegador
- Suporta thumbnails/capas dos canais e conteúdos

## Uso do `yt_dlp`

O `main.py` usa `yt_dlp` para listar transmissões ao vivo (rota `/get_caze`). Instruções rápidas:

- `yt-dlp` já é instalado via `pip install yt-dlp` (veja seção dependências).
- Instale `ffmpeg` se for necessário para processamento/downloads (opcional).

Exemplo de execução (dentro do ambiente virtual):

```bash
# Executa o servidor principal (interface)
python3 main.py

# Em outro terminal, executa o servidor de proxy HLS
cd app && python3 streaming.py
```

Observações:

- `yt_dlp` é utilizado apenas para extrair listas/metadados de streams; o projeto não faz downloads automáticos.
- O `app/streaming.py` faz proxy de streams HLS (m3u8). Embeds do YouTube não funcionam via proxy — use URLs m3u8 diretas ou a interface web.

## URLs para Jellyfin

Para integrar com Jellyfin, use as seguintes URLs (substitua o IP/hostname conforme necessário):

```
http://localhost:5000/stream/band
http://localhost:5000/stream/sbt
http://localhost:5000/stream/record-news
http://localhost:5000/stream/tv-cultura
```

## Funcionalidades

### main.py
- Player HLS integrado (hlsplayer.net)
- Interface responsiva em tela cheia
- Seleção de canais em sidebar

### app/streaming.py
- Servidor M3U8 para streaming direto
- Compatível com Jellyfin e outros aplicativos
- Suporte a proxy de streams

## Canais Disponíveis

- **band**: Band
- **sbt**: SBT
- **record-news**: Record News
- **tv-cultura**: TV Cultura

## Desativar ambiente virtual

```bash
deactivate
```