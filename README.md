# TVBox Streaming Server

Servidor Flask para streaming de conteúdo M3U8 com player integrado.

## Instalação

```bash
pip install flask requests
```

## Como usar

```bash
python main.py
```

Acesse `http://localhost:8080` no navegador.

## Funcionalidades

- Player HLS integrado (hlsplayer.net)
- Proxy M3U8 com suporte a parâmetros
- Interface responsiva em tela cheia

## Requisitos

- Python 3.7+
- Flask
- Requests