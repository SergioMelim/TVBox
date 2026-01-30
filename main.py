from flask import Flask, render_template_string, request, jsonify
import yt_dlp

app = Flask(__name__)

# CONFIGURAÇÃO DE CANAIS
CHANNELS = {
    "band": {
        "name": "Band TV",
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
                        "name": entry.get('title'),
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
    <title>StreamHub | Sinal Comunitário</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0a0c0f;
            --sidebar-bg: #12151a;
            --accent: #00d1b2;
            --card-bg: #1e232b;
            --text-main: #e1e1e1;
            --text-dim: #94a3b8;
        }

        body { font-family: 'Inter', sans-serif; background: var(--bg-dark); color: var(--text-main); margin: 0; display: flex; height: 100vh; overflow: hidden; }

        #sidebar { 
            width: 300px; background: var(--sidebar-bg); border-right: 1px solid #232a35;
            display: flex; flex-direction: column; transition: width 0.3s ease; flex-shrink: 0;
        }
        #sidebar.collapsed { width: 85px; }
        #sidebar.collapsed h2, #sidebar.collapsed span, #sidebar.collapsed .section-header, #sidebar.collapsed #btn-load-caze { display: none; }

        .sidebar-header { padding: 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #232a35; }
        .logo-area { display: flex; align-items: center; gap: 10px; color: var(--accent); font-weight: 800; }

        .section-header { 
            padding: 15px; font-size: 0.75rem; color: var(--accent); 
            text-transform: uppercase; letter-spacing: 1px; cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(255,255,255,0.03); margin-top: 1px;
        }
        .arrow { transition: transform 0.3s; font-size: 0.7rem; color: var(--text-dim); }
        .arrow.open { transform: rotate(180deg); }
        
        .submenu { display: none; padding: 10px; }
        .submenu.show { display: block; }

        .channel-card {
            display: flex; align-items: center; padding: 10px; border-radius: 10px;
            text-decoration: none; color: inherit; transition: 0.2s; margin-bottom: 5px;
            background: transparent;
        }
        .channel-card:hover { background: var(--card-bg); }
        .channel-card.active { background: var(--card-bg); border-left: 3px solid var(--accent); }

        .logo-wrapper {
            width: 36px; height: 36px; background: white; border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            margin-right: 12px; flex-shrink: 0; padding: 3px;
        }
        .logo-wrapper img { max-width: 100%; max-height: 100%; object-fit: contain; }

        .fav-btn { margin-left: auto; color: var(--text-dim); cursor: pointer; font-size: 0.9rem; padding: 5px; }
        .fav-btn.active { color: #ff4757; }

        #btn-load-caze {
            width: 100%; background: #ffcc00; color: #000; border: none;
            padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 10px;
        }

        #main-stage { flex-grow: 1; background: #000; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <aside id="sidebar">
        <div class="sidebar-header">
            <div class="logo-area"><i class="fas fa-satellite-dish"></i><span class="logo-text">STREAMHUB</span></div>
            <i class="fas fa-bars" style="cursor:pointer" onclick="toggleSidebar()"></i>
        </div>
        <div style="overflow-y: auto; flex-grow: 1;">
            <div id="section-favs-header" class="section-header" onclick="toggleAccordion('submenu-favs', this)">
                <span>Favoritos</span><i class="fas fa-chevron-down arrow" id="arrow-submenu-favs"></i>
            </div>
            <div id="submenu-favs" class="submenu"></div>

            <div class="section-header" onclick="toggleAccordion('submenu-open', this)">
                <span>Canais Abertos</span><i class="fas fa-chevron-down arrow" id="arrow-submenu-open"></i>
            </div>
            <div id="submenu-open" class="submenu">
                {% for id, info in channels.items() %}
                <div class="channel-card {{ 'active' if current_id == id else '' }}" id="card-{{ id }}">
                    <a href="/?ch={{ id }}" style="display:flex; align-items:center; flex-grow:1; text-decoration:none; color:inherit;">
                        <div class="logo-wrapper"><img src="{{ info.logo }}"></div>
                        <span class="nav-text">{{ info.name }}</span>
                    </a>
                    <i class="fas fa-heart fav-btn" onclick="toggleFavorite('{{ id }}', '{{ info.name }}', '{{ info.logo }}')"></i>
                </div>
                {% endfor %}
            </div>

            <div class="section-header" onclick="toggleAccordion('submenu-sports', this)">
                <span>Esportes</span><i class="fas fa-chevron-down arrow" id="arrow-submenu-sports"></i>
            </div>
            <div id="submenu-sports" class="submenu">
                <div class="channel-card" onclick="toggleAccordion('caze-items', this)" style="cursor:pointer">
                    <div class="logo-wrapper"><img src="https://logospng.org/wp-content/uploads/caze-tv.png"></div>
                    <span class="nav-text">Cazé TV</span>
                    <i class="fas fa-chevron-down arrow" style="margin-left:auto; font-size:0.6rem"></i>
                </div>
                <div id="caze-items" class="submenu" style="padding-left: 15px; border-left: 1px solid #333; margin-left: 18px;">
                    <button id="btn-load-caze" onclick="loadCaze()">CARREGAR LIVES</button>
                    <div id="caze-list"></div>
                </div>
            </div>
        </div>
    </aside>
    <main id="main-stage">
        {% if current_url %}
            <iframe src="{{ current_url|safe }}" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        {% else %}
            <div style="display:flex; align-items:center; justify-content:center; height:100%; color:#444;">Selecione um canal</div>
        {% endif %}
    </main>

    <script>
        window.onload = function() {
            ['submenu-favs', 'submenu-open', 'submenu-sports', 'caze-items'].forEach(id => {
                if (localStorage.getItem(id) === 'true') {
                    document.getElementById(id).classList.add('show');
                    const arrow = document.getElementById('arrow-' + id);
                    if (arrow) arrow.classList.add('open');
                }
            });
            renderFavorites();
            if(localStorage.getItem('caze-loaded') === 'true') loadCaze();
        };

        function toggleSidebar() { document.getElementById('sidebar').classList.toggle('collapsed'); }

        function toggleAccordion(id, element) {
            const submenu = document.getElementById(id);
            const isShowing = submenu.classList.toggle('show');
            const arrow = element.querySelector('.arrow') || document.getElementById('arrow-' + id);
            if (arrow) arrow.classList.toggle('open');
            localStorage.setItem(id, isShowing);
        }

        function toggleFavorite(id, name, logo) {
            let favs = JSON.parse(localStorage.getItem('favChannels') || '{}');
            favs[id] ? delete favs[id] : favs[id] = { name, logo };
            localStorage.setItem('favChannels', JSON.stringify(favs));
            renderFavorites();
        }

        function renderFavorites() {
            const favs = JSON.parse(localStorage.getItem('favChannels') || '{}');
            const container = document.getElementById('submenu-favs');
            const header = document.getElementById('section-favs-header');
            container.innerHTML = '';
            const keys = Object.keys(favs);
            header.style.display = keys.length ? 'flex' : 'none';
            keys.forEach(id => {
                container.innerHTML += `<div class="channel-card"><a href="/?ch=${id}" style="display:flex; align-items:center; flex-grow:1; text-decoration:none; color:inherit;"><div class="logo-wrapper"><img src="${favs[id].logo}"></div><span class="nav-text">${favs[id].name}</span></a><i class="fas fa-heart fav-btn active" onclick="toggleFavorite('${id}')"></i></div>`;
            });
        }

        async function loadCaze() {
            const list = document.getElementById('caze-list');
            const btn = document.getElementById('btn-load-caze');
            btn.innerText = "BUSCANDO...";
            try {
                const response = await fetch('/get_caze');
                const lives = await response.json();
                list.innerHTML = '';
                lives.forEach(live => {
                    list.innerHTML += `<a href="/?vid=${encodeURIComponent(live.url)}" class="channel-card"><div class="logo-wrapper"><img src="https://logospng.org/wp-content/uploads/caze-tv.png"></div><span class="nav-text" style="font-size:0.7rem">${live.name.substring(0,30)}...</span></a>`;
                });
                btn.style.display = 'none';
                localStorage.setItem('caze-loaded', 'true');
            } catch (e) { btn.innerText = "ERRO AO CARREGAR"; }
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
            current_url = channel.get('url') if channel.get('type') == 'youtube' else f"https://hlsplayer.net/embed?type=m3u8&src={channel.get('url')}"
    elif vid_url:
        current_url = vid_url
    return render_template_string(HTML_TEMPLATE, channels=CHANNELS, current_id=channel_id, current_url=current_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)