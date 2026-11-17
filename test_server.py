import asyncio
import uvicorn
import httpx
from main import app

async def test():
    config = uvicorn.Config(app, host='0.0.0.0', port=8001, log_level='info')
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve())
    await asyncio.sleep(2)
    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:8001/health')
        print('Health:', r.json())
        r = await client.get('http://localhost:8001/')
        print('Root status:', r.status_code, 'len:', len(r.text))
    server.should_exit = True
    await task

asyncio.run(test())