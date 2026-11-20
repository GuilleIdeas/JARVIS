/**
 * JARVIS - CORE INTERACTIVITY ENGINE (PREMIUM VERSION)
 * Estética: Vision & Iron Man HUD
 * Objetivo: Centro de Mando Global Profesional y Robusto
 */

const AppState = {
    messages: [],
    activeDirectors: [],
    isRecording: false,
    currentModel: 'nvidia/nemotron-3-ultra',
    ws: null,
    reconnectAttempts: 0,
    controllers: {},
    activeDivision: 'div_01_jarvis'
};

const DIVISIONS = [
    { id: 'div_01_jarvis', name: 'JARVIS', icon: 'hub', color: '#00F3FF', description: 'Sala Privada y Núcleo de Mando' },
    { id: 'div_02_mundo', name: 'MUNDO', icon: 'public', color: '#42A5F5', description: 'Vigilancia Global y Telemetría' },
    { id: 'div_03_consejo', name: 'CONSEJO', icon: 'groups', color: '#B388FF', description: 'Sala de Situación Estratégica' },
    { id: 'div_04_investigacion', name: 'INVESTIGACIÓN', icon: 'search', color: '#FFD54F', description: 'OSINT Interconectado' },
    { id: 'div_05_seguridad', name: 'SEGURIDAD', icon: 'shield', color: '#FF5252', description: 'Blindaje Integral y OpSec' },
    { id: 'div_06_juridico', name: 'JURÍDICO', icon: 'gavel', color: '#66BB6A', description: 'Expertiz Legal Global' },
    { id: 'div_07_finanzas', name: 'FINANZAS', icon: 'account_balance', color: '#4CAF50', description: 'Hub Financiero y Trading Algorítmico' },
    { id: 'div_08_fabrica', name: 'FÁBRICA', icon: 'precision_manufacturing', color: '#FFA726', description: 'Ingeniería de Software Autónoma' },
    { id: 'div_09_negocios', name: 'NEGOCIOS', icon: 'business_center', color: '#7986CB', description: 'Gestión Ejecutiva y E-Commerce' },
    { id: 'div_10_marketing', name: 'MARKETING', icon: 'campaign', color: '#EC407A', description: 'Estrategia de Marca y Cultura' },
    { id: 'div_11_ciencia', name: 'CIENCIA', icon: 'science', color: '#26C6DA', description: 'Laboratorio de I+D y Patrones' },
    { id: 'div_12_cerebro', name: 'CEREBRO', icon: 'psychology', color: '#AB47BC', description: 'Graphify Visual Interconectado' },
];

class WebSocketClient {
    constructor(state) {
        this.state = state;
        this.ws = null;
    }

    async connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('[JARVIS] Connection Established');
            this.state.reconnectAttempts = 0;
            this.sendSystemMessage('Sincronización con el núcleo completada. Sistemas operativos.');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (e) {
                console.error('[JARVIS] Error parsing message:', e);
            }
        };

        this.ws.onclose = () => {
            console.log('[JARVIS] Connection Lost');
            this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
            console.error('[JARVIS] Socket Error:', error);
        };
    }

    handleMessage(data) {
        switch (data.type) {
            case 'chat_response':
                this.appendMessage('assistant', data.content);
                break;
            case 'system_alert':
                this.pushIntelligenceFeed(data.msg, data.level || 'info');
                break;
            case 'tactical_response':
                this.pushIntelligenceFeed(`Táctico: ${data.response}`, 'warn');
                break;
            default:
                console.log('[JARVIS] Data received:', data);
        }
    }

    attemptReconnect() {
        if (this.state.reconnectAttempts < 5) {
            this.state.reconnectAttempts++;
            setTimeout(() => this.connect(), 5000);
        }
    }

    send(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('[JARVIS] WebSocket is not open. Current state:', this.ws?.readyState);
        }
    }

    sendSystemMessage(msg) {
        this.pushIntelligenceFeed(msg, 'system');
    }

    pushIntelligenceFeed(msg, level = 'info') {
        const feed = document.getElementById('intel-feed');
        if (!feed) return;
        const entry = document.createElement('div');
        const colors = {
            system: 'border-primary-container text-primary-container',
            info: 'border-blue-400 text-blue-400',
            warn: 'border-yellow-400 text-yellow-400',
            error: 'border-red-400 text-red-400'
        };
        entry.className = `p-2 mb-2 text-[10px] font-mono border-l-2 bg-surface-container/50 animate-slide-in ${colors[level] || colors.info}`;
        entry.innerHTML = `<span class="opacity-50">[${new Date().toLocaleTimeString()}]</span> ${msg}`;
        feed.prepend(entry);
    }

    appendMessage(role, content) {
        const chat = document.getElementById('chat-messages');
        if (!chat) return;
        const div = document.createElement('div');
        div.className = `p-3 rounded-lg mb-2 max-w-[80%] ${role === 'user' ? 'bg-primary-container/20 self-end text-right' : 'bg-surface-container self-start border border-outline-variant'} text-sm font-mono`;
        div.innerText = content;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }
}

