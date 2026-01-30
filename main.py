from flask import Flask, render_template_string, request

app = Flask(__name__)


CHANNELS = {
    "band": {
        "name": "Band",
        "url": "https://hqf6tcxuhk.singularcdn.net.br/live/019498af-1fdf-7df5-86bd-e4a6f588d6a7/s1/playlist_nova-a.m3u8?sjwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmlfc3ViIjoiLzAxOTQ5OGFmLTFmZGYtN2RmNS04NmJkLWU0YTZmNTg4ZDZhNy8iLCJ1aWQiOiI2MzZjYmE2Zi03ZWY5LTRiZjEtOGZmZi05OWEzODc2NjM5ZDgiLCJyYXUiOm51bGwsImJleSI6ZmFsc2UsImlpcCI6ZmFsc2UsIm5iZiI6MTc2OTcxNzQyMCwiaWF0IjoxNzY5NzE3NDIwLCJleHAiOjE4MDEyNTM0MjAsImp0aSI6IjYzNmNiYTZmLTdlZjktNGJmMS04ZmZmLTk5YTM4NzY2MzlkOCIsImlzcyI6IlNwYWxsYSJ9.dMygPahTbVfmdsGtFHwUzu5uH11uf0-4f1Y4UHZT6Ks&uid=636cba6f-7ef9-4bf1-8fff-99a3876639d8&magica=sim",
        "logo":"https://logodownload.org/wp-content/uploads/2014/02/band-logo-0.png"
    },
    "tv-cultura": {
        "name": "TV Cultura",
        "url": "https://player-tvcultura.stream.uol.com.br/live/tvcultura_lsd.m3u8?vhost=player-tvcultura.stream.uol.com.br",
        "logo": "https://logodownload.org/wp-content/uploads/2017/11/tv-cultura-logo-5.png"
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TV Digital Comunitária</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; margin: 0; display: flex; }
        #sidebar { width: 250px; background: #1f1f1f; height: 100vh; overflow-y: auto; padding: 20px; }
        #player-container { flex-grow: 1; background: #000; height: 100vh; }
        .channel-item { display: flex; align-items: center; padding: 10px; cursor: pointer; border-radius: 8px; transition: 0.3s; margin-bottom: 10px; text-decoration: none; color: white; }
        .channel-item:hover { background: #333; }
        .channel-item img { width: 40px; margin-right: 15px; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div id="sidebar">
        <h2>Canais Abertos</h2>
        {% for id, info in channels.items() %}
        <a href="/?ch={{ id }}" class="channel-item">
            <img src="{{ info.logo }}" alt="{{ info.name }}">
            <span>{{ info.name }}</span>
        </a>
        {% endfor %}
    </div>
    <div id="player-container">
        {% if current_url %}
            <iframe src="https://hlsplayer.net/embed?type=m3u8&src={{ current_url }}" allowfullscreen></iframe>
        {% else %}
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <p>Selecione um canal para começar a assistir</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/")
def home():
    channel_id = request.args.get('ch')
    current_url = CHANNELS.get(channel_id, {}).get('url')
    return render_template_string(HTML_TEMPLATE, channels=CHANNELS, current_url=current_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)