# ECC Directors - Minimal implementation for imports
from core.jarvis_core import DirectorRole

def get_director_prompt(director: DirectorRole) -> str:
    return "Eres un asesor experto del Consejo ECC."

def get_all_directors():
    return list(DirectorRole)

def get_director_metadata(director: DirectorRole) -> dict:
    return {"name": director.value.replace('_', ' ').title(), "short": director.value[:15]}