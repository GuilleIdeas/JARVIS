// JARVIS ECC Frontend - Interactivity (Single file)

const AppState = { messages: [], activeDirectors: [], isRecording: false, currentModel: 'nvidia/nemotron-3-ultra', ws: null, reconnectAttempts: 0, controllers: {} };

class WebSocketClient {
  constructor(state) { this.state = state; this.ws = null; }
  async connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    this.ws = new WebSocket(wsUrl);
    this.ws.onopen = () => { console.log('[JARVIS] WebSocket conectado'); this.state.reconnectAttempts = 0; };
    this.ws.onmessage = (event) => { const data = JSON.parse(event.data); this.handleMessage(data); };
    this.ws.onclose = () => { console.log('[JARVIS] WebSocket desconectado'); this.attemptReconnect(); };
    this.ws.onerror = (error) => { console.error('[JARVIS] WebSocket error:', error); };
  }
  handleMessage(data) {
    switch (data.type) {
      case 'chat_response': this.appendMessage('assistant', data.content, data.metadata); this.updateExecutiveResponse(data.executive_summary); this.updateActiveDirectors(data.active_directors); break;
      case 'stream_chunk': this.appendStreamChunk(data.content); break;
      case 'system_metrics': this.updateSystemMetrics(data.metrics); break;
      case 'financial_tick': this.updateFinancialTicker(data.ticker); break;
      case 'trading_log': this.appendTradingLog(data.log); break;
      case 'apps_log': this.appendAppsLog(data.log); break;
      case 'opsec_log': this.appendOpsecLog(data.log); break;
      case 'tactical_response': this.appendTacticalResponse(data.response); break;
    }
  }
  attemptReconnect() { if (this.state.reconnectAttempts < 5) { this.state.reconnectAttempts++; const delay = Math.min(1000 * Math.pow(2, this.state.reconnectAttempts), 30000); setTimeout(() => this.connect(), delay); } }
  send(message) { if (this.ws && this.ws.readyState === WebSocket.OPEN) this.ws.send(JSON.stringify(message)); }
  appendMessage(role, content, metadata = {}) {
    const messagesDiv = document.getElementById('chat-messages'); if (!messagesDiv) return;
    const messageDiv = document.createElement('div'); messageDiv.className = 'message ' + role + '-message flex flex-col gap-1 max-w-[85%] ' + (role === 'user' ? 'self-end' : 'self-start') + ' animate-slide-in';
    const timestamp = new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const model = metadata.model || this.state.currentModel; const directors = metadata.directors || [];
    if (role === 'user') {
      messageDiv.innerHTML = '<div class="flex items-center gap-2 justify-end"><div class="text-right"><div class="font-mono text-xs text-secondary uppercase">USUARIO</div><div class="font-sans text-[10px] text-on-surface-variant">' + timestamp + '</div></div><div class="w-8 h-8 rounded-full bg-gradient-to-br from-secondary-container to-tertiary-container flex items-center justify-center"><span class="material-symbols-outlined text-[18px] text-on-secondary">person</span></div></div><div class="ml-10 bg-secondary-container/20 backdrop-blur-md rounded-lg p-3 border border-secondary-container/30 text-on-surface text-sm whitespace-pre-wrap">' + this.escapeHtml(content) + '</div><div class="ml-10 font-mono text-[10px] text-outline-variant">' + timestamp + ' • ' + model + '</div>';
    } else {
      const directorsBadges = directors.length > 0 ? '<div class="flex flex-wrap gap-1 mt-2">' + directors.map(d => '<span class="px-1.5 py-0.5 bg-surface-container-lowest rounded text-[9px] font-mono text-primary-container border border-primary-container/20">' + d + '</span>').join('') + '</div>' : '';
      messageDiv.innerHTML = '<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-container to-secondary-container flex items-center justify-center"><span class="material-symbols-outlined text-[18px] text-on-primary">smart_toy</span></div><div><div class="font-mono text-xs text-primary uppercase">JARVIS ECC</div><div class="font-sans text-[10px] text-on-surface-variant">Consejo Ejecutivo • ' + (directors.length > 0 ? directors.join(', ') : 'Análisis directo') + '</div></div></div><div class="ml-10 bg-surface-container-low/80 backdrop-blur-md rounded-lg p-3 border border-primary-container/20 text-on-surface text-sm whitespace-pre-wrap">' + this.escapeHtml(content) + '</div>' + directorsBadges + '<div class="ml-10 font-mono text-[10px] text-outline-variant">' + timestamp + ' • ' + model + '</div>';
    }
    messagesDiv.appendChild(messageDiv); messagesDiv.scrollTop = messagesDiv.scrollHeight; if (messagesDiv.children.length > 100) messagesDiv.removeChild(messagesDiv.firstChild);
  }
  escapeHtml(text) { const div = document.createElement('div'); div.textContent = text; return div.innerHTML; }
  appendStreamChunk(content) { const messagesDiv = document.getElementById('chat-messages'); let lastMessage = messagesDiv.lastElementChild; if (lastMessage && lastMessage.classList.contains('assistant-message')) { const contentDiv = lastMessage.querySelector('.whitespace-pre-wrap'); if (contentDiv) contentDiv.textContent += content; } else { const messageDiv = document.createElement('div'); messageDiv.className = 'message assistant-message flex flex-col gap-1 max-w-[85%] self-start animate-slide-in'; messageDiv.innerHTML = '<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-container to-secondary-container flex items-center justify-center"><span class="material-symbols-outlined text-[18px] text-on-primary">smart_toy</span></div><div><div class="font-mono text-xs text-primary uppercase">JARVIS ECC</div><div class="font-sans text-[10px] text-on-surface-variant">Streaming...</div></div></div><div class="ml-10 bg-surface-container-low/80 backdrop-blur-md rounded-lg p-3 border border-primary-container/20 text-on-surface text-sm whitespace-pre-wrap">' + this.escapeHtml(content) + '</div>'; document.getElementById('chat-messages').appendChild(messageDiv); } document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight; }
  updateExecutiveResponse(summary) { const el = document.getElementById('executive-response'); if (el && summary) el.innerHTML = '<div class="bg-surface-container-lowest p-3 rounded border border-primary-container/20"><div class="font-mono text-xs text-primary uppercase mb-1">RESUMEN EJECUTIVO</div><div class="text-sm text-on-surface">' + this.escapeHtml(summary) + '</div></div>'; }
  updateActiveDirectors(directors) { const el = document.getElementById('active-directors'); const countEl = document.getElementById('directors-count'); if (directors && directors.length > 0) { this.state.activeDirectors = directors; el.textContent = 'Directores: ' + directors.join(', '); if (countEl) countEl.textContent = directors.length + '/8'; document.querySelectorAll('.director-card').forEach(card => { const directorId = card.dataset.director; const isActive = directors.some(d => directorId.includes(d.toLowerCase().replace(' ', '_'))); card.classList.toggle('border-primary', isActive); card.classList.toggle('bg-surface-container-high', isActive); const dot = card.querySelector('.w-2.h-2'); if (dot) dot.classList.toggle('animate-pulse', isActive); }); } else { el.textContent = 'Sin directores activos'; if (countEl) countEl.textContent = '0/8'; } }
  updateSystemMetrics(metrics) { if (metrics.cpu !== undefined) { document.getElementById('cpu-bar').style.width = metrics.cpu + '%'; document.getElementById('cpu-text').textContent = metrics.cpu + '%'; } if (metrics.memory !== undefined) { document.getElementById('mem-bar').style.width = metrics.memory + '%'; document.getElementById('mem-text').textContent = metrics.memory + '%'; } if (metrics.network !== undefined) { document.getElementById('net-bar').style.width = metrics.network + '%'; document.getElementById('net-text').textContent = metrics.network + '%'; } }
  updateFinancialTicker(ticker) { Object.entries(ticker).forEach(([key, value]) => { const priceEl = document.getElementById(key + '-price'); const changeEl = document.getElementById(key + '-change'); if (priceEl) priceEl.textContent = value.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); if (changeEl) { changeEl.textContent = (value.change >= 0 ? '▲' : '▼') + ' ' + Math.abs(value.change).toFixed(2) + '%'; changeEl.className = 'font-mono text-sm font-bold flex items-center ' + (value.change >= 0 ? 'text-primary-fixed' : 'text-error'); }); }
  appendTradingLog(log) { const el = document.getElementById('trading-console'); if (!el) return; const div = document.createElement('div'); div.className = 'text-xs font-mono'; div.textContent = log; el.appendChild(div); el.scrollTop = el.scrollHeight; while (el.children.length > 100) el.removeChild(el.firstChild); }
  appendAppsLog(log) { const el = document.getElementById('apps-console'); if (!el) return; const div = document.createElement('div'); div.className = 'text-xs font-mono'; div.textContent = log; el.appendChild(div); el.scrollTop = el.scrollHeight; while (el.children.length > 100) el.removeChild(el.firstChild); }
  appendOpsecLog(log) { const el = document.getElementById('opsec-console'); if (!el) return; const div = document.createElement('div'); div.className = 'text-xs font-mono'; div.textContent = log; el.appendChild(div); el.scrollTop = el.scrollHeight; while (el.children.length > 100) el.removeChild(el.firstChild); }
  appendTacticalResponse(response) { const el = document.getElementById('opsec-console'); if (!el) return; const div = document.createElement('div'); div.className = 'text-xs font-mono text-primary-fixed-dim'; div.textContent = response; el.appendChild(div); el.scrollTop = el.scrollHeight; }
}

