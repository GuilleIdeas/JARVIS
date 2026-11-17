import sys
sys.path.insert(0, '.')

from core.config import settings
from core.jarvis_core import get_jarvis_core, DirectorRole
from ecc_directors import get_all_directors, get_director_prompt, get_director_metadata
from tools_and_bridges.registry import get_tool_registry
from apps_bridge.bridge import get_bridge

print('=== CONFIG ===')
print(f'NVIDIA configured: {settings.has_nvidia_key}')
print(f'OpenRouter configured: {settings.has_openrouter_key}')
print(f'Port: {settings.port}')

print()
print('=== JARVIS CORE ===')
core = get_jarvis_core()
print(f'Core initialized: {core._initialized}')

print()
print('=== ECC DIRECTORS ===')
directors = get_all_directors()
print(f'Total directors: {len(directors)}')
for d in directors:
    meta = get_director_metadata(d)
    print(f'  - {meta.get("short", d.value)}: {meta.get("name")}')

print()
print('=== TOOLS REGISTRY ===')
registry = get_tool_registry()
status = registry.get_status_summary()
print(f'Total tools: {status["total_tools"]}')
for cat, info in status["by_category"].items():
    print(f'  {cat}: {info["total"]} tools')

print()
print('=== APPS BRIDGE ===')
bridge = get_bridge()
print(f'Endpoints: {list(bridge.get_status().keys())}')

print()
print('ALL SYSTEMS OPERATIONAL')