class DivisionManager {
    constructor(state) {
        this.state = state;
    }

    init() {
        this.renderMenu();
        this.switchDivision(this.state.activeDivision);
    }

    renderMenu() {
        const menu = document.getElementById('divisions-menu');
        if (!menu) return;
        menu.innerHTML = DIVISIONS.map(div => `
            <button class="w-full flex items-center gap-3 p-3 rounded-lg transition-all duration-200 group ${this.state.activeDivision === div.id ? 'bg-primary-container/10 text-primary border-l-2 border-primary-container' : 'text-on-surface-variant hover:bg-surface-container hover:text-primary'}" 
                    onclick="JARVIS.controllers.divisionManager.switchDivision('${div.id}')">
                <span class="material-symbols-outlined transition-transform group-hover:scale-110" style="color: ${div.color}">${div.icon}</span>
                <span class="hidden lg:block text-xs font-medium tracking-wide uppercase">${div.name}</span>
            </button>
        `).join('');
    }

    switchDivision(divId) {
        this.state.activeDivision = divId;
        const div = DIVISIONS.find(d => d.id === divId);
        if (!div) return;

        document.getElementById('active-division-icon').className = 'material-symbols-outlined';
        document.getElementById('active-division-icon').innerText = div.icon;
        document.getElementById('active-division-icon').style.color = div.color;
        document.getElementById('active-division-title').innerText = div.name;

        this.renderMenu();
        this.renderDivisionContent(div);
    }

