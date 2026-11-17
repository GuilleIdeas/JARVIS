import uvicorn
from main import app
import asyncio
import httpx

async def test():
    config = uvicorn.Config(app, host='0.0.0.0', port=8002, log_level='warning')
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())
    await asyncio.sleep(2)
    
    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:8002/')
        print('Status:', r.status_code)
        print('Content-Type:', r.headers.get('content-type'))
        print('Length:', len(r.text))
        print('Has app div:', 'app' in r.text)
        print('Has JARVIS:', 'JARVIS' in r.text)
        print('Has script:', '<script' in r.text)
        print('--- First 500 chars ---')
        print(r.text[:500])
    
    server.should_exit = True
    await task

asyncio.run(test())