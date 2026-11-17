# ============================================
# JARVIS ECC - NÚCLEO ORQUESTADOR PRINCIPAL (Parte 1)
# ============================================

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, AsyncGenerator, Dict, List, Optional, Set
from loguru import logger

from openai import AsyncOpenAI
from core.config import settings, get_settings


class ModelProvider(str, Enum):
    NVIDIA = 'nvidia'
    OPENROUTER = 'openrouter'


class DirectorRole(str, Enum):
    INGENIERIA_SOFTWARE = 'ingenieria_software'
    TRADING_MERCADOS = 'trading_mercados'
    FINANZAS_CONTABILIDAD = 'finanzas_contabilidad'
    GEOPOLITICA_CULTURA = 'geopolitica_cultura'
    CONSEJO_CIENTIFICO = 'consejo_cientifico'
    DATOS_PATRONES = 'datos_patrones'
    MARKETING_VENTAS = 'marketing_ventas'
    SEGURIDAD_CIBERSEGURIDAD = 'seguridad_ciberseguridad'


@dataclass
class DirectorInvocation:
    director: DirectorRole
    prompt: str
    response: str
    tokens_used: int
    latency_ms: float
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error: Optional[str] = None


@dataclass
class ExecutiveResponse:
    request_id: str
    user_query: str
    executive_summary: str
    detailed_response: str
    active_directors: List[DirectorRole]
    director_invocations: List[DirectorInvocation]
    model_used: str
    provider: ModelProvider
    total_tokens: int
    total_latency_ms: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class JarvisCore:
    """
    Núcleo Orquestador de JARVIS ECC.
    
    Responsabilidades:
    - Conectar a NVIDIA Build (Nemotron 3 Ultra) como modelo principal
    - Respaldo automático a OpenRouter si falla NVIDIA
    - Analizar cada solicitud en español
    - Delegar tareas a Directores ECC según el tema
    - Sintetizar respuesta ejecutiva unificada indicando qué áreas intervinieron
    """
    
    CLASSIFIER_SYSTEM_PROMPT = """Eres el CLASIFICADOR DEL CONSEJO EJECUTIVO ECC de JARVIS.
Tu misión: Analizar la consulta del usuario en español y determinar QUÉ DIRECTORES ECC deben intervenir.

DIRECTORES DISPONIBLES:
1. INGENIERIA_SOFTWARE - Desarrollo, arquitectura, auditoría de código, fábrica de apps, CI/CD, DevOps
2. TRADING_MERCADOS - Trading cuantitativo, análisis técnico, cripto, forex, bolsas, HFT, derivados
3. FINANZAS_CONTABILIDAD - Finanzas corporativas, contabilidad, inversión, proyectos, emprendimiento, fiscalidad
4. GEOPOLITICA_CULTURA - Política internacional, geopolítica, religión, cultura, análisis por países, riesgo país
5. CONSEJO_CIENTIFICO - Matemáticas, física, sociología, ciencias duras, investigación, metodología científica
6. DATOS_PATRONES - Análisis de datos, big data, patrones, ML/IA, inteligencia estratégica, OSINT
7. MARKETING_VENTAS - Marketing digital, ventas, e-commerce, growth hacking, algoritmos redes sociales, branding
8. SEGURIDAD_CIBERSEGURIDAD - Seguridad física, OpSec, ciberseguridad, hardening, privacidad, cumplimiento

REGLAS:
- Selecciona 1-3 directores MÁS RELEVANTES (no todos)
- Considera la naturaleza principal de la consulta
- Si es ambigua, elige el director más probable + uno de apoyo
- Responde SOLO con un JSON válido: {"directors": ["ROL1", "ROL2"], "reasoning": "breve justificación", "confidence": 0.95}"""

    SYNTHESIS_SYSTEM_PROMPT = """Eres el SINTETIZADOR EJECUTIVO DEL CONSEJO ECC de JARVIS.
Tu misión: Recibir las respuestas de los Directores ECC y producir una RESPUESTA EJECUTIVA UNIFICADA.

FORMATO DE SALIDA REQUERIDO:
## RESUMEN EJECUTIVO
[2-3 párrafos concisos en español ejecutivo, lenguaje directo, sin florituras]

## ANÁLISIS POR ÁREA
### [NOMBRE DIRECTOR 1]
[Síntesis de su aportación clave - 2-3 líneas]

### [NOMBRE DIRECTOR 2]
[Síntesis de su aportación clave - 2-3 líneas]

## RECOMENDACIONES ACCIONABLES
1. [Acción concreta 1]
2. [Acción concreta 2]
3. [Acción concreta 3]

## MÉTRICAS DE CONFIANZA
- Directores consultados: [lista]
- Consenso: [Alto/Medio/Bajo]
- Riesgos identificados: [lista breve]

REGLAS:
- Español ejecutivo, tono profesional militar/empresarial
- NO repitas información, SINTETIZA
- Prioriza lo accionable y estratégico
- Indica claramente desacuerdos entre directores si los hay"""

    def __init__(self):
        self.settings = get_settings()
        self._nvidia_client = None
        self._openrouter_client = None
        self._initialized = False
        self.stats = {
            'total_requests': 0,
            'nvidia_success': 0,
            'openrouter_fallback': 0,
            'errors': 0,
            'avg_latency_ms': 0.0
        }
    
    async def initialize(self):
        if self._initialized:
            return
        if self.settings.has_nvidia_key:
            self._nvidia_client = AsyncOpenAI(
                api_key=self.settings.nvidia_api_key,
                base_url=self.settings.nvidia_base_url,
                timeout=self.settings.request_timeout
            )
            logger.info('[JARVIS] Cliente NVIDIA Build inicializado (Nemotron 3 Ultra)')
        else:
            logger.warning('[JARVIS] NVIDIA_API_KEY no configurada - se usará OpenRouter como principal')
        
        if self.settings.has_openrouter_key:
            self._openrouter_client = AsyncOpenAI(
                api_key=self.settings.openrouter_api_key,
                base_url=self.settings.openrouter_base_url,
                timeout=self.settings.request_timeout
            )
            logger.info('[JARVIS] Cliente OpenRouter inicializado (respaldo)')
        else:
            logger.warning('[JARVIS] OPENROUTER_API_KEY no configurada - sin respaldo automático')
        
        if not self._nvidia_client and not self._openrouter_client:
            raise RuntimeError('JARVIS requiere al menos NVIDIA_API_KEY u OPENROUTER_API_KEY')
        self._initialized = True

    async def _get_primary_client(self):
        if self._nvidia_client:
            return self._nvidia_client, ModelProvider.NVIDIA, self.settings.nvidia_model
        elif self._openrouter_client:
            return self._openrouter_client, ModelProvider.OPENROUTER, self.settings.openrouter_fallback_models_list[0]
        raise RuntimeError('No hay clientes disponibles')
    
    async def _get_fallback_client(self, exclude_provider):
        if exclude_provider != ModelProvider.OPENROUTER and self._openrouter_client:
            return self._openrouter_client, ModelProvider.OPENROUTER, self.settings.openrouter_fallback_models_list[0]
        if exclude_provider != ModelProvider.NVIDIA and self._nvidia_client:
            return self._nvidia_client, ModelProvider.NVIDIA, self.settings.nvidia_model
        return None

    async def _chat_completion(self, client, model, messages, temperature=None, max_tokens=None, stream=False):
        return await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature or self.settings.temperature,
            max_tokens=max_tokens or self.settings.max_tokens,
            top_p=self.settings.top_p,
            stream=stream
        )
    
    async def _stream_completion(self, client, model, messages):
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
            top_p=self.settings.top_p,
            stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def classify_directors(self, user_query: str):
        await self.initialize()
        client, provider, model = await self._get_primary_client()
        messages = [
            {'role': 'system', 'content': self.CLASSIFIER_SYSTEM_PROMPT},
            {'role': 'user', 'content': f'CONSULTA: {user_query}'}
        ]
        try:
            response = await self._chat_completion(client, model, messages, temperature=0.1, max_tokens=500)
            result = json.loads(response.choices[0].message.content)
            directors = [DirectorRole(d) for d in result.get('directors', [])]
            reasoning = result.get('reasoning', '')
            confidence = float(result.get('confidence', 0.8))
            valid_directors = [d for d in directors if d in DirectorRole]
            if not valid_directors:
                valid_directors = self._fallback_classification(user_query)
                reasoning = 'Clasificación por palabras clave (fallback)'
                confidence = 0.6
            return valid_directors[:3], reasoning, confidence
        except Exception as e:
            logger.error(f'[JARVIS] Error en clasificación: {e}')
            fallback = self._fallback_classification(user_query)
            return fallback, f'Error en clasificación LLM: {str(e)[:100]}', 0.5

    def _fallback_classification(self, query: str):
        query_lower = query.lower()
        scores = {}
        keywords = {
            DirectorRole.INGENIERIA_SOFTWARE: ['código', 'programa', 'app', 'aplicación', 'software', 'desarrollo', 'api', 'script', 'bug', 'refactor', 'arquitectura', 'ci/cd', 'deploy', 'docker', 'kubernetes', 'git'],
            DirectorRole.TRADING_MERCADOS: ['trading', 'bolsa', 'cripto', 'crypto', 'bitcoin', 'ethereum', 'forex', 'acciones', 'futuros', 'opciones', 'análisis técnico', 'indicador', 'oscila', 'velas', 'orderbook', 'liquidez', 'hedge', 'arbitraje', 'quant', 'hft'],
            DirectorRole.FINANZAS_CONTABILIDAD: ['finanzas', 'contabilidad', 'balance', 'pérdidas', 'ganancias', 'flujo caja', 'inversión', 'proyecto', 'emprendimiento', 'fiscal', 'impuestos', 'iva', 'irpf', 'sociedades', 'valuation', 'capex', 'opex'],
            DirectorRole.GEOPOLITICA_CULTURA: ['geopolítica', 'política', 'país', 'guerra', 'conflicto', 'sanciones', 'onu', 'otan', 'brasil', 'china', 'eeuu', 'rusia', 'oriente medio', 'religión', 'cultura', 'riesgo país'],
            DirectorRole.CONSEJO_CIENTIFICO: ['matemática', 'física', 'sociología', 'ciencia', 'investigación', 'teorema', 'ecuación', 'modelo', 'simulación', 'estadística', 'probabilidad', 'álgebra', 'cálculo', 'termodinámica'],
            DirectorRole.DATOS_PATRONES: ['datos', 'análisis', 'patrón', 'machine learning', 'ia', 'inteligencia artificial', 'big data', 'osint', 'inteligencia', 'scraping', 'minería', 'clustering', 'regresión', 'predicción'],
            DirectorRole.MARKETING_VENTAS: ['marketing', 'ventas', 'ecommerce', 'e-commerce', 'seo', 'sem', 'redes sociales', 'instagram', 'tiktok', 'linkedin', 'growth', 'conversión', 'funnel', 'lead', 'cliente', 'branding', 'publicidad'],
            DirectorRole.SEGURIDAD_CIBERSEGURIDAD: ['seguridad', 'ciberseguridad', 'opsec', 'hardening', 'privacidad', 'anonymity', 'tor', 'vpn', 'firewall', 'pentest', 'vulnerabilidad', 'exploit', 'malware', 'phishing', 'cifrado', 'pci', 'iso']
        }
        for director, kws in keywords.items():
            score = sum(1 for kw in kws if kw in query_lower)
            if score > 0:
                scores[director] = score
        if not scores:
            return [DirectorRole.INGENIERIA_SOFTWARE]
        sorted_directors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [d for d, _ in sorted_directors[:2]]

    async def invoke_director(self, director, user_query, context=''):
        await self.initialize()
        from ecc_directors import get_director_prompt
        system_prompt = get_director_prompt(director)
        full_prompt = (
            f"CONSULTA DEL USUARIO: {user_query}\n\n"
            f"CONTEXTO ADICIONAL: {context if context else 'Ninguno'}\n\n"
            f"INSTRUCCIONES: Responde como {director.value.replace('_', ' ').title()}. "
            "Proporciona análisis experto, recomendaciones concretas y nivel de confianza. "
            "Sé directo, técnico y accionable."
        )
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': full_prompt}
        ]
        start_time = time.perf_counter()
        client, provider, model = await self._get_primary_client()
        try:
            response = await self._chat_completion(client, model, messages)
            latency_ms = (time.perf_counter() - start_time) * 1000
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens if response.usage else 0
            return DirectorInvocation(
                director=director,
                prompt=full_prompt[:500],
                response=content,
                tokens_used=tokens,
                latency_ms=latency_ms,
                success=True
            )
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f'[JARVIS] Error invocando director {director}: {e}')
            fallback = await self._get_fallback_client(provider)
            if fallback:
                fb_client, fb_provider, fb_model = fallback
                try:
                    response = await self._chat_completion(fb_client, fb_model, messages)
                    latency_ms = (time.perf_counter() - start_time) * 1000
                    content = response.choices[0].message.content
                    tokens = response.usage.total_tokens if response.usage else 0
                    self.stats['openrouter_fallback'] += 1
                    return DirectorInvocation(
                        director=director,
                        prompt=full_prompt[:500],
                        response=f'[RESPALDO {fb_provider.value.upper()}] {content}',
                        tokens_used=tokens,
                        latency_ms=latency_ms,
                        success=True
                    )
                except Exception as e2:
                    logger.error(f'[JARVIS] Fallback también falló para {director}: {e2}')
            return DirectorInvocation(
                director=director,
                prompt=full_prompt[:500],
                response=f'ERROR: {str(e)[:200]}',
                tokens_used=0,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )

    async def synthesize_response(self, user_query, invocations):
        await self.initialize()
        directors_context = "\n\n".join([
            f"=== {inv.director.value.upper()} ===\n{inv.response}"
            for inv in invocations if inv.success
        ])
        messages = [
            {"role": "system", "content": self.SYNTHESIS_SYSTEM_PROMPT},
            {"role": "user", "content": f"CONSULTA ORIGINAL: {user_query}\n\nRESPUESTAS DE DIRECTORES:\n{directors_context}"}
        ]
        client, provider, model = await self._get_primary_client()
        try:
            response = await self._chat_completion(client, model, messages)
            content = response.choices[0].message.content
            parts = content.split('## ANÁLISIS POR ÁREA')
            executive_summary = parts[0].replace('## RESUMEN EJECUTIVO', '').strip()
            detailed_response = '## ANÁLISIS POR ÁREA' + parts[1] if len(parts) > 1 else content
            return executive_summary, detailed_response
        except Exception as e:
            logger.error(f'[JARVIS] Error en síntesis: {e}')
            fallback = await self._get_fallback_client(provider)
            if fallback:
                fb_client, fb_provider, fb_model = fallback
                try:
                    response = await self._chat_completion(fb_client, fb_model, messages)
                    content = response.choices[0].message.content
                    parts = content.split('## ANÁLISIS POR ÁREA')
                    return parts[0].replace('## RESUMEN EJECUTIVO', '').strip(), content
                except Exception:
                    pass
            summary = f"Análisis completado por {len(invocations)} director(es). Ver detalles abajo."
            detailed = "## RESPUESTAS DIRECTAS\n\n" + directors_context


            return summary, detailed

    async def process_request(self, user_query, context='', stream=False):
        request_id = str(uuid.uuid4())[:8]
        start_total = time.perf_counter()
        self.stats['total_requests'] += 1
        logger.info(f'[JARVIS:{request_id}] Nueva consulta: {user_query[:100]}')
        
        directors, reasoning, confidence = await self.classify_directors(user_query)
        logger.info(f'[JARVIS:{request_id}] Directores: {[d.value for d in directors]} (confianza: {confidence:.0%})')
        
        invocation_tasks = [self.invoke_director(d, user_query, context) for d in directors]
        invocations = await asyncio.gather(*invocation_tasks, return_exceptions=True)
        
        valid_invocations = []
        for i, inv in enumerate(invocations):
            if isinstance(inv, Exception):
                logger.error(f'[JARVIS:{request_id}] Excepción en director {directors[i]}: {inv}')
                valid_invocations.append(DirectorInvocation(
                    director=directors[i], prompt='',
                    response=f'ERROR INTERNO: {str(inv)[:200]}',
                    tokens_used=0, latency_ms=0, success=False, error=str(inv)
                ))
            else:
                valid_invocations.append(inv)
        
        executive_summary, detailed_response = await self.synthesize_response(user_query, valid_invocations)
        
        total_latency = (time.perf_counter() - start_total) * 1000
        total_tokens = sum(inv.tokens_used for inv in valid_invocations)
        active_directors = [inv.director for inv in valid_invocations if inv.success]
        
        self.stats['avg_latency_ms'] = (
            (self.stats['avg_latency_ms'] * (self.stats['total_requests'] - 1) + total_latency)
            / self.stats['total_requests']
        )
        if any(inv.success for inv in valid_invocations):
            self.stats['nvidia_success'] += 1
        else:
            self.stats['errors'] += 1
        
        provider = ModelProvider.NVIDIA if self._nvidia_client else ModelProvider.OPENROUTER
        model_used = self.settings.nvidia_model if provider == ModelProvider.NVIDIA else self.settings.openrouter_fallback_models_list[0]
        
        return ExecutiveResponse(
            request_id=request_id,
            user_query=user_query,
            executive_summary=executive_summary,
            detailed_response=detailed_response,
            active_directors=active_directors,
            director_invocations=valid_invocations,
            model_used=model_used,
            provider=provider,
            total_tokens=total_tokens,
            total_latency_ms=total_latency,
            metadata={
                'classification_reasoning': reasoning,
                'classification_confidence': confidence,
                'directors_requested': [d.value for d in directors]
            }
        )

    async def process_stream(self, user_query, context=''):
        response = await self.process_request(user_query, context)
        yield {'type': 'metadata', 'request_id': response.request_id, 'active_directors': [d.value for d in response.active_directors], 'model': response.model_used, 'provider': response.provider.value}
        yield {'type': 'executive_summary_start'}
        for chunk in response.executive_summary.split():
            yield {'type': 'executive_summary_chunk', 'content': chunk + ' '}
            await asyncio.sleep(0.02)
        yield {'type': 'executive_summary_end'}
        yield {'type': 'detailed_start'}
        for chunk in response.detailed_response.split():
            yield {'type': 'detailed_chunk', 'content': chunk + ' '}
            await asyncio.sleep(0.01)
        yield {'type': 'detailed_end'}
        yield {'type': 'complete', 'total_tokens': response.total_tokens, 'latency_ms': response.total_latency_ms}

    def get_stats(self):
        return {
            **self.stats,
            'nvidia_configured': self.settings.has_nvidia_key,
            'openrouter_configured': self.settings.has_openrouter_key,
            'primary_model': self.settings.nvidia_model if self.settings.has_nvidia_key else 'OpenRouter',
            'fallback_models': self.settings.openrouter_fallback_models_list
        }


_jarvis_core = None

def get_jarvis_core():
    global _jarvis_core
    if _jarvis_core is None:
        _jarvis_core = JarvisCore()
    return _jarvis_core

async def initialize_jarvis():
    core = get_jarvis_core()
    await core.initialize()
    return core