    renderDivisionContent(div) {
        const content = document.getElementById('division-content');
        if (div.id === 'div_01_jarvis') {
            this.renderJarvisChat();
            return;
        }

        content.innerHTML = `
            <div class="h-full w-full flex flex-col animate-slide-in">
                <div class="flex items-center justify-between mb-6 border-b border-outline-variant pb-4">
                    <div>
                        <h3 class="text-2xl font-display text-primary" style="text-shadow: 0 0 10px ${div.color}66">${div.name}</h3>
                        <p class="text-xs font-mono text-outline-variant uppercase tracking-widest">${div.description}</p>
                    </div>
                    <div class="flex gap-3">
                        <div class="px-3 py-1 rounded border border-primary-container/30 text-[10px] font-mono text-primary-container animate-pulse">
                            STATUS: OPERATIONAL
                        </div>
                        <button class="p-2 rounded bg-surface-container border border-outline-variant text-primary-container hover:border-primary-container transition-all">
                            <span class="material-symbols-outlined text-sm">settings</span>
                        </button>
                    </div>
                </div>
                <div class="flex-1 grid grid-cols-12 gap-4 overflow-hidden">
                    <div class="col-span-8 flex flex-col gap-4">
                        <div class="flex-1 bg-surface-container/30 border border-outline-variant rounded-xl p-4 relative overflow-hidden">
                            <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(${div.color} 1px, transparent 1px); background-size: 20px 20px;"></div>
                            <div class="relative z-10 h-full flex flex-col">
                                <div class="flex items-center justify-between mb-4">
                                    <span class="text-[10px] font-mono text-outline-variant uppercase tracking-tighter">Consola de Operaciones Tácticas</span>
                                    <span class="material-symbols-outlined text-xs text-outline-variant">expand_more</span>
                                </div>
                                <div class="flex-1 bg-black/40 border border-outline-variant rounded p-3 font-mono text-xs text-on-surface overflow-y-auto custom-scrollbar">
                                    <div class="text-primary-container mb-2">> Inicializando protocolos de ${div.name}...</div>
                                    <div class="text-outline-variant">> Cargando módulos de inteligencia... [OK]</div>
                                    <div class="text-outline-variant">> Estableciendo enlace con el CORE... [OK]</div>
                                    <div class="text-primary mt-4 animate-pulse">SISTEMA LISTO. ESPERANDO DIRECTIVAS DEL COMANDANTE...</div>
                                </div>
                            </div>
                        </div>
                        <div class="h-1/3 grid grid-cols-3 gap-4">
                            <div class="bg-surface-container/50 border border-outline-variant rounded-xl p-3">
                                <span class="text-[10px] font-mono text-outline-variant uppercase">Carga de Procesamiento</span>
                                <div class="mt-2 h-1.5 w-full bg-black/50 rounded-full overflow-hidden">
                                    <div class="h-full bg-primary-container w-1/3 animate-pulse" style="background-color: ${div.color}"></div>
                                </div>
                            </div>
                            <div class="bg-surface-container/50 border border-outline-variant rounded-xl p-3">
                                <span class="text-[10px] font-mono text-outline-variant uppercase">Sincronización de Datos</span>
                                <div class="mt-2 h-1.5 w-full bg-black/50 rounded-full overflow-hidden">
                                    <div class="h-full bg-primary-container w-2/3 animate-pulse" style="background-color: ${div.color}"></div>
                                </div>
                            </div>
                            <div class="bg-surface-container/50 border border-outline-variant rounded-xl p-3">
                                <span class="text-[10px] font-mono text-outline-variant uppercase">Integridad del Nodo</span>
                                <div class="mt-2 text-xs font-mono text-primary-container">99.9% STABLE</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-span-4 bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex flex-col overflow-hidden">
                        <h4 class="text-xs font-mono text-primary uppercase border-b border-outline-variant pb-2 mb-4 flex items-center gap-2">
                            <span class="material-symbols-outlined text-sm animate-pulse">radar</span> Intelligence Feed
                        </h4>
                        <div id="intel-feed" class="flex-1 overflow-y-auto custom-scrollbar pr-2">
                            <!-- Logs dinámicos -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.pushIntelligenceFeed(`Acceso concedido a División ${div.name}.`, 'system');
    }

    renderJarvisChat() {
        const content = document.getElementById('division-content');
        content.innerHTML = `
            <div class="h-full w-full flex gap-4 animate-slide-in">
                <div class="w-1/3 flex flex-col gap-4">
                    <div class="flex-1 bg-surface-container/20 border border-outline-variant rounded-2xl relative overflow-hidden flex items-center justify-center">
                        <div class="absolute inset-0 opacity-20" style="background: radial-gradient(circle at center, #00F3FF 0%, transparent 70%);"></div>
                        <div class="relative z-10 flex flex-col items-center">
                            <div class="w-48 h-48 rounded-full border-4 border-primary-container shadow-[0_0_50px_#00F3FF] flex items-center justify-center animate-pulse">
                                <div class="w-40 h-40 rounded-full border-2 border-dashed border-primary-container/50 animate-spin-slow flex items-center justify-center">
                                    <span class="material-symbols-outlined text-6xl text-primary-container">face</span>
                                </div>
                            </div>
                            <h3 class="mt-6 font-display text-primary tracking-widest uppercase text-sm">Jarvis Core Active</h3>
                            <div class="flex gap-1 mt-2">
                                <div class="w-1 h-1 bg-primary-container rounded-full animate-bounce"></div>
                                <div class="w-1 h-1 bg-primary-container rounded-full animate-bounce [animation-delay:0.2s]"></div>
                                <div class="w-1 h-1 bg-primary-container rounded-full animate-bounce [animation-delay:0.4s]"></div>
                            </div>
                        </div>
                    </div>
                    <div class="h-1/3 bg-surface-container/50 border border-outline-variant rounded-2xl p-4">
                        <h4 class="text-[10px] font-mono text-outline-variant uppercase mb-2">Estado de Conexión</h4>
                        <div class="space-y-2">
                            <div class="flex justify-between text-xs font-mono"><span>Nvidia Build:</span> <span class="text-green-400">ONLINE</span></div>
                            <div class="flex justify-between text-xs font-mono"><span>OpenRouter:</span> <span class="text-green-400">READY</span></div>
                            <div class="flex justify-between text-xs font-mono"><span>Graphify:</span> <span class="text-primary-container animate-pulse">SYNCING</span></div>
                        </div>
                    </div>
                </div>
                <div class="flex-1 flex flex-col bg-surface-container/30 border border-outline-variant rounded-2xl overflow-hidden relative">
                    <div class="p-4 border-b border-outline-variant bg-surface-container/50 flex items-center justify-between">
                        <span class="font-display text-primary text-sm uppercase tracking-widest">Secure Communication Channel</span>
                        <span class="text-[10px] font-mono text-outline-variant">ENCRYPTED AES-256</span>
                    </div>
                    <div id="chat-messages" class="flex-1 overflow-y-auto p-4 flex flex-col gap-3 custom-scrollbar">
                        <div class="bg-surface-container border border-outline-variant p-3 rounded-lg self-start max-w-[80%] text-sm font-mono">
                            Bienvenido, Comandante. Todos los sistemas están operativos. Estoy conectado a las 12 divisiones y Graphify está procesando datos. ¿Cuál es la directiva?
                        </div>
                    </div>
                    <div class="p-4 bg-surface-container-lowest border-t border-outline-variant">
                        <div class="flex items-center gap-3 bg-surface-container p-2 rounded-xl border border-outline-variant focus-within:border-primary-container transition-all">
                            <label class="cursor-pointer p-2 text-outline-variant hover:text-primary-container transition-colors">
                                <span class="material-symbols-outlined">attach_file</span>
                                <input type="file" class="hidden" id="file-upload" multiple onchange="JARVIS.controllers.chat.handleFileUpload(this)">
                            </label>
                            <input type="text" id="chat-input" placeholder="Escriba una directiva..." class="flex-1 bg-transparent outline-none text-sm font-mono text-on-surface">
                            <button id="btn-mic" class="p-2 text-outline-variant hover:text-red-400 transition-colors">
                                <span class="material-symbols-outlined">mic</span>
                            </button>
                            <button id="btn-send" class="bg-primary-container text-on-primary px-4 py-2 rounded-lg font-bold text-xs uppercase hover:bg-primary-fixed transition-all">
                                Enviar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.pushIntelligenceFeed(`Canal de comunicación seguro establecido.`, 'system');
    }

