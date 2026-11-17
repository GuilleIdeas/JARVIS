with open('/workspaces/JARVIS/main.py', 'r') as f:
    lines = f.readlines()

# Fix line 231 (index 230)
lines[230] = "        content = content.replace('</body>', chat_script + '\\\\n</body>')\n"

with open('/workspaces/JARVIS/main.py', 'w') as f:
    f.writelines(lines)

print('Fixed')