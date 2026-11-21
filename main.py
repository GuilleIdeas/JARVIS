from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
from core.jarvis_core import JarvisCore

app = FastAPI()
jarvis = JarvisCore()

# Request model for chat
class ChatRequest(BaseModel):
    message: str
    division: str

# Serve static files from frontend/desktop
app.mount("/static", StaticFiles(directory="/workspaces/JARVIS/frontend/desktop"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("/workspaces/JARVIS/frontend/desktop/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # context can be expanded based on the division
    context = {"division": request.division}
    response_text = jarvis.process_query(request.message, context=context)
    
    # Enforce the "Señor" instead of "Comandante" policy in the output if the model missed it
    response_text = response_text.replace("Comandante", "Señor")
    
    return {"response": response_text}

@app.get("/api/brain/graph")
async def get_graph():
    # Mock data for the Graphify visualization in Division 12
    nodes = [
        {"id": 1, "label": "JARVIS Core", "group": "core"},
        {"id": 2, "label": "Mundo", "group": "div"},
        {"id": 3, "label": "Consejo", "group": "div"},
        {"id": 4, "label": "Investigación", "group": "div"},
        {"id": 5, "label": "Seguridad", "group": "div"},
        {"id": 6, "label": "Jurídico", "group": "div"},
        {"id": 7, "label": "Finanzas", "group": "div"},
        {"id": 8, "label": "Fábrica", "group": "div"},
        {"id": 9, "label": "Negocios", "group": "div"},
        {"id": 10, "label": "Marketing", "group": "div"},
        {"id": 11, "label": "Ciencia", "group": "div"},
        {"id": 12, "label": "Cerebro", "group": "div"},
        {"id": 13, "label": "OSINT Horus", "group": "tool"},
        {"id": 14, "label": "Nemotron 3", "group": "core"},
    ]
    edges = [
        {"from": 1, "to": 2}, {"from": 1, "to": 3}, {"from": 1, "to": 4},
        {"from": 1, "to": 5}, {"from": 1, "to": 6}, {"from": 1, "to": 7},
        {"from": 1, "to": 8}, {"from": 1, "to": 9}, {"from": 1, "to": 10},
        {"from": 1, "to": 11}, {"from": 1, "to": 12}, {"from": 1, "to": 14},
        {"from": 4, "to": 13},
    ]
    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
