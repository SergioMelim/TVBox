from flask import Flask, render_template_string, request

app = Flask(__name__)

# DICIONÁRIO DE CANAIS
CHANNELS = {
    "band": {
        "name": "Band",
        "url": "https://hqf6tcxuhk.singularcdn.net.br/live/019498af-1fdf-7df5-86bd-e4a6f588d6a7/s1/playlist_nova-a.m3u8?sjwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmlfc3ViIjoiLzAxOTQ5OGFmLTFmZGYtN2RmNS04NmJkLWU0YTZmNTg4ZDZhNy8iLCJ1aWQiOiI2MzZjYmE2Zi03ZWY5LTRiZjEtOGZmZi05OWEzODc2NjM5ZDgiLCJyYXUiOm51bGwsImJleSI6ZmFsc2UsImlpcCI6ZmFsc2UsIm5iZiI6MTc2OTcxNzQyMCwiaWF0IjoxNzY5NzE3NDIwLCJleHAiOjE4MDEyNTM0MjAsImp0aSI6IjYzNmNiYTZmLTdlZjktNGJmMS04ZmZmLTk5YTM4NzY2MzlkOCIsImlzcyI6IlNwYWxsYSJ9.dMygPahTbVfmdsGtFHwUzu5uH11uf0-4f1Y4UHZT6Ks&uid=636cba6f-7ef9-4bf1-8fff-99a3876639d8&magica=sim",
        "logo": "https://logodownload.org/wp-content/uploads/2014/02/band-logo-0.png"
    },
    "sbt": {
        "name": "SBT",
        "url": "https://www.youtube.com/embed/_3aOntSizW4?autoplay=1",
        "logo": "https://logodownload.org/wp-content/uploads/2013/12/sbt-logo-0-2048x2048.png",
        "type": "youtube"
    },
    "record-news": {
        "name": "Record News",
        "url": "https://www.youtube.com/embed/7L_6I_fSrjk?autoplay=1",
        "logo": "https://logodownload.org/wp-content/uploads/2013/12/record-tv-logo.png",
        "type": "youtube"
    },
    "tv-aparecida": {
        "name": "TV Aparecida",
        "url": "https://www.youtube.com/embed/4CAmwaFJo6k?autoplay=1",
        "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnMtIF9UjvllUKFACrnNZSKCt6qNfI_oBLsA&s",
        "type": "youtube"
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
        body { font-family: sans-serif; background: #000; color: white; margin: 0; display: flex; overflow: hidden; height: 100vh; }
        
        /* Sidebar com largura variável */
        #sidebar { 
            width: 250px; background: #1f1f1f; height: 100vh; overflow-y: auto; 
            border-right: 1px solid #333; transition: width 0.3s ease;
            display: flex; flex-direction: column; flex-shrink: 0;
        }
        
        /* Estado encolhido */
        #sidebar.collapsed { width: 80px; padding: 10px; }
        #sidebar.collapsed h2, #sidebar.collapsed span { display: none; }
        #sidebar.collapsed .channel-item { justify-content: center; padding: 10px 0; }
        #sidebar.collapsed .channel-item img { margin-right: 0; }

        /* Cabeçalho do Menu */
        .sidebar-header { padding: 15px; display: flex; align-items: center; justify-content: space-between; }
        #toggle-btn { background: none; border: none; color: #00d1b2; font-size: 1.5rem; cursor: pointer; padding: 5px; }

        h2 { font-size: 1.1rem; color: #00d1b2; margin: 0; }

        .channel-list { padding: 10px; flex-grow: 1; }

        .channel-item { 
            display: flex; align-items: center; padding: 10px; cursor: pointer; 
            border-radius: 8px; transition: 0.3s; margin-bottom: 10px; 
            text-decoration: none; color: white; background: #2a2a2a; overflow: hidden;
        }
        .channel-item:hover { background: #333; }
        .channel-item img { width: 40px; height: 40px; object-fit: contain; margin-right: 15px; background: white; border-radius: 4px; padding: 2px; flex-shrink: 0; }

        #player-container { flex-grow: 1; background: #000; height: 100vh; position: relative; }
        
        iframe { width: 100%; height: 100%; border: none; }
        
        .no-selection { display: flex; justify-content: center; align-items: center; height: 100%; color: #666; text-align: center; }

        /* Ajuste para mobile */
        @media (max-width: 600px) {
            #sidebar.collapsed { width: 0; padding: 0; border: none; }
        }
    </style>
</head>
<body>
    <div id="sidebar">
        <div class="sidebar-header">
            <h2>Canais</h2>
            <button id="toggle-btn" onclick="toggleMenu()">☰</button>
        </div>
        
        <div class="channel-list">
            {% for id, info in channels.items() %}
            <a href="/?ch={{ id }}" class="channel-item" title="{{ info.name }}">
                <img src="{{ info.logo }}" alt="{{ info.name }}">
                <span>{{ info.name }}</span>
            </a>
            {% endfor %}
        </div>
    </div>

    <div id="player-container">
        {% if current_channel %}
            {% if current_channel.type == 'youtube' %}
                <iframe src="{{ current_channel.url|safe }}" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            {% else %}
                <iframe src="https://hlsplayer.net/embed?type=m3u8&src={{ current_channel.url|safe }}" allowfullscreen></iframe>
            {% endif %}
        {% else %}
            <div class="no-selection">
                <p>Selecione um canal para assistir.</p>
            </div>
        {% endif %}
    </div>

    <script>
        function toggleMenu() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('collapsed');
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    channel_id = request.args.get('ch')
    current_channel = CHANNELS.get(channel_id)
    return render_template_string(HTML_TEMPLATE, channels=CHANNELS, current_channel=current_channel)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)