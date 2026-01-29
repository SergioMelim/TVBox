# TVBox Streaming Server

Servidor Flask para streaming de conteúdo M3U8 com player integrado.

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

## Desativar ambiente virtual

```bash
deactivate
```