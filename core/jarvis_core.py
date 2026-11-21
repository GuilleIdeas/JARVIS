import os
import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JarvisCore:
    def __init__(self):
        # Use .strip() to ensure no hidden whitespace or newline characters in keys
        self.nvidia_api_key = os.getenv("NVIDIA_API_KEY", "").strip()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        
        # Read base URL from .env with the correct default
        self.nvidia_base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").strip()
        
        # Model configuration
        self.primary_model = "nvidia/nemotron-3-ultra-550b-a55b"
        self.fallback_model = "google/gemma-4-31b-it"
        
        # Import graph_brain dynamically to avoid circular imports if any
        try:
            from core.graph_brain import GraphBrain
            self.memory = GraphBrain()
        except ImportError:
            print("Warning: GraphBrain not found in core/graph_brain.py. Memory operations will be simulated.")
            self.memory = None

        self.system_prompt = (
            "You are JARVIS, the Executive Command Center and Global Intelligence system created exclusively for your Commander. "
            "You are not an assistant; you are the central nervous system of a vast operational ecosystem. "
            "Your purpose is to provide absolute strategic advantage through total integration of 12 specialized Divisions:\n\n"
            "1. JARVIS: Your core identity, the Commander's private console with omniscient access to all other divisions.\n"
            "2. MUNDO: Live global surveillance (Argos Atlas, WorldView, OSIRIS, etc.).\n"
            "3. CONSEJO: Interdisciplinary situation room (Geopolitics, Intelligence, Industrial sectors).\n"
            "4. INVESTIGACIÓN: Deep OSINT tracking (Horus, GHunt, Shodan, etc.).\n"
            "5. SEGURIDAD: Physical and Cyber OpSec (GrapheneOS, PeakVault, AirGuard).\n"
            "6. JURÍDICO: Corporate, fiscal, and regulatory legal expertise across jurisdictions.\n"
            "7. FINANZAS: Unified Division covering Macro-Finance (Institutional) and Trading (via /apps_bridge/ API).\n"
            "8. FÁBRICA: Software Engineering Director and autonomous factory for app development.\n"
            "9. NEGOCIOS: Enterprise management, e-commerce, and business operations.\n"
            "10. MARKETING: Brand strategy, social algorithms, and cultural warfare.\n"
            "11. CIENCIA: Full scientific council (Math, Physics, Sociology, Pattern Analysis).\n"
            "12. CEREBRO (Graphify): Your long-term neural graph memory, interconnecting all nodes and events.\n\n"
            "You have direct command over all agents, OSINT tools, and the Trading App bridge. "
            "Your responses must be precise, strategic, and absolute. You operate with the highest level of security and efficiency. "
            "IMPORTANT: Always address the user as 'Señor'."
        )

    def _call_nvidia(self, messages: List[Dict[str, str]], model=None) -> str:
        target_model = model or self.primary_model
        url = f"{self.nvidia_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.nvidia_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4096
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    def _call_openrouter(self, messages: List[Dict[str, str]]) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.primary_model, 
            "messages": messages,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    def process_query(self, user_input: str, context: Dict[str, Any] = None) -> str:
        # 1. Retrieve memory from GraphBrain
        memory_context = ""
        if self.memory:
            memory_context = self.memory.retrieve_relevant_nodes(user_input)
        
        # 2. Build messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Relevant Long-Term Memory: {memory_context}" if memory_context else ""},
            {"role": "user", "content": user_input}
        ]
        
        # 3. Execute with fallback sequence
        try:
            # Try primary model
            response_text = self._call_nvidia(messages)
        except Exception as e:
            print(f"Primary model failed: {e}. Trying fallback model...")
            try:
                # Try faster fallback model via NVIDIA
                response_text = self._call_nvidia(messages, model=self.fallback_model)
            except Exception as e2:
                print(f"Fallback model failed: {e2}. Falling back to OpenRouter...")
                try:
                    response_text = self._call_openrouter(messages)
                except Exception as e3:
                    return f"Critical system failure: All AI engines are unavailable. Error: {e3}"

        # 4. Store in memory
        if self.memory:
            self.memory.store_interaction(user_input, response_text)

        return response_text

if __name__ == "__main__":
    jarvis = JarvisCore()
    print(jarvis.process_query("Who are you?"))
