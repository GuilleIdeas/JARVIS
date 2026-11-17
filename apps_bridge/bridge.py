# JARVIS ECC - Bridge API
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, Callable
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import logging
import hmac
import hashlib
import time
import uuid

logger = logging.getLogger(__name__)


class BridgeEndpoint(str, Enum):
    TRADING = "trading"
    WHATSAPP = "whatsapp"
    SIGNAL = "signal"
    JARVIS_APPS = "jarvis_apps"


@dataclass
class BridgeConfig:
    endpoint: BridgeEndpoint
    name: str
    base_url: str
    api_key: Optional[str] = None
    secret: Optional[str] = None
    enabled: bool = True
    rate_limit: int = 100
    timeout: int = 30


class BridgeRequest(BaseModel):
    action: str
    payload: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}


class BridgeResponse(BaseModel):
    success: bool
    data: Any = None
    error: Optional[str] = None
    request_id: str
    timestamp: float


class AppBridge:
    def __init__(self):
        self.endpoints = {}
        self.handlers = {}
        self._setup()
    
    def _setup(self):
        self.endpoints = {
            BridgeEndpoint.TRADING: BridgeConfig(BridgeEndpoint.TRADING, "Trading Propietaria", "http://localhost:9821"),
            BridgeEndpoint.WHATSAPP: BridgeConfig(BridgeEndpoint.WHATSAPP, "WhatsApp", "https://graph.facebook.com/v18.0"),
            BridgeEndpoint.SIGNAL: BridgeConfig(BridgeEndpoint.SIGNAL, "Signal", "http://localhost:8080"),
            BridgeEndpoint.JARVIS_APPS: BridgeConfig(BridgeEndpoint.JARVIS_APPS, "JARVIS Apps", "http://localhost:8001"),
        }
    
    def register_endpoint(self, config):
        self.endpoints[config.endpoint] = config
    
    def register_handler(self, endpoint, action, handler):
        self.handlers[f"{endpoint.value}.{action}"] = handler
    
    def get_endpoint(self, endpoint):
        return self.endpoints.get(endpoint)
    
    def verify_signature(self, endpoint, payload, signature):
        config = self.get_endpoint(endpoint)
        if not config or not config.secret:
            return True
        expected = hmac.new(config.secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
    
    async def call_endpoint(self, endpoint, action, payload):
        import httpx
        config = self.get_endpoint(endpoint)
        if not config or not config.enabled:
            return BridgeResponse(success=False, error=f"Endpoint no disponible: {endpoint.value}", request_id=str(uuid.uuid4())[:8], timestamp=time.time())
        key = f"{endpoint.value}.{action}"
        if key in self.handlers:
            try:
                result = await self.handlers[key](payload)
                return BridgeResponse(success=True, data=result, request_id=str(uuid.uuid4())[:8], timestamp=time.time())
            except Exception as e:
                return BridgeResponse(success=False, error=str(e), request_id=str(uuid.uuid4())[:8], timestamp=time.time())
        return BridgeResponse(success=True, data={"status": "forwarded"}, request_id=str(uuid.uuid4())[:8], timestamp=time.time())
    
    def get_status(self):
        return {ep.value: {"name": cfg.name, "enabled": cfg.enabled} for ep, cfg in self.endpoints.items()}


_bridge_instance = None
def get_bridge():
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = AppBridge()
    return _bridge_instance


bridge_router = APIRouter(prefix="/api/bridge", tags=["bridge"])

@bridge_router.get("/status")
async def bridge_status():
    return get_bridge().get_status()

@bridge_router.post("/{endpoint}/{action}", response_model=BridgeResponse)
async def bridge_call(endpoint: BridgeEndpoint, action: str, request: BridgeRequest, x_signature: Optional[str] = Header(None)):
    return await get_bridge().call_endpoint(endpoint, action, request.payload)