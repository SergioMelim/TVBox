from flask import Flask, render_template_string, request, jsonify
import yt_dlp

app = Flask(__name__)

# DICIONÁRIO DE CANAIS ABERTOS
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

@app.route("/get_caze")
def get_caze():
    ydl_opts = {'quiet': True, 'extract_flat': True, 'playlist_items': '1-8'}
    url_caze = "https://www.youtube.com/@CazeTV/streams"
    lives = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_caze, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    lives.append({
                        "title": entry.get('title'),
                        "url": f"https://www.youtube.com/embed/{entry.get('id')}?autoplay=1"
                    })
                    if len(lives) >= 5: break
    except: pass
    return jsonify(lives)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sinal Digital Comunitário</title>
    <style>
        body { font-family: sans-serif; background: #000; color: white; margin: 0; display: flex; overflow: hidden; height: 100vh; }
        #sidebar { width: 300px; background: #1f1f1f; height: 100vh; overflow-y: auto; border-right: 1px solid #333; transition: width 0.3s ease; display: flex; flex-direction: column; flex-shrink: 0; }
        #sidebar.collapsed { width: 85px; padding: 10px; }
        #sidebar.collapsed h2, #sidebar.collapsed span, #sidebar.collapsed .section-header, #sidebar.collapsed .caze-toggle { display: none; }
        .sidebar-header { padding: 15px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #333; }
        #toggle-btn { background: none; border: none; color: #00d1b2; font-size: 1.5rem; cursor: pointer; }
        .section-header { padding: 12px 15px; font-size: 0.85rem; color: #00d1b2; text-transform: uppercase; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: #252525; margin-top: 2px; }
        .submenu { display: none; padding: 5px 10px; background: #1a1a1a; }
        .submenu.show { display: block; }
        .channel-item { display: flex; align-items: center; padding: 10px; cursor: pointer; border-radius: 8px; transition: 0.3s; margin-bottom: 5px; text-decoration: none; color: white; background: #2a2a2a; }
        .channel-item:hover { background: #333; border-left: 4px solid #00d1b2; }
        .channel-item img { width: 35px; height: 35px; object-fit: contain; margin-right: 12px; background: white; border-radius: 4px; padding: 2px; }
        .caze-toggle { padding: 10px; background: #333; border-radius: 8px; margin-top: 5px; cursor: pointer; display: flex; align-items: center; justify-content: space-between; }
        .caze-toggle img { width: 30px; height: 30px; margin-right: 10px; background: white; border-radius: 4px; padding: 2px;}
        .caze-submenu { display: none; padding-left: 15px; margin-top: 5px; border-left: 1px dashed #444; }
        .caze-submenu.show { display: block; }
        #btn-load { width: 100%; background: #ffcc00; color: black; border: none; padding: 8px; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 5px; font-size: 0.7rem; }
        .arrow { transition: transform 0.3s; font-size: 0.7rem; }
        .arrow.open { transform: rotate(180deg); }
        #player-container { flex-grow: 1; background: #000; height: 100vh; position: relative; }
        iframe { width: 100%; height: 100%; border: none; }
        .no-selection { display: flex; justify-content: center; align-items: center; height: 100%; color: #666; text-align: center; }
    </style>
</head>
<body>
    <div id="sidebar">
        <div class="sidebar-header">
            <h2>Canais</h2>
            <button id="toggle-btn" onclick="toggleMenu()">☰</button>
        </div>
        <div class="channel-list">
            <div class="section-header" onclick="toggleSection('open-channels', this)">
                <span>Canais Abertos</span>
                <span class="arrow" id="arrow-open-channels">▼</span>
            </div>
            <div id="open-channels" class="submenu">
                {% for id, info in channels.items() %}
                <a href="/?ch={{ id }}" class="channel-item">
                    <img src="{{ info.logo }}" alt="{{ info.name }}">
                    <span style="font-size: 0.9rem;">{{ info.name }}</span>
                </a>
                {% endfor %}
            </div>

            <div class="section-header" onclick="toggleSection('sports-channels', this)">
                <span>Esportes</span>
                <span class="arrow" id="arrow-sports-channels">▼</span>
            </div>
            <div id="sports-channels" class="submenu">
                <div class="caze-toggle" onclick="handleCazeClick(this)">
                    <div style="display: flex; align-items: center;">
                        <img src="https://logospng.org/wp-content/uploads/caze-tv.png" alt="CazéTV">
                        <span style="font-size: 0.9rem;">Cazé TV</span>
                    </div>
                    <span class="arrow" id="caze-arrow">▼</span>
                </div>
                <div id="caze-list" class="caze-submenu">
                    <button id="btn-load" onclick="loadCaze(event)">+ CARREGAR LIVES</button>
                    <div id="caze-items"></div>
                </div>
            </div>
        </div>
    </div>

    <div id="player-container">
        {% if current_url %}
            <iframe src="{{ current_url|safe }}" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        {% else %}
            <div class="no-selection"><p>Escolha uma categoria ao lado.</p></div>
        {% endif %}
    </div>

    <script>
        window.onload = function() {
            // Restaura Canais Abertos
            if(localStorage.getItem('open-channels') === 'true') {
                document.getElementById('open-channels').classList.add('show');
                document.getElementById('arrow-open-channels').classList.add('open');
            }
            // Restaura Esportes
            if(localStorage.getItem('sports-channels') === 'true') {
                document.getElementById('sports-channels').classList.add('show');
                document.getElementById('arrow-sports-channels').classList.add('open');
            }
            // Restaura o submenu da CazéTV
            if(localStorage.getItem('caze-list-open') === 'true') {
                document.getElementById('caze-list').classList.add('show');
                document.getElementById('caze-arrow').classList.add('open');
                
                // Se a lista de vídeos já tinha sido carregada antes, carrega de novo automaticamente
                if(localStorage.getItem('caze-loaded') === 'true') {
                    loadCaze();
                }
            }
        };

        function toggleMenu() { document.getElementById('sidebar').classList.toggle('collapsed'); }

        function toggleSection(id, element) {
            const section = document.getElementById(id);
            const arrow = element.querySelector('.arrow');
            const isShowing = section.classList.toggle('show');
            arrow.classList.toggle('open');
            localStorage.setItem(id, isShowing);
        }

        function handleCazeClick(element) {
            const submenu = document.getElementById('caze-list');
            const arrow = document.getElementById('caze-arrow');
            const isShowing = submenu.classList.toggle('show');
            arrow.classList.toggle('open');
            // Salva apenas se o menu está expandido
            localStorage.setItem('caze-list-open', isShowing);
        }

        async function loadCaze(event) {
            if(event) event.stopPropagation();
            const btn = document.getElementById('btn-load');
            const list = document.getElementById('caze-items');
            const cazeLogo = "https://logospng.org/wp-content/uploads/caze-tv.png";
            btn.innerText = "BUSCANDO...";
            
            try {
                const response = await fetch('/get_caze');
                const lives = await response.json();
                list.innerHTML = "";
                lives.forEach(live => {
                    const item = document.createElement('a');
                    item.href = `/?vid=${encodeURIComponent(live.url)}`;
                    item.className = "channel-item";
                    item.innerHTML = `<img src="${cazeLogo}"> <span style="font-size:0.75rem;">${live.title}</span>`;
                    list.appendChild(item);
                });
                btn.style.display = "none";
                // Salva que a programação foi carregada com sucesso
                localStorage.setItem('caze-loaded', 'true');
            } catch (e) { 
                btn.innerText = "ERRO. TENTAR NOVAMENTE?"; 
                localStorage.setItem('caze-loaded', 'false');
            }
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    channel_id = request.args.get('ch')
    vid_url = request.args.get('vid')
    current_url = None
    if channel_id:
        channel = CHANNELS.get(channel_id)
        if channel:
            if channel.get('type') == 'youtube':
                current_url = channel.get('url')
            else:
                current_url = f"https://hlsplayer.net/embed?type=m3u8&src={channel.get('url')}"
    elif vid_url:
        current_url = vid_url
    return render_template_string(HTML_TEMPLATE, channels=CHANNELS, current_url=current_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)