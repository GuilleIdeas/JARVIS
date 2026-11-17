with open('/workspaces/JARVIS/main.py', 'r') as f:
    content = f.read()

# Fix the problematic line
content = content.replace(
    "        content = content.replace('</body>', chat_script + '\\n\"\n</body>')",
    "        content = content.replace('</body>', chat_script + '\\n</body>')"
)

with open('/workspaces/JARVIS/main.py', 'w') as f:
    f.write(content)

print('Fixed')