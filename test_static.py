import uvicorn
from main import app
import asyncio
import httpx

async def test():
    config = uvicorn.Config(app, host='0.0.0.0', port=8003, log_level='warning')
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())
    await asyncio.sleep(2)
    
    async with httpx.AsyncClient() as client:
        # Test main page
        r = await client.get('http://localhost:8003/')
        print('Root:', r.status_code, 'len:', len(r.text))
        
        # Test renderer.js
        r = await client.get('http://localhost:8003/static/ui/renderer.js')
        print('renderer.js:', r.status_code, 'len:', len(r.text))
        
        # Test styles.css
        r = await client.get('http://localhost:8003/static/styles.css')
        print('styles.css:', r.status_code, 'len:', len(r.text))
        
        # Test app.js
        r = await client.get('http://localhost:8003/static/app.js')
        print('app.js:', r.status_code, 'len:', len(r.text))
        
        # Test chat/controller.js
        r = await client.get('http://localhost:8003/static/chat/controller.js')
        print('chat/controller.js:', r.status_code, 'len:', len(r.text))
        
        # Test network/websocket.js
        r = await client.get('http://localhost:8003/static/network/websocket.js')
        print('network/websocket.js:', r.status_code, 'len:', len(r.text))
        
        # Test system/metrics.js
        r = await client.get('http://localhost:8003/static/system/metrics.js')
        print('system/metrics.js:', r.status_code, 'len:', len(r.text))
    
    server.should_exit = True
    await task

asyncio.run(test())