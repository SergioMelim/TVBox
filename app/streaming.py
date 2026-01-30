from flask import Flask, Response
import requests

app = Flask(__name__)

# Rota para transmitir o stream m3u8
@app.route('/stream/<channel>')
def stream(channel):
    # Verifica se o canal existe
    if channel not in CHANNELS:
        return "Canal não encontrado!", 404

    # Obtém a URL do canal
    url = CHANNELS[channel]['url']

    # Faz a requisição para o stream
    def generate():
        with requests.get(url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk

    return Response(generate(), content_type='application/x-mpegURL')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
