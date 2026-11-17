with open('/workspaces/JARVIS/core/jarvis_core.py', 'r') as f:
    lines = f.readlines()

# Fix lines 311-323
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if i == 310:  # line 311 (0-indexed 310)
        new_lines.append('        directors_context = "\\n\\n".join([\n')
    elif i == 311:
        new_lines.append('            f"=== {inv.director.value.upper()} ===\\n{inv.response}"\n')
    elif i == 312:
        new_lines.append('            for inv in invocations if inv.success\n')
    elif i == 313:
        new_lines.append('        ])\n')
    elif i == 314:
        new_lines.append('        messages = [\n')
    elif i == 315:
        new_lines.append('            {"role": "system", "content": self.SYNTHESIS_SYSTEM_PROMPT},\n')
    elif i == 316:
        new_lines.append('            {"role": "user", "content": f"CONSULTA ORIGINAL: {user_query}\\n\\nRESPUESTAS DE DIRECTORES:\\n{directors_context}"}\n')
    elif i == 317:
        new_lines.append('        ]\n')
    else:
        new_lines.append(line)
    i += 1

with open('/workspaces/JARVIS/core/jarvis_core.py', 'w') as f:
    f.writelines(new_lines)

print('Fixed')