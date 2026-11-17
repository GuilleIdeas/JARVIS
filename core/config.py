# ============================================
# JARVIS ECC - CONFIGURACIÓN CENTRAL
# ============================================

from functools import lru_cache
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración central de JARVIS ECC usando Pydantic Settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # --- NVIDIA Build ---
    nvidia_api_key: str = Field(default="", alias="NVIDIA_API_KEY")
    nvidia_base_url: str = Field(default="https://integrate.api.nvidia.com/v1", alias="NVIDIA_BASE_URL")
    nvidia_model: str = Field(default="nvidia/nemotron-3-ultra-550b-a55b", alias="NVIDIA_MODEL")
    
    # --- OpenRouter ---
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL")
    openrouter_fallback_models: str = Field(default="openrouter/auto,openrouter/claude-3.5-sonnet,openrouter/gpt-4o", alias="OPENROUTER_FALLBACK_MODELS")
    
    # --- Servidor ---
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # --- Modelos ---
    default_model: str = Field(default="nvidia/nemotron-3-ultra", alias="DEFAULT_MODEL")
    max_tokens: int = Field(default=8192, alias="MAX_TOKENS")
    temperature: float = Field(default=0.3, alias="TEMPERATURE")
    top_p: float = Field(default=0.9, alias="TOP_P")
    stream: bool = Field(default=True, alias="STREAM")
    
    # --- Timeouts ---
    request_timeout: int = Field(default=120, alias="REQUEST_TIMEOUT")
    ws_heartbeat_interval: int = Field(default=30, alias="WS_HEARTBEAT_INTERVAL")
    ws_reconnect_max_attempts: int = Field(default=5, alias="WS_RECONNECT_MAX_ATTEMPTS")
    
    # --- Seguridad ---
    cors_origins: str = Field(default="http://localhost:8000,http://127.0.0.1:8000", alias="CORS_ORIGINS")
    rate_limit_requests: int = Field(default=100, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, alias="RATE_LIMIT_WINDOW")
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def openrouter_fallback_models_list(self) -> List[str]:
        return [model.strip() for model in self.openrouter_fallback_models.split(",")]
    
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"
    
    @property
    def has_nvidia_key(self) -> bool:
        return bool(self.nvidia_api_key and self.nvidia_api_key != "tu_nvidia_api_key_aqui")
    
    @property
    def has_openrouter_key(self) -> bool:
        return bool(self.openrouter_api_key and self.openrouter_api_key != "tu_openrouter_api_key_aqui")


@lru_cache
def get_settings() -> Settings:
    """Obtiene la configuración cacheada (singleton)."""
    return Settings()


# Configuración global accesible
settings = get_settings()