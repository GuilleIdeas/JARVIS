# JARVIS ECC - Tool Registry (Completo con GHUNT y TOUTATIS)
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
import asyncio
import logging

logger = logging.getLogger(__name__)

class ToolCategory(str, Enum):
    OSINT_INTELIGENCIA = 'osint_inteligencia'
    OSINT_RASTREO = 'osint_rastreo'
    OPSEC_PRIVACIDAD = 'opsec_privacidad'
    OPSEC_BLINDAJE = 'opsec_blindaje'

class ToolStatus(str, Enum):
    AVAILABLE = 'available'
    CONFIGURED = 'configured'
    RUNNING = 'running'
    ERROR = 'error'
    DISABLED = 'disabled'

@dataclass
class ToolConfig:
    name: str
    category: ToolCategory
    description: str
    command: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key_env: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    timeout: int = 300
    rate_limit: Optional[int] = None

@dataclass
class ToolResult:
    tool_name: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

# ============================================
# HERRAMIENTAS OSINT
# ============================================

OSINT_TOOLS = {
    'argos_atlas': ToolConfig('Argos Atlas', ToolCategory.OSINT_INTELIGENCIA, 'Inteligencia de amenazas',
        command='argos-atlas', api_endpoint='https://api.argos-atlas.com/v1', api_key_env='ARGOS_ATLAS_API_KEY'),
    'osiris': ToolConfig('Osiris', ToolCategory.OSINT_INTELIGENCIA, 'Reconocimiento de infraestructura',
        command='osiris', parameters={'modules': ['dns', 'ssl', 'headers']}),
    'horus': ToolConfig('Horus', ToolCategory.OSINT_INTELIGENCIA, 'Analisis de amenazas IA',
        command='horus', api_endpoint='https://api.horus-threat.com/v1', api_key_env='HORUS_API_KEY'),
    'flowsint': ToolConfig('Flowsint', ToolCategory.OSINT_INTELIGENCIA, 'Analisis de flujos de red',
        command='flowsint'),
    'graphify': ToolConfig('Graphify', ToolCategory.OSINT_INTELIGENCIA, 'Visualizacion de grafos',
        command='graphify', api_endpoint='https://api.graphify.io/v1', api_key_env='GRAPHIFY_API_KEY'),
    'facecheck_id': ToolConfig('FaceCheck.ID', ToolCategory.OSINT_INTELIGENCIA, 'Busqueda facial inversa',
        api_endpoint='https://api.facecheck.id/v1', api_key_env='FACECHECK_API_KEY'),
    'war_sanctions': ToolConfig('War Sanctions', ToolCategory.OSINT_INTELIGENCIA, 'Sanciones internacionales',
        api_endpoint='https://api.war-sanctions.gov/v1', api_key_env='WAR_SANCTIONS_API_KEY'),
    'airplanes_live': ToolConfig('Airplanes Live', ToolCategory.OSINT_RASTREO, 'Tracking de vuelos',
        api_endpoint='https://api.airplanes.live/v2', api_key_env='AIRPLANES_LIVE_API_KEY'),
    'marine_traffic': ToolConfig('Marine Traffic', ToolCategory.OSINT_RASTREO, 'Tracking maritimo AIS',
        api_endpoint='https://services.marinetraffic.com/api', api_key_env='MARINE_TRAFFIC_API_KEY'),
    'insecam': ToolConfig('Insecam', ToolCategory.OSINT_RASTREO, 'Camaras IP expuestas',
        command='insecam-scanner'),
    'shodan_images': ToolConfig('Shodan Images', ToolCategory.OSINT_RASTREO, 'Dispositivos IoT expuestos',
        api_endpoint='https://api.shodan.io/shodan/host/search', api_key_env='SHODAN_API_KEY'),
    'wordmonitor': ToolConfig('Wordmonitor', ToolCategory.OSINT_RASTREO, 'Monitoreo de reputacion web',
        api_endpoint='https://api.wordmonitor.com/v1', api_key_env='WORDMONITOR_API_KEY'),
    'alien_eyes': ToolConfig('Alien Eyes', ToolCategory.OSINT_RASTREO, 'Vigilancia satelital',
        api_endpoint='https://api.alien-eyes.space/v1', api_key_env='ALIEN_EYES_API_KEY'),
    'ghost_track': ToolConfig('Ghost Track', ToolCategory.OSINT_RASTREO, 'Rastreo huella digital',
        command='ghost-track'),
    'deanonymizer': ToolConfig('Deanonymizer', ToolCategory.OSINT_RASTREO, 'Correlacion identidades',
        command='deanonymizer'),
    'open_planter': ToolConfig('Open Planter', ToolCategory.OSINT_RASTREO, 'Analisis blockchain',
        api_endpoint='https://api.openplanter.xyz/v1', api_key_env='OPEN_PLANTER_API_KEY'),
    'web_search_people': ToolConfig('Busqueda Web Personas', ToolCategory.OSINT_RASTREO, 'Busqueda personas publicas',
        command='web-search-people'),
    'web_search_companies': ToolConfig('Busqueda Web Empresas', ToolCategory.OSINT_RASTREO, 'Busqueda empresas publicas',
        command='web-search-companies'),
    'ghunt': ToolConfig('GHUNT', ToolCategory.OSINT_RASTREO, 'Investigacion cuentas Google (email, telefono, YouTube, Drive, Fotos)',
        command='ghunt', parameters={'modules': ['email', 'phone', 'youtube', 'drive', 'photos']}),
    'toutatis': ToolConfig('TOUTATIS', ToolCategory.OSINT_RASTREO, 'Investigacion cuentas Facebook/Instagram (OSINT social media)',
        command='toutatis', parameters={'modules': ['profile', 'friends', 'posts', 'photos', 'pages']}),
}

