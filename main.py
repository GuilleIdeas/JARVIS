# JARVIS ECC - Servidor Principal FastAPI
# Sirve el HTML de Stitch directamente con script embebido para chat API

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import uvicorn
from pathlib import Path

# Importar el núcleo JARVIS
from core.jarvis_core import get_jarvis_core, initialize_jarvis

app = FastAPI(title="JARVIS ECC", version="9.4.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
frontend_path = Path(__file__).parent / "frontend" / "desktop"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


# Modelos
class ChatRequest(BaseModel):
    message: str
    model: str = "nvidia/nemotron-3-ultra"
    context: str = ""


class ChatResponse(BaseModel):
    request_id: str
    executive_summary: str
    detailed_response: str
    active_directors: list[str]
    model_used: str
    provider: str
    total_tokens: int
    latency_ms: float
    metadata: dict = {}


# Inicializar JARVIS al arrancar
@app.on_event("startup")
async def startup_event():
    await initialize_jarvis()


# Rutas principales
@app.get("/", response_class=HTMLResponse)
async def root():
    """Sirve el HTML principal de Stitch (Cleopatra - Centro de Mando Global)"""
    html_path = Path(__file__).parent / "JARVIS" / "JARVIS" / "jarvis_ecc_n_cleo_de_mando_global" / "code.html"
    if html_path.exists():
        content = html_path.read_text(encoding="utf-8")
        # Inyectar script de chat al final del body
        chat_script = """<script>
// Chat API Client para JARVIS ECC
(function() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('btn-send');
    const chatMessages = document.getElementById('chat-messages');
    const micBtn = document.getElementById('btn-mic');
    const modelSelector = document.getElementById('model-selector');
    const clearBtn = document.getElementById('clear-chat');
    const activeDirectorsEl = document.getElementById('active-directors');
    
    let currentModel = 'nvidia/nemotron-3-ultra';
    let isRecording = false;
    let mediaRecorder = null;
    let audioChunks = [];
    
    // Añadir mensaje al chat
    function addMessage(role, content, meta = {}) {
        if (!chatMessages) return;
        const div = document.createElement('div');
        div.className = 'message ' + role + '-message flex flex-col gap-1 max-w-[85%] ' + (role === 'user' ? 'self-end' : 'self-start') + ' animate-slide-in';
        const time = new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const model = meta.model || 'nvidia/nemotron-3-ultra';
        const directors = meta.directors || [];
        
        if (role === 'user') {
            div.innerHTML = '<div class="flex items-center gap-2 justify-end"><div class="text-right"><div class="font-mono text-xs text-secondary uppercase">USUARIO</div><div class="font-sans text-[10px] text-on-surface-variant">' + time + '</div></div><div class="w-8 h-8 rounded-full bg-gradient-to-br from-secondary-container to-tertiary-container flex items-center justify-center"><span class="material-symbols-outlined text-[18px] text-on-secondary">person</span></div></div><div class="ml-10 bg-secondary-container/20 backdrop-blur-md rounded-lg p-3 border border-secondary-container/30 text-on-surface text-sm whitespace-pre-wrap">' + content + '</div><div class="ml-10 font-mono text-[10px] text-outline-variant">' + time + ' • ' + model + '</div>';
        } else {
            const directorsBadges = meta.directors && meta.directors.length > 0 
                ? '<div class="flex flex-wrap gap-1 mt-2">' + meta.directors.map(d => '<span class="px-1.5 py-0.5 bg-surface-container-lowest rounded text-[9px] font-mono text-primary-container border border-primary-container/20">' + d + '</span>').join('') + '</div>' : '';
            div.innerHTML = '<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-container to-secondary-container flex items-center justify-center"><span class="material-symbols-outlined text-[18px] text-on-primary">smart_toy</span></div><div><div class="font-mono text-xs text-primary uppercase">JARVIS ECC</div><div class="font-sans text-[10px] text-on-surface-variant">Consejo Ejecutivo • ' + (meta.directors && meta.directors.length > 0 ? meta.directors.join(', ') : 'Análisis directo') + '</div></div><div class="ml-10 bg-surface-container-low/80 backdrop-blur-md rounded-lg p-3 border border-primary-container/20 text-on-surface text-sm whitespace-pre-wrap">' + content + '</div>' + directorsBadges + '<div class="ml-10 font-mono text-[10px] text-outline-variant">' + time + ' • ' + model + '</div>';
        }
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Enviar mensaje
    async function sendMessage() {
        const input = document.getElementById('chat-input');
        const content = input.value.trim();
        if (!content) return;
        input.value = '';
        input.style.height = 'auto';
        
        addMessage('user', content);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: content, model: currentModel })
            );
            const data = await response.json();
            addMessage('assistant', data.detailed_response || data.executive_summary, { 
                model: data.model_used, 
                directors: data.active_directors 
            });
        } catch (err) {
            console.error('[JARVIS] Error:', err);
            addMessage('assistant', 'Error de conexión: ' + err.message);
        }
    }
    
    // Event listeners
    const sendBtn = document.getElementById('btn-send');
    const chatInput = document.getElementById('chat-input');
    const micBtn = document.getElementById('btn-mic');
    const clearBtn = document.getElementById('clear-chat');
    const modelSelector = document.getElementById('model-selector');
    
    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (chatInput) chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    if (chatInput) chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 128) + 'px';
    });
    if (modelSelector) modelSelector.addEventListener('change', (e) => { currentModel = e.target.value; });
    if (clearBtn) clearBtn.addEventListener('click', () => {
        document.getElementById('chat-messages').innerHTML = '';
        addMessage('system', 'Chat limpiado. Sistemas listos para nueva directiva.');
    });
    if (modelSelector) modelSelector.addEventListener('change', (e) => { currentModel = e.target.value; });
    
    // Micrófono (Push-to-Talk)
    let isRecording = false;
    let mediaRecorder = null;
    let audioChunks = [];
    
    const micBtn = document.getElementById('btn-mic');
    if (micBtn) {
        micBtn.addEventListener('mousedown', startRecording);
        micBtn.addEventListener('mouseup', stopRecording);
        micBtn.addEventListener('mouseleave', stopRecording);
        micBtn.addEventListener('touchstart', (e) => { e.preventDefault(); startRecording(); });
        micBtn.addEventListener('touchend', (e) => { e.preventDefault(); stopRecording(); });
    }
    
    async function startRecording() {
        if (isRecording) return;
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                await sendAudioToBackend(audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };
            mediaRecorder.start();
            isRecording = true;
            document.getElementById('btn-mic').classList.add('recording');
            document.getElementById('mic-icon').classList.add('hidden');
            document.getElementById('mic-icon-active').classList.remove('hidden');
            document.getElementById('btn-mic').style.boxShadow = '0 0 24px #00F3FF';
        } catch (err) {
            console.error('[JARVIS] Error accediendo al micrófono:', err);
            alert('No se pudo acceder al micrófono. Verifique los permisos.');
        }
    }
    
    function stopRecording() {
        if (!isRecording || !mediaRecorder) return;
        mediaRecorder.stop();
        isRecording = false;
        document.getElementById('btn-mic').classList.remove('recording');
        document.getElementById('mic-icon').classList.remove('hidden');
        document.getElementById('mic-icon-active').classList.add('hidden');
        document.getElementById('btn-mic').style.boxShadow = '';
    }
    
    async function sendAudioToBackend(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        formData.append('model', 'nvidia/nemotron-3-ultra');
        try {
            const response = await fetch('/api/voice', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.text) {
                document.getElementById('chat-input').value = data.text;
                document.dispatchEvent(new Event('submit'));
            }
        } catch (err) {
            console.error('[JARVIS] Error enviando audio:', err);
        }
    }
    
    // Exponer funciones globalmente
    window.addMessage = addMessage;
    window.sendMessage = sendMessage;
    window.startRecording = startRecording;
    window.stopRecording = stopRecording;
    window.currentModel = currentModel;
})();
</script>"""
        # Insertar antes de </body>
        content = content.replace('</body>', chat_script + '\\n</body>')


        return HTMLResponse(content=content)
    return HTMLResponse(content="<h1>JARVIS ECC</h1><p>Frontend no encontrado</p>")


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Endpoint principal de chat con el Consejo ECC"""
    core = get_jarvis_core()
    response = await core.process_request(request.message, request.context)
    return ChatResponse(
        request_id=response.request_id,
        executive_summary=response.executive_summary,
        detailed_response=response.detailed_response,
        active_directors=[d.value for d in response.active_directors],
        model_used=response.model_used,
        provider=response.provider.value,
        total_tokens=response.total_tokens,
        latency_ms=response.total_latency_ms,
        metadata=response.metadata
    )


@app.post("/api/voice")
async def voice_endpoint(request: Request):
    """Endpoint para procesamiento de voz (STT)"""
    form = await request.form()
    audio = form.get("audio")
    model = form.get("model", "nvidia/nemotron-3-ultra")
    
    if not audio:
        return {"error": "No audio provided"}
    
    # TODO: Implementar STT real (Whisper, etc.)
    # Por ahora devolvemos un placeholder
    return {"text": "[Transcripción de voz no implementada todavía]"}


@app.get("/health")
async def health():
    core = get_jarvis_core()
    return {
        "status": "healthy",
        "version": "9.4.0",
        "jarvis_core": core.get_stats()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
