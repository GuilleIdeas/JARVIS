# JARVIS - Servidor Principal FastAPI
# Servido optimizado para el Centro de Mando Global

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio
import json
import uvicorn
from pathlib import Path

# Importar el núcleo JARVIS
from core.jarvis_core import get_jarvis_core, initialize_jarvis

# --- LIFESPAN HANDLER (Reemplaza on_event startup) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de inicio
    await initialize_jarvis()
    yield
    # Lógica de cierre si fuera necesaria

app = FastAPI(title="JARVIS", version="10.0.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos correctamente
frontend_path = Path(__file__).parent / "frontend" / "desktop"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

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

# --- WEBSOCKET ENDPOINT (Soporte para Chat y Feed) ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Aceptamos la conexión sin restricciones de origen para evitar el 403 Forbidden
    await websocket.accept()
    core = get_jarvis_core()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get('type') == 'chat_request':
                # Procesar solicitud a través del núcleo JARVIS
                user_msg = message_data.get('message', '')
                response = await core.process_request(user_msg)
                
                await websocket.send_json({
                    'type': 'chat_response',
                    'content': response.executive_summary,
                    'metadata': {
                        'directors': [d.value for d in response.active_directors],
                        'model': response.model_used
                    }
                })
            elif message_data.get('type') == 'tactical_command':
                # Simular respuesta táctica inmediata
                cmd = message_data.get('command', '')
                await websocket.send_json({
                    'type': 'tactical_response',
                    'response': f'Directiva "{cmd}" recibida. Ejecutando protocolos de enlace...'
                })
    except WebSocketDisconnect:
        print("Cliente WebSocket desconectado")
    except Exception as e:
        print(f"Error en WebSocket: {e}")

# Rutas principales
@app.get("/main", response_class=HTMLResponse)
async def root():
    html_path = Path(__file__).parent / "frontend" / "desktop" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>JARVIS</h1><p>Frontend no encontrado</p>")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
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
    form = await request.form()
    audio = form.get("audio")
    if not audio:
        return {"error": "No audio provided"}
    return {"text": "[Transcripción de voz no implementada todavía]"}

@app.get("/health")
async def health():
    core = get_jarvis_core()
    return {
        "status": "healthy",
        "version": "10.0.0",
        "jarvis_core": core.get_stats()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
