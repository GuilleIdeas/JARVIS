with open('/workspaces/JARVIS/main.py', 'r') as f:
    lines = f.readlines()

# Fix line 231 (index 230) - the chat_script replacement
lines[230] = "        content = content.replace('</body>', chat_script + '\\n</body>')\n"

# Remove the broken next line
if len(lines) > 231 and '</body>')' in lines[231]:
    lines.pop(231)

with open('/workspaces/JARVIS/main.py', 'w') as f:
    f.writelines(lines)

print('Fixed')