class ChatController {
  constructor(state) { this.state = state; }
  init() { this.setupEventListeners(); }
  setupEventListeners() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('btn-send');
    const micBtn = document.getElementById('btn-mic');
    const clearBtn = document.getElementById('clear-chat');
    const modelSelector = document.getElementById('model-selector');
    if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
    if (input) input.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.sendMessage(); } });
    if (input) input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 128) + 'px'; });
    if (modelSelector) modelSelector.addEventListener('change', (e) => { this.state.currentModel = e.target.value; });
    if (clearBtn) clearBtn.addEventListener('click', () => { document.getElementById('chat-messages').innerHTML = ''; this.state.ws?.appendMessage('system', 'Chat limpiado. Sistemas listos para nueva directiva.'); });
    if (micBtn) { micBtn.addEventListener('mousedown', () => this.startRecording()); micBtn.addEventListener('mouseup', () => this.stopRecording()); micBtn.addEventListener('mouseleave', () => this.stopRecording()); micBtn.addEventListener('touchstart', (e) => { e.preventDefault(); this.startRecording(); }); micBtn.addEventListener('touchend', (e) => { e.preventDefault(); this.stopRecording(); });
  }
  sendMessage() { const input = document.getElementById('chat-input'); const content = input.value.trim(); if (!content) return; input.value = ''; input.style.height = 'auto'; if (this.state.ws) { this.state.ws.appendMessage('user', content); this.state.ws.send({ type: 'chat', content: content, model: this.state.currentModel }); } }
  async startRecording() { if (this.state.isRecording) return; try { const stream = await navigator.mediaDevices.getUserMedia({ audio: true }); this.state.mediaRecorder = new MediaRecorder(stream); this.state.audioChunks = []; this.state.mediaRecorder.ondataavailable = (e) => { this.state.audioChunks.push(e.data); }; this.state.mediaRecorder.onstop = async () => { const audioBlob = new Blob(this.state.audioChunks, { type: 'audio/webm' }); await this.sendAudioToBackend(audioBlob); stream.getTracks().forEach(track => track.stop()); }; this.state.mediaRecorder.start(); this.state.isRecording = true; document.getElementById('btn-mic').classList.add('recording'); document.getElementById('mic-icon').classList.add('hidden'); document.getElementById('mic-icon-active').classList.remove('hidden'); document.getElementById('btn-mic').style.boxShadow = '0 0 24px #00F3FF'; } catch (err) { console.error('[JARVIS] Error accediendo al micrófono:', err); alert('No se pudo acceder al micrófono. Verifique los permisos.'); } }
  stopRecording() { if (!this.state.isRecording || !this.state.mediaRecorder) return; this.state.mediaRecorder.stop(); this.state.isRecording = false; document.getElementById('btn-mic').classList.remove('recording'); document.getElementById('mic-icon').classList.remove('hidden'); document.getElementById('mic-icon-active').classList.add('hidden'); document.getElementById('btn-mic').style.boxShadow = ''; }
  async sendAudioToBackend(audioBlob) { const formData = new FormData(); formData.append('audio', audioBlob, 'recording.webm'); formData.append('model', this.state.currentModel); try { const response = await fetch('/api/voice', { method: 'POST', body: formData }); const data = await response.json(); if (data.text && this.state.ws) { this.state.ws.send({ type: 'chat', content: data.text, model: this.state.currentModel }); } } catch (err) { console.error('[JARVIS] Error enviando audio:', err); } }
}

