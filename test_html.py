import uvicorn
from main import app
import asyncio
import httpx
import re

async def test():
    config = uvicorn.Config(app, host='0.0.0.0', port=8004, log_level='warning')
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())
    await asyncio.sleep(2)
    
    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:8004/')
        html = r.text
        print('Has <div id=app>:', 'id="app"' in html)
        print('Has <script type=module:', 'type="module"' in html)
        print('Has app.js:', 'app.js' in html)
        print('Has renderer.js import:', 'renderer.js' in html)
        print('Has Tailwind CDN:', 'tailwindcss.com' in html)
        print('Has material-symbols:', 'material-symbols' in html)
        print('---')
        scripts = re.findall(r'<script[^>]*>.*?</script>', html, re.DOTALL)
        for s in scripts:
            print('Script tag:', s[:300])
    
    server.should_exit = True
    await task

asyncio.run(test())