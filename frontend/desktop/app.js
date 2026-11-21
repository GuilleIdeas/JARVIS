document.addEventListener('DOMContentLoaded', () => {
    const divisions = [
        "JARVIS", "MUNDO", "CONSEJO", "INVESTIGACIÓN", "SEGURIDAD", 
        "JURÍDICO", "FINANZAS", "FÁBRICA", "NEGOCIOS", "MARKETING", 
        "CIENCIA", "CEREBRO"
    ];

    const navMenu = document.getElementById('nav-menu');
    const moduleContent = document.getElementById('module-content');
    const panelTitle = document.getElementById('panel-title');
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    let currentDivision = "JARVIS";

    divisions.forEach((div, index) => {
        const item = document.createElement('div');
        item.className = 'nav-item';
        item.innerText = `${index + 1}. ${div}`;
        item.onclick = () => selectDivision(div, item);
        navMenu.appendChild(item);
    });

    function selectDivision(div, element) {
        currentDivision = div;
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        element.classList.add('active');
        panelTitle.innerText = `DIVISIÓN ${divisions.indexOf(div) + 1}: ${div}`;
        loadModule(div);
    }

    function loadModule(div) {
        moduleContent.innerHTML = '';
        if (div === "FINANZAS") {
            moduleContent.innerHTML = `
                <div class="sub-tabs">
                    <div class="sub-tab active" onclick="alert('Cargando Macroeconomía...')">FINANZAS</div>
                    <div class="sub-tab" onclick="alert('Conectando puente API Trading...')">TRADING</div>
                </div>
                <div style="padding:20px; color: var(--neon-blue);">
                    Dashboard Financiero Integrado... <br> [Análisis de Activos | Flujos de Capital | Trading Bot Status]
                </div>`;
        } else if (div === "CEREBRO") {
            moduleContent.innerHTML = `
                <div style="position:absolute; top:10px; left:10px; z-index:10; display:flex; gap:10px;">
                    <input type="text" id="node-search" placeholder="Buscar Nodo..." style="background:rgba(0,0,0,0.7); border:1px solid var(--neon-blue); color:white; padding:5px; border-radius:4px;">
                </div>
                <div id="graph-canvas"></div>`;
            initGraph();
        } else {
            moduleContent.innerHTML = `
                <div style="padding:20px; color: var(--neon-blue); text-align:center; margin-top: 50px;">
                    <h2>MÓDULO ${div} ACTIVO</h2>
                    <p>Accediendo a bases de datos y agentes especialistas de la división ${div}...</p>
                </div>`;
        }
    }

    async function initGraph() {
        const response = await fetch('/api/brain/graph');
        const data = await response.json();
        const container = document.getElementById('graph-canvas');
        const graphData = { nodes: new vis.DataSet(data.nodes), edges: new vis.DataSet(data.edges) };
        const options = {
            nodes: { shape: 'dot', size: 16, font: { color: '#e0ffff', size: 14, face: 'Rajdhani' }, borderWidth: 2 },
            edges: { color: { color: '#00f2ff', highlight: '#00ffea' }, width: 2, smooth: { type: 'continuous' } },
            groups: { core: { color: { background: '#ff00ff' }, size: 20 }, div: { color: { background: '#00f2ff' } }, tool: { color: { background: '#0066ff' } } },
            physics: { enabled: true, barnesHut: { gravitationalConstant: -2000 } }
        };
        new vis.Network(container, graphData, options);
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        appendMessage('user', text);
        userInput.value = '';
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, division: currentDivision })
            });
            const data = await response.json();
            appendMessage('jarvis', data.response);
        } catch (e) {
            appendMessage('jarvis', 'Error de conexión con el núcleo central.');
        }
    }

    function appendMessage(role, text) {
        const msg = document.createElement('div');
        msg.className = `message ${role === 'user' ? 'user-msg' : 'jarvis-msg'}`;
        msg.innerText = text;
        chatHistory.appendChild(msg);
        
        // Auto-scroll to bottom on every new message
        chatHistory.scrollTo({
            top: chatHistory.scrollHeight,
            behavior: 'smooth'
        });
    }

    sendBtn.onclick = sendMessage;
    userInput.onkeypress = (e) => { if(e.key === 'Enter') sendMessage(); };
});
