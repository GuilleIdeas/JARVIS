with open('/workspaces/JARVIS/core/jarvis_core.py', 'r') as f:
    lines = f.readlines()

# Fix line 340 (0-indexed 339) - write with proper escaped newlines
lines[339] = '            detailed = "## RESPUESTAS DIRECTAS\\n\\n" + directors_context\n'

with open('/workspaces/JARVIS/core/jarvis_core.py', 'w') as f:
    f.writelines(lines)

print('Fixed line 340')