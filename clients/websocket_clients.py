import asyncio
import json
import websockets
import logging
from typing import Callable
import aiohttp

logging.basicConfig(level=logging.INFO)

class WebSocketClient:
    def __init__(self, name: str, url: str, source_type: str, on_message: Callable):
        self.name = name
        self.url = url
        self.source_type = source_type
        self.on_message = on_message

    async def connect_ws(self):
        while True:
            try:
                async with websockets.connect(self.url) as ws:
                    logging.info(f"Connected to {self.name} (WebSocket)")
                    async for message in ws:
                        data = json.loads(message)
                        await self.on_message(self.source_type, data)
            except Exception as e:
                logging.warning(f"{self.name} connection error (WebSocket): {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def connect_sse(self):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as resp:
                        logging.info(f"Connected to {self.name} (SSE)")
                        async for line in resp.content:
                            if line:
                                try:
                                    decoded = line.decode().strip()
                                    if decoded.startswith("data:"):
                                        payload = decoded.replace("data:", "", 1).strip()
                                        data = json.loads(payload)
                                        await self.on_message(self.source_type, data)
                                except Exception as e:
                                    logging.warning(f"Error parsing SSE message from {self.name}: {e}")
            except Exception as e:
                logging.warning(f"{self.name} connection error (SSE): {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def connect(self, mode="ws"):
        if mode == "sse":
            await self.connect_sse()
        else:
            await self.connect_ws()

async def start_all_clients(config, on_message):
    tasks = []
    for src in config['sources']:
        mode = src.get('mode', 'ws')
        client = WebSocketClient(
            name=src['name'],
            url=src['url'],
            source_type=src['type'],
            on_message=on_message
        )
        tasks.append(asyncio.create_task(client.connect(mode)))
    await asyncio.gather(*tasks)