class SystemMetrics {
  constructor(state) { this.state = state; this.interval = null; }
  start() { this.interval = setInterval(() => { if (this.state.ws) { this.state.ws.updateSystemMetrics({ cpu: Math.max(5, Math.min(45, 12 + Math.random() * 20 - 10)), memory: Math.max(20, Math.min(60, 34 + Math.random() * 10 - 5)), network: Math.max(2, Math.min(25, 8 + Math.random() * 8 - 4)) }); } }, 2000); }
}

class FinancialTicker {
  constructor(state) { this.state = state; this.interval = null; this.prices = { 'sp500': 5912.40, 'btc': 67420.00, 'eth': 3840.50, 'gold': 2340.20, 'dxy': 104.32, 'vix': 14.85 }; }
  start() { this.interval = setInterval(() => { Object.keys(this.prices).forEach(key => { const change = (Math.random() - 0.5) * 0.005; this.prices[key] *= (1 + change); if (this.state.ws) { this.state.ws.updateFinancialTicker({ [key]: { price: this.prices[key], change: change * 100 } }); } }); }, 3000); }
}

class TacticalConsoles {
  constructor(state) { this.state = state; this.interval = null; }
  start() { this.interval = setInterval(() => { if (!this.state.ws) return; const tradingLogs = ['[QUANT] Escaneando orderbook L3...', '[HEDGE] Rebalanceando delta-neutral...', '[RISK] VaR 99%: $12.4K | Esperado: $8.2K', '[EXEC] Fill confirmado: 25 ES @ 5415.25', '[ALPHA] Signal detectada: Momentum +18.4', '[LATENCY] CME RTT: 0.18ms | NY4: 0.22ms']; const appsLogs = ['[SWARM] Agente Architect: Nuevo PR #2341', '[CI/CD] Pipeline completado en 7.8s', '[AUDITOR] SAST: 0 vulnerabilidades críticas', '[REGISTRY] Push: quant-engine:v5.1.0', '[DEPLOY] Canary deploy a LD4 iniciado']; const opsecLogs = ['[PI-HOLE] 237 dominios bloqueados en última hora', '[VOPONO] Ruta rotada: CH → IS → FI', '[FAWKES] Perturbación adversarial aplicada', '[MVT] Escaneo completado: 0 indicadores Pegasus', '[GRAPHENE] Hardening: Memoria verificada']; if (Math.random() < 0.3) this.state.ws.appendTradingLog(tradingLogs[Math.floor(Math.random() * tradingLogs.length)]); if (Math.random() < 0.3) this.state.ws.appendAppsLog(appsLogs[Math.floor(Math.random() * appsLogs.length)]); if (Math.random() < 0.3) this.state.ws.appendOpsecLog(opsecLogs[Math.floor(Math.random() * opsecLogs.length)]); }, 5000); }
}

