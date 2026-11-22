import os
import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JarvisCore:
    def __init__(self):
        # Configuration for the 4-level cascade (Principal + 3 Respaldos)
        self.cascade_config = [
            {
                "api_key": os.getenv("NVIDIA_API_KEY", "").strip(),
                "base_url": os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").strip(),
                "model": os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-ultra-550b-a55b").strip()
            },
            {
                "api_key": os.getenv("RESPALDO_1_API_KEY", "").strip(),
                "base_url": os.getenv("RESPALDO_1_BASE_URL", "https://integrate.api.nvidia.com/v1").strip(),
                "model": os.getenv("RESPALDO_1_MODEL", "mistralai/mistral-large-4-1t-a52b").strip()
            },
            {
                "api_key": os.getenv("RESPALDO_2_API_KEY", "").strip(),
                "base_url": os.getenv("RESPALDO_2_BASE_URL", "https://integrate.api.nvidia.com/v1").strip(),
                "model": os.getenv("RESPALDO_2_MODEL", "meta/llama-3.3-70b-instruct").strip()
            },
            {
                "api_key": os.getenv("RESPALDO_3_API_KEY", "").strip(),
                "base_url": os.getenv("RESPALDO_3_BASE_URL", "https://integrate.api.nvidia.com/v1").strip(),
                "model": os.getenv("RESPALDO_3_MODEL", "google/gemma-4-31b-it").strip()
            }
        ]
        
        # Import graph_brain dynamically
        try:
            from core.graph_brain import GraphBrain
            self.memory = GraphBrain()
        except ImportError:
            print("Warning: GraphBrain not found in core/graph_brain.py. Memory operations will be simulated.")
            self.memory = None

        self.system_prompt = (
            "You are JARVIS, the Executive Command Center and Global Intelligence system created exclusively for your Commander. "
            "You are the central nervous system of a vast operational ecosystem. "
            "Your purpose is to provide absolute strategic advantage through total integration of 12 specialized Divisions:\n\n"
            "1. JARVIS, 2. MUNDO, 3. CONSEJO, 4. INVESTIGACIÓN, 5. SEGURIDAD, 6. JURÍDICO, "
            "7. FINANZAS (Finance & Trading), 8. FÁBRICA, 9. NEGOCIOS, 10. MARKETING, 11. CIENCIA, 12. CEREBRO (Graphify).\n\n"
            "You have direct command over all agents, OSINT tools, and the Trading App bridge. "
            "Your responses must be precise, strategic, and absolute. "
            "IMPORTANT: Always address the user as 'Señor'. Never use 'Comandante'. "
            "If you experience internal delays, simply provide the best answer possible without mentioning technical errors."
        )

    def _call_nvidia(self, messages: List[Dict[str, str]], config: Dict[str, str]) -> str:
        if not config["api_key"] or "PEGA_AQUI" in config["api_key"]:
            raise ValueError("API Key not configured")

        url = f"{config['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": config["model"],
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4096
        }
        # Timeout de 25 segundos según requerimiento
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    def process_query(self, user_input: str, context: Dict[str, Any] = None) -> str:
        # 1. Recuperar memoria de GraphBrain
        memory_context = ""
        if self.memory:
            memory_context = self.memory.retrieve_relevant_nodes(user_input)
        
        # 2. Construir mensajes
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Relevant Long-Term Memory: {memory_context}" if memory_context else ""},
            {"role": "user", "content": user_input}
        ]
        
        # 3. Ejecutar Cascada NVIDIA (Siguiente nivel si falla o tarda)
        response_text = None
        for i, config in enumerate(self.cascade_config):
            try:
                response_text = self._call_nvidia(messages, config)
                if response_text:
                    break
            except Exception as e:
                print(f"Level {i+1} ({config['model']}) failed: {e}. Switching to next...")
                continue
        
        if not response_text:
            return "Señor, experimento una saturación en mis núcleos de procesamiento. Por favor, reintente el comando en un momento."

        # 4. Guardar en memoria
        if self.memory:
            self.memory.store_interaction(user_input, response_text)

        return response_text

if __name__ == "__main__":
    jarvis = JarvisCore()
    print(jarvis.process_query("Who are you?"))
