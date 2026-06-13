<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nascondino Pro</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding: 10px;
        }
        h2 {
            color: #fff;
            margin: 10px 0;
            text-shadow: 0 0 10px #ff00ff;
        }
        .info {
            color: #aaa;
            font-size: 12px;
            margin-bottom: 10px;
            text-align: center;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            max-width: 400px;
            width: 100%;
        }
        .cell {
            aspect-ratio: 1;
            border-radius: 12px;
            border: 2px solid #gold;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .cell:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        }
        .cell.disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .cell.found-lion {
            border-color: #ff4444;
            box-shadow: 0 0 20px #ff4444;
        }
        .cell.found-key {
            border-color: #ffd700;
            box-shadow: 0 0 20px #ffd700;
        }
        .cell.found-gift {
            border-color: #ff69b4;
            box-shadow: 0 0 20px #ff69b4;
        }
        .cell.found-user {
            border-color: #00ff88;
            box-shadow: 0 0 20px #00ff88;
        }
        .cell-number {
            position: absolute;
            top: 4px;
            left: 4px;
            background: rgba(0,0,0,0.7);
            color: #fff;
            padding: 2px 6px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: bold;
        }
        .cell-icon {
            font-size: 32px;
            z-index: 2;
        }
        .cell-label {
            position: absolute;
            bottom: 2px;
            background: rgba(0,0,0,0.8);
            color: #fff;
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 90%;
        }
        /* Sfondo porta magica */
        .door-bg {
            background-image: url(https://postimg.cc/BP8xMH5n); /* <-- CAMBIA CON URL REALE */
            background-size: cover;
            background-position: center;
        }
        .door-bg::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.3);
            z-index: 1;
        }
    </style>
</head>
<body>
    <h2 id="title">🚪 NASCONDINO PRO</h2>
    <div class="info" id="info">Caricamento...</div>
    <div class="grid" id="grid"></div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        
        // URL della tua immagine porta - CAMBIA QUI!
        const PORTA_URL = "https://i.imgur.com/TUO_URL_PORTA.jpg"; // <-- METTI URL REALE
        
        // Parse dati dal bot
        const urlParams = new URLSearchParams(window.location.search);
        const gameData = JSON.parse(urlParams.get('data') || '{}');
        
        const grid = document.getElementById('grid');
        const title = document.getElementById('title');
        const info = document.getElementById('info');
        
        let selectedPort = null;
        
        function renderGrid() {
            grid.innerHTML = '';
            
            if (gameData.phase === 'hide') {
                title.textContent = '🚪 SCEGLI DOVE NASCONDERTI';
                info.textContent = `Round ${gameData.round} | Sei un NASCOSTO`;
            } else {
                title.textContent = '🔍 CERCA I NASCOSTI';
                info.textContent = `Round ${gameData.round} | Tentativi: ${gameData.attempts_left?.[tg.initDataUnsafe?.user?.id] || '?'}`;
            }
            
            for (let i = 0; i < gameData.ports; i++) {
                const cell = document.createElement('div');
                cell.className = 'cell door-bg';
                cell.dataset.port = i;
                
                // Numero porta
                const num = document.createElement('div');
                num.className = 'cell-number';
                num.textContent = i;
                cell.appendChild(num);
                
                // Controlla se già usata
                if (gameData.used_ports?.includes(i)) {
                    cell.classList.add('disabled');
                    
                    // Determina cosa c'era qui
                    let icon = '';
                    let label = '';
                    let foundClass = '';
                    
                    if (gameData.found?.includes(i)) {
                        // Trovato utente - cerca nome
                        const hiddenPos = gameData.hidden_positions || {};
                        for (let [uid, port] of Object.entries(hiddenPos)) {
                            if (port == i) {
                                icon = '👤';
                                label = 'Trovato!';
                                foundClass = 'found-user';
                                break;
                            }
                        }
                    }
                    
                    if (i === gameData.key_port && gameData.key_found) {
                        icon = '🗝️';
                        label = 'CHIAVE!';
                        foundClass = 'found-key';
                    }
                    if (i === gameData.gift_port && gameData.gift_found) {
                        icon = '🎁';
                        label = 'REGALO!';
                        foundClass = 'found-gift';
                    }
                    if (i === gameData.lion_port && gameData.lion_found) {
                        icon = '🦁';
                        label = 'LEONE!';
                        foundClass = 'found-lion';
                    }
                    
                    if (foundClass) cell.classList.add(foundClass);
                    if (icon) {
                        const ic = document.createElement('div');
                        ic.className = 'cell-icon';
                        ic.textContent = icon;
                        cell.appendChild(ic);
                    }
                    if (label) {
                        const lb = document.createElement('div');
                        lb.className = 'cell-label';
                        lb.textContent = label;
                        cell.appendChild(lb);
                    }
                }
                
                cell.onclick = () => handleClick(i, cell);
                grid.appendChild(cell);
            }
        }
        
        function handleClick(port, cell) {
            if (cell.classList.contains('disabled')) return;
            
            if (gameData.phase === 'hide') {
                tg.sendData(JSON.stringify({
                    action: 'hide',
                    port: port
                }));
                cell.classList.add('disabled');
                cell.style.background = 'linear-gradient(135deg, #00ff88, #00cc66)';
                const ok = document.createElement('div');
                ok.className = 'cell-icon';
                ok.textContent = '✅';
                cell.appendChild(ok);
            } else {
                // Fase seek
                const attempts = gameData.attempts_left?.[tg.initDataUnsafe?.user?.id] || 0;
                if (attempts <= 0) {
                    tg.showAlert('😴 Tentativi finiti!');
                    return;
                }
                
                tg.sendData(JSON.stringify({
                    action: 'seek',
                    port: port
                }));
                cell.classList.add('disabled');
            }
        }
        
        renderGrid();
        
        // Ricevi risposta dal bot
        tg.onEvent('webAppDataReceived', (data) => {
            const response = JSON.parse(data);
            if (response.alert) {
                tg.showAlert(response.alert);
            }
        });
    </script>
</body>
</html>