    updateClock() {
        const clock = document.getElementById('global-clock');
        if (clock) clock.innerText = new Date().toISOString().slice(11, 19) + ' UTC';
    }
}

class ChatController {
    constructor(state) {
        this.state = state;
        this.setupListeners();
    }

    setupListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.id === 'btn-send' || e.target.closest('#btn-send')) {
                this.sendMessage();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && document.activeElement && document.activeElement.id === 'chat-input') {
                this.sendMessage();
            }
        });
    }

    appendUserMessage(text) {
        const chat = document.getElementById('chat-messages');
        if (!chat) return;
        const div = document.createElement('div');
        div.className = 'p-3 rounded-lg mb-2 max-w-[80%] bg-primary-container/20 self-end text-right text-sm font-mono';
        div.innerText = text;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        if (!input || !input.value.trim()) return;

        const message = input.value.trim();
        this.appendUserMessage(message);
        input.value = '';

        // INTENTO 1: WebSocket (Rápido)
        if (AppState.controllers.ws && AppState.controllers.ws.ws && AppState.controllers.ws.ws.readyState === WebSocket.OPEN) {
            AppState.controllers.ws.send({
                type: 'chat_request',
                message: message,
                division: AppState.activeDivision
            });
        } else {
            console.warn('[JARVIS] WebSocket no disponible, usando Fallback HTTP API...');
            // INTENTO 2: HTTP API (Respaldo seguro)
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        model: AppState.currentModel,
                        context: AppState.activeDivision
                    })
                });
                const data = await response.json();
                this.appendAssistantMessage(data.executive_summary);
            } catch (e) {
                console.error('[JARVIS] Fallo crítico en ambos canales:', e);
                this.appendAssistantMessage('Error crítico: No se pudo establecer comunicación con el núcleo. Verifique el servidor.');
            }
        }
    }

    appendAssistantMessage(text) {
        const chat = document.getElementById('chat-messages');
        if (!chat) return;
        const div = document.createElement('div');
        div.className = 'p-3 rounded-lg mb-2 max-w-[80%] bg-surface-container self-start text-left text-sm font-mono border border-primary-container/20';
        div.innerText = text;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }


    handleFileUpload(input) {
        const files = input.files;
        if (!files.length) return;
        for (let file of files) {
            this.appendUserMessage(`Archivo adjunto: ${file.name}`);
            AppState.controllers.ws.send({
                type: 'file_upload',
                fileName: file.name,
                fileSize: file.size
            });
        }
    }

    init() {
        console.log('[JARVIS] Chat Controller initialized');
    }
}

async function init() {
    AppState.controllers.ws = new WebSocketClient(AppState);
    AppState.controllers.divisionManager = new DivisionManager(AppState);
    AppState.controllers.chat = new ChatController(AppState);
    
    await AppState.controllers.ws.connect();
    AppState.controllers.divisionManager.init();
    AppState.controllers.chat.init();
    
    setupGlobalListeners();
    setupTacticalCommand();
    
    setInterval(() => AppState.controllers.divisionManager.updateClock(), 1000);
    AppState.controllers.divisionManager.updateClock();
}

function setupGlobalListeners() {
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('jarvis-command-input')?.focus();
        }
    });
}

function setupTacticalCommand() {
    const tacticalInput = document.getElementById('jarvis-command-input');
    const tacticalBtn = document.getElementById('btn-send-tactical');
    if (tacticalBtn && tacticalInput) {
        tacticalBtn.addEventListener('click', () => {
            const cmd = tacticalInput.value.trim();
            if (cmd && AppState.controllers.ws) {
                AppState.controllers.ws.send({ type: 'tactical_command', command: cmd });
                tacticalInput.value = '';
            }
        });
        tacticalInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') tacticalBtn.click(); });
    }
}

window.JARVIS = AppState;
if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
export { AppState, init };
