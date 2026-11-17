with open('/workspaces/JARVIS/core/jarvis_core.py', 'r') as f:
    content = f.read()

# Fix the unterminated f-strings
content = content.replace(
    "summary = f'Análisis completado por {len(invocations)} director(es). Ver detalles abajo.'",
    'summary = f"Análisis completado por {len(invocations)} director(es). Ver detalles abajo."'
)
content = content.replace(
    "detailed = f'## RESPUESTAS DIRECTAS\n\n{directors_context}'",
    'detailed = f"## RESPUESTAS DIRECTAS\n\n{directors_context}"'
)

with open('/workspaces/JARVIS/core/jarvis_core.py', 'w') as f:
    f.write(content)

print('Fixed f-strings')