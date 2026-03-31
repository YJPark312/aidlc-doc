import asyncio
from collections import defaultdict


class SSEManager:
    def __init__(self):
        self._connections: dict[int, list[asyncio.Queue]] = defaultdict(list)

    def connect(self, store_id: int) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        self._connections[store_id].append(queue)
        return queue

    def disconnect(self, store_id: int, queue: asyncio.Queue):
        if queue in self._connections[store_id]:
            self._connections[store_id].remove(queue)

    async def broadcast(self, store_id: int, event: str, data: str):
        for queue in self._connections[store_id]:
            await queue.put(f"event: {event}\ndata: {data}\n\n")


sse_manager = SSEManager()