OPSEC_TOOLS = {
    'pihole': ToolConfig('Pi-hole', ToolCategory.OPSEC_PRIVACIDAD, 'Bloqueo DNS a nivel de red',
        command='pihole', api_endpoint='http://pihole.local/admin/api.php'),
    'vopono': ToolConfig('Vopono', ToolCategory.OPSEC_BLINDAJE, 'VPN multi-hop WireGuard',
        command='vopono', parameters={'hops': 3, 'countries': ['CH', 'IS', 'FI']}),
    'simplelogin': ToolConfig('SimpleLogin', ToolCategory.OPSEC_PRIVACIDAD, 'Alias de email',
        api_endpoint='https://api.simplelogin.io/v2', api_key_env='SIMPLELOGIN_API_KEY'),
    'grapheneos': ToolConfig('GrapheneOS', ToolCategory.OPSEC_BLINDAJE, 'OS movil endurecido',
        command='grapheneos-audit'),
    'mvt_project': ToolConfig('MVT Project', ToolCategory.OPSEC_PRIVACIDAD, 'Deteccion spyware Pegasus',
        command='mvt'),
    'airguard': ToolConfig('AirGuard', ToolCategory.OPSEC_PRIVACIDAD, 'Deteccion trackers Bluetooth',
        command='airguard'),
    'peakvault': ToolConfig('PeakVault', ToolCategory.OPSEC_BLINDAJE, 'Boveda post-cuantica',
        command='peakvault', api_endpoint='https://api.peakvault.io/v1', api_key_env='PEAKVAULT_API_KEY'),
    'imagine_scrubber': ToolConfig('Imagine Scrubber', ToolCategory.OPSEC_PRIVACIDAD, 'Limpieza metadatos EXIF',
        command='imagine-scrubber'),
    'fawkes': ToolConfig('Fawkes', ToolCategory.OPSEC_BLINDAJE, 'Anti-reconocimiento facial',
        command='fawkes'),
    'cover_your_tracks': ToolConfig('Cover Your Tracks', ToolCategory.OPSEC_PRIVACIDAD, 'Test huella navegador',
        command='coveryourtracks', api_endpoint='https://coveryourtracks.eff.org/api/v1'),
    'mailacces': ToolConfig('Mailacces', ToolCategory.OPSEC_PRIVACIDAD, 'Monitor filtraciones',
        api_endpoint='https://api.mailacces.com/v1', api_key_env='MAILACCES_API_KEY'),
    'anonymity': ToolConfig('Anonymity Tor', ToolCategory.OPSEC_BLINDAJE, 'Red Tor hardened',
        command='anonymity-tor'),
    'ublock_origin': ToolConfig('uBlock Origin', ToolCategory.OPSEC_PRIVACIDAD, 'Bloqueador contenido',
        command='ublock-origin'),
}

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.executors = {}
        self._load_all_tools()

    def _load_all_tools(self):
        for tid, cfg in OSINT_TOOLS.items():
            self.tools[tid] = cfg
        for tid, cfg in OPSEC_TOOLS.items():
            self.tools[tid] = cfg
        logger.info(f'[ToolRegistry] Cargadas {len(self.tools)} herramientas')

    def get_tool(self, tool_id: str) -> Optional[ToolConfig]:
        return self.tools.get(tool_id)

    def get_tools_by_category(self, category: ToolCategory) -> List[ToolConfig]:
        return [t for t in self.tools.values() if t.category == category]

    def register_executor(self, tool_id: str, executor: Callable):
        self.executors[tool_id] = executor

    async def execute_tool(self, tool_id: str, params: Dict[str, Any] = None) -> ToolResult:
        import time
        start = time.perf_counter()
        tool = self.get_tool(tool_id)
        if not tool:
            return ToolResult(tool_name=tool_id, success=False, error=f'No encontrada: {tool_id}',
                execution_time_ms=(time.perf_counter()-start)*1000)
        if tool_id in self.executors:
            try:
                result = await self.executors[tool_id](params or {})
                result.execution_time_ms = (time.perf_counter()-start)*1000
                return result
            except Exception as e:
                return ToolResult(tool_name=tool_id, success=False, error=str(e),
                    execution_time_ms=(time.perf_counter()-start)*1000)
        await asyncio.sleep(0.1)
        return ToolResult(tool_name=tool_id, success=True, data={'status': 'simulated'},
            execution_time_ms=(time.perf_counter()-start)*1000)

    def get_status_summary(self) -> Dict[str, Any]:
        by_cat = {}
        for cat in ToolCategory:
            tools = self.get_tools_by_category(cat)
            by_cat[cat.value] = {'total': len(tools), 'enabled': sum(1 for t in tools if t.enabled), 'tools': [t.name for t in tools]}
        return {'total_tools': len(self.tools), 'enabled_tools': sum(1 for t in self.tools.values() if t.enabled), 'by_category': by_cat}

tool_registry = ToolRegistry()

def get_tool_registry() -> ToolRegistry:
    return tool_registry
