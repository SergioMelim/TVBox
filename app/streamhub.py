from flask import Flask, render_template_string, request, jsonify, Response, stream_with_context
import requests

app = Flask(__name__)

# --- PROXY DE VÍDEO (Ponte de sinal) ---
@app.route("/proxy_video")
def proxy_video():
    video_url = request.args.get('url')
    if not video_url: return "URL inválida", 400
    
    def generate():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) VLC/3.0.18',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        try:
            with requests.get(video_url, headers=headers, stream=True, timeout=30) as r:
                for chunk in r.iter_content(chunk_size=1024*256):
                    if chunk: yield chunk
        except Exception as e:
            print(f"Erro no Proxy: {e}")

    # TV/Live costumam ser .ts (MPEG-TS), Filmes/Séries costumam ser MP4/MKV
    mime = "video/mp2t" if "/live/" in video_url or video_url.endswith(".ts") else "video/mp4"
    return Response(stream_with_context(generate()), content_type=mime)

# --- API XTREAM ---
@app.route("/api/xtream")
def api_xtream():
    dns = request.args.get('dns')
    user = request.args.get('user')
    password = request.args.get('pass')
    action = request.args.get('action')
    series_id = request.args.get('series_id')
    cat_id = request.args.get('cat_id')
    
    url = f"{dns}/player_api.php?username={user}&password={password}&action={action}"
    if cat_id: url += f"&category_id={cat_id}"
    if series_id: url += f"&series_id={series_id}"
    
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        if action == "get_series_info":
            print(f"--- DEBUG SÉRIE {series_id} ---")
            print(f"Chaves no JSON: {list(data.keys())}")
        return jsonify(data)
    except: return jsonify([])

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>StreamHub Pro | Proceder Digital</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/mpegts.js@latest/dist/mpegts.min.js"></script>
    <style>
        :root { --bg: #05070a; --card: #12161f; --accent: #00d1b2; --text: #ffffff; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; height: 100vh; overflow: hidden; }
        .screen { display: none; height: 100vh; width: 100vw; flex-direction: row; }
        #home-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; background: radial-gradient(circle, #12161f 0%, #05070a 100%); }
        .grid-menu { display: grid; grid-template-columns: repeat(2, 220px); gap: 25px; }
        .menu-btn { background: var(--card); padding: 40px 20px; border-radius: 25px; cursor: pointer; transition: 0.3s; border: 2px solid transparent; text-align: center; }
        .menu-btn:hover { border-color: var(--accent); transform: translateY(-10px); background: #1c2331; }
        .menu-btn i { font-size: 3.5rem; color: var(--accent); margin-bottom: 15px; display: block; }
        #sidebar { width: 350px; background: #0d1117; border-right: 1px solid #232a35; overflow-y: auto; }
        .sidebar-header { padding: 25px; background: var(--accent); color: #000; font-weight: 800; cursor: pointer; }
        #config-screen { display: none; flex-direction: column; align-items: center; justify-content: center; }
        .config-box { background: var(--card); padding: 40px; border-radius: 30px; width: 400px; }
        input { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #333; background: #05070a; color: white; margin-bottom: 15px; box-sizing: border-box; }
        #player-area { flex-grow: 1; background: #000; display: flex; align-items: center; justify-content: center; }
        video { width: 100%; height: 100%; }
        .item-list { padding: 15px; border-bottom: 1px solid #1a1e24; cursor: pointer; display: flex; align-items: center; gap: 15px; }
        .season-title { padding: 10px 20px; background: #000; color: var(--accent); font-weight: bold; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
        .ep-list { padding: 12px 15px 12px 40px; border-bottom: 1px solid #1a1e24; font-size: 0.85rem; cursor: pointer; color: #aaa; }
        .ep-list:hover { color: var(--accent); background: #12161f; }
    </style>
</head>
<body>
    <div id="home-screen" class="screen" style="display: flex; flex-direction: column;">
        <h1 style="letter-spacing: 8px; margin-bottom: 40px;">STREAM<span style="color:var(--accent)">HUB</span></h1>
        <div class="grid-menu">
            <div class="menu-btn" onclick="openApp('live')"><i class="fas fa-tv"></i><span>TV AO VIVO</span></div>
            <div class="menu-btn" onclick="openApp('movies')"><i class="fas fa-film"></i><span>FILMES</span></div>
            <div class="menu-btn" onclick="openApp('series')"><i class="fas fa-layer-group"></i><span>SÉRIES</span></div>
            <div class="menu-btn" onclick="showConfig()"><i class="fas fa-tools"></i><span>CONFIG</span></div>
        </div>
    </div>

    <div id="config-screen" class="screen">
        <div class="config-box">
            <h2 style="color:var(--accent)">Configurações</h2>
            <input type="text" id="cfg-dns" placeholder="Servidor (Ex: http://dns.com:80)">
            <input type="text" id="cfg-user" placeholder="Usuário">
            <input type="password" id="cfg-pass" placeholder="Senha">
            <button class="menu-btn" style="width:100%;" onclick="saveConfig()">SALVAR</button>
            <p onclick="hideAllAndShow('home-screen')" style="text-align:center; cursor:pointer; opacity:0.5; margin-top:20px;">Voltar</p>
        </div>
    </div>

    <div id="app-interface" class="screen">
        <aside id="sidebar">
            <div class="sidebar-header" onclick="hideAllAndShow('home-screen')"><i class="fas fa-chevron-left"></i> VOLTAR</div>
            <div id="list-content"></div>
        </aside>
        <main id="player-area">
            <video id="videoElement" controls autoplay></video>
        </main>
    </div>

    <script>
        let player = null;

        function hideAllAndShow(id) {
            document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
            document.getElementById(id).style.display = (id === 'app-interface' ? 'flex' : 'flex');
            if (player) { player.destroy(); player = null; }
            document.getElementById('videoElement').src = "";
        }

        function showConfig() {
            document.getElementById('cfg-dns').value = localStorage.getItem('xt-dns') || '';
            document.getElementById('cfg-user').value = localStorage.getItem('xt-user') || '';
            document.getElementById('cfg-pass').value = localStorage.getItem('xt-pass') || '';
            hideAllAndShow('config-screen');
        }

        function saveConfig() {
            localStorage.setItem('xt-dns', document.getElementById('cfg-dns').value);
            localStorage.setItem('xt-user', document.getElementById('cfg-user').value);
            localStorage.setItem('xt-pass', document.getElementById('cfg-pass').value);
            alert("Salvo!"); hideAllAndShow('home-screen');
        }

        function openApp(mode) {
            if(!localStorage.getItem('xt-dns')) return showConfig();
            hideAllAndShow('app-interface');
            loadCategories(mode);
        }

        async function loadCategories(mode) {
            const dns = localStorage.getItem('xt-dns'), user = localStorage.getItem('xt-user'), pass = localStorage.getItem('xt-pass');
            const action = mode === 'live' ? 'get_live_categories' : (mode === 'movies' ? 'get_vod_categories' : 'get_series_categories');
            const r = await fetch(`/api/xtream?dns=${encodeURIComponent(dns)}&user=${user}&pass=${pass}&action=${action}`);
            const cats = await r.json();
            const list = document.getElementById('list-content');
            list.innerHTML = '';
            cats.forEach(c => {
                const div = document.createElement('div');
                div.className = 'item-list';
                div.innerHTML = `<i class="fas fa-folder" style="color:#ffcc00"></i> <span>${c.category_name}</span>`;
                div.onclick = () => loadItems(mode, c.category_id);
                list.appendChild(div);
            });
        }

        async function loadItems(mode, catId) {
            const dns = localStorage.getItem('xt-dns'), user = localStorage.getItem('xt-user'), pass = localStorage.getItem('xt-pass');
            const action = mode === 'live' ? 'get_live_streams' : (mode === 'movies' ? 'get_vod_streams' : 'get_series');
            const r = await fetch(`/api/xtream?dns=${encodeURIComponent(dns)}&user=${user}&pass=${pass}&action=${action}&cat_id=${catId}`);
            const items = await r.json();
            const list = document.getElementById('list-content');
            list.innerHTML = `<div class="sidebar-header" style="background:#1a202c; color:white;" onclick="loadCategories('${mode}')"><i class="fas fa-arrow-left"></i> VOLTAR</div>`;
            
            items.forEach(i => {
                const div = document.createElement('div');
                div.className = 'item-list';
                const thumb = i.stream_icon || i.cover || 'https://cdn-icons-png.flaticon.com/512/716/716429.png';
                div.innerHTML = `<img src="${thumb}" style="width:40px; height:50px; border-radius:5px; object-fit:cover"> <span>${i.name || i.title}</span>`;
                if (mode === 'series') div.onclick = () => loadEpisodes(i.series_id || i.id, div);
                else div.onclick = () => playMedia(`${dns}/${mode === 'live' ? 'live' : 'movie'}/${user}/${pass}/${i.stream_id}.${i.container_extension || 'ts'}`, mode);
                list.appendChild(div);
            });
        }

        async function loadEpisodes(seriesId, parentDiv) {
            const dns = localStorage.getItem('xt-dns'), user = localStorage.getItem('xt-user'), pass = localStorage.getItem('xt-pass');
            const nextEl = parentDiv.nextElementSibling;
            if (nextEl && nextEl.classList.contains('ep-container')) { nextEl.remove(); return; }

            const r = await fetch(`/api/xtream?dns=${encodeURIComponent(dns)}&user=${user}&pass=${pass}&action=get_series_info&series_id=${seriesId}`);
            const data = await r.json();
            
            const epContainer = document.createElement('div');
            epContainer.className = 'ep-container';
            const epData = data.episodes;

            if (epData) {
                // Itera sobre as temporadas (keys do dicionário)
                Object.keys(epData).sort((a,b) => a-b).forEach(seasonKey => {
                    const seasonDiv = document.createElement('div');
                    seasonDiv.className = 'season-title';
                    seasonDiv.innerText = `Temporada ${seasonKey}`;
                    epContainer.appendChild(seasonDiv);

                    const episodes = epData[seasonKey];
                    // Transforma em array se não for
                    const epArray = Array.isArray(episodes) ? episodes : Object.values(episodes);
                    
                    epArray.forEach(ep => {
                        const epDiv = document.createElement('div');
                        epDiv.className = 'ep-list';
                        epDiv.innerText = `E${ep.episode_num || '?'} - ${ep.title || 'Episódio'}`;
                        
                        // ID do vídeo pode estar em ep.id ou ep.stream_id
                        const vidId = ep.id || ep.stream_id;
                        const ext = ep.container_extension || 'mp4';
                        const url = `${dns}/series/${user}/${pass}/${vidId}.${ext}`;
                        
                        epDiv.onclick = (e) => { e.stopPropagation(); playMedia(url, 'vod'); };
                        epContainer.appendChild(epDiv);
                    });
                });
            }
            parentDiv.after(epContainer);
        }

        function playMedia(url, mode) {
            const video = document.getElementById('videoElement');
            const proxyUrl = window.location.origin + '/proxy_video?url=' + encodeURIComponent(url);
            if (player) { player.destroy(); player = null; }
            
            if (mode === 'live' || url.includes('.ts')) {
                player = mpegts.createPlayer({ type: 'mse', isLive: true, url: proxyUrl });
                player.attachMediaElement(video); player.load(); player.play();
            } else {
                video.src = proxyUrl;
                video.play().catch(e => console.log("Aguardando play."));
            }
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)