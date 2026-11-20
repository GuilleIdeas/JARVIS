# CONSTITUCIÓN MAESTRA DEL SISTEMA: JARVIS
## 1. VISIÓN Y PROPÓSITO DEL PROYECTO
- **Nombre Oficial:** JARVIS (no usar siglas extra como "ECC" en el título principal de la interfaz).
- **Alcance:** Centro de Mando Ejecutivo, Inteligencia Global, Investigación OSINT, Blindaje OpSec, Análisis Jurídico/Económico y Fábrica Autónoma de Software, diseñado estrictamente para uso personal del Comandante.
- **Motores de IA:**
  - Constructor de código (Cline): `google/gemma-4-31b-it` (NVIDIA Build).
  - Cerebro Central de JARVIS (`jarvis_core.py`): `nvidia/nemotron-3-ultra-550b-a55b` (NVIDIA Build) con respaldo automático en OpenRouter.

## 2. ARQUITECTURA DE LAS 12 DIVISIONES OPERATIVAS (`/divisions/`)
Cada división debe ser un módulo independiente en Python con un especialista IA dedicado y herramientas reales:
1. **JARVIS (Sala Privada):** Consola directa de interacción (Web, App Móvil, WhatsApp, Signal) para hablar, estudiar, analizar y organizarse con acceso transversal a todo el sistema.
2. **MUNDO (Vigilancia Global):** Monitoreo geoespacial y telemetría en vivo integrando **Argos Atlas**, **God's Eye View (WorldView 3D)**, **OSIRIS**, **Airplanes-live**, **Marine Traffic**, **Insecam** y alertas globales.
3. **CONSEJO (Sala de Situación):** Debate interdisciplinario entre directores de Geopolítica, Política, Religión, Cultura y sectores estratégicos (Inmobiliario, Agropecuario, Minero e Hidrocarburos) para anticipar escenarios y detectar oportunidades.
4. **INVESTIGACIÓN (OSINT Interconectado):** Rastreo profundo de personas, empresas, dominios y redes integrando **Horus**, **Flowsint**, **GHunt**, **Toutatis**, **FaceCheck.ID**, **Shodan Images**, **Wordmonitor**, **Alien_eyes**, **Ghost-Track**, **Deanonymizer** y **Open Planter**.
5. **SEGURIDAD (Blindaje Integral):** Protección física, operacional y ciberseguridad/OpSec para mantener a JARVIS libre de fugas e intrusiones, monitoreando **Pi-hole**, **Vopono**, **SimpleLogin**, **GrapheneOS**, **MVT-Project**, **AirGuard**, **PeakVault**, **Imagine-scrubber**, **Fawkes**, **Cover Your Tracks (EFF)**, **Mailacces**, **Anonymity** y **uBlock Origin**.
6. **JURÍDICO (Leyes y Países):** Experto legal corporativo, mercantil, financiero y regulatorio alimentado con códigos legales y normativas por país/jurisdicción.
7. **ECONOMÍA (Unificada en 2 Sub-divisiones):**
   - **7.1 Finanzas:** Macroeconomía, análisis fundamental e institucional, acciones, ETFs, bonos, holdings, proyectos a largo plazo y contabilidad.
   - **7.2 Trading:** Gestión algorítmica y control de riesgo (Futuros, Margen y Opciones en Bolsa, Forex y Cripto) conectado vía API (`/apps_bridge/`) a mi App de Trading Propietaria (sistema externo), solicitando siempre mi autorización antes de operar.
8. **FÁBRICA (Ingeniería y Software):** Director de Ingeniería de Software y taller autónomo para diseñar, programar, auditar y desplegar nuevas aplicaciones y scripts.
9. **NEGOCIOS (Empresas y E-Commerce):** Gestión ejecutiva de emprendimientos, empresas, tiendas digitales, ventas y operaciones comerciales.
10. **MARKETING (Redes y Cultura):** Estrategia de marca, algoritmos de redes sociales, crecimiento digital y batalla cultural.
11. **CIENCIA (Laboratorio e I+D):** Consejo científico completo (Matemática, Física, Sociología y ciencias aplicadas) + análisis de datos y patrones.
12. **CEREBRO (Graphify Visual):** Red neuronal interactiva (2D/3D) dividida por bóvedas temáticas que interconecta nodos, investigaciones, leyes, eventos e impactos en tiempo real.

## 3. REGLAS DE DISEÑO Y FUNCIONALIDAD
- **Inspiración Visual:** Tomar como base estética los archivos originales de Google Stitch en el repositorio (estilo Dark Neon espacial / Tron / Iron Man HUD: fondo `#04070D`, bordes cian neón `#00F3FF`, azul eléctrico `#0066FF` y acentos magenta `#B026FF`), adaptando la estructura para albergar las 12 divisiones con paridad entre Escritorio y Móvil.
- **Cero Botones Muertos:** Cada botón de división, pestaña, buscador, micrófono y consola de chat debe ejecutar lógica real conectada al backend en FastAPI (`main.py`).