async function init() { console.log('[JARVIS] Inicializando Centro de Mando Global...'); AppState.controllers.ws = new WebSocketClient(AppState); AppState.controllers.chat = new ChatController(AppState); AppState.controllers.metrics = new SystemMetrics(AppState); AppState.controllers.ticker = new FinancialTicker(AppState); AppState.controllers.consoles = new TacticalConsoles(AppState); AppState.controllers.chat.init(); await AppState.controllers.ws.connect(); AppState.controllers.metrics.start(); AppState.controllers.ticker.start(); AppState.controllers.consoles.start(); setupGlobalListeners(); animateEntrance(); setupTabs(); setupTacticalCommand(); console.log('[JARVIS] Sistemas operativos. Númcleo listo.'); }
function setupGlobalListeners() { document.addEventListener('dragover', e => e.preventDefault()); document.addEventListener('drop', e => e.preventDefault()); document.addEventListener('keydown', (e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); document.getElementById('chat-input')?.focus(); } if (e.key === 'Escape') { const input = document.getElementById('chat-input'); if (input === document.activeElement) input.blur(); } }); document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && AppState.ws?.readyState !== WebSocket.OPEN) { AppState.controllers.ws.connect(); } }); }
function animateEntrance() { document.querySelectorAll('.director-card').forEach((card, i) => { card.style.opacity = '0'; card.style.transform = 'translateX(-20px)'; setTimeout(() => { card.style.transition = 'all 0.4s ease'; card.style.opacity = '1'; card.style.transform = 'translateX(0)'; }, i * 80); }); }
function setupTabs() { document.querySelectorAll('.tab-btn').forEach(btn => { btn.addEventListener('click', () => switchTab(btn.dataset.tab)); }); }
function switchTab(tabId) { document.querySelectorAll('.tab-btn').forEach(btn => { const isActive = btn.dataset.tab === tabId; btn.classList.toggle('active', isActive); btn.setAttribute('aria-selected', isActive); }); document.querySelectorAll('.tab-content').forEach(content => { const isActive = content.id === tabId; content.classList.toggle('hidden', !isActive); content.setAttribute('aria-hidden', !isActive); }); }
function setupTacticalCommand() { const tacticalInput = document.getElementById('jarvis-command-input'); const tacticalBtn = document.getElementById('btn-send-tactical'); if (tacticalBtn && tacticalInput) { tacticalBtn.addEventListener('click', () => { const cmd = tacticalInput.value.trim(); if (cmd && AppState.ws) { AppState.ws.appendTacticalResponse('[JARVIS ECC] Ejecutando directiva táctica: "' + cmd + '"'); AppState.ws.send({ type: 'tactical_command', command: cmd }); } }); tacticalInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') tacticalBtn.click(); }); }
}
window.JARVIS = AppState;
if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
export { AppState, init };
