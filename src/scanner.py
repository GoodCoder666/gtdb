import asyncio

from config import GtdbConfig
from utils import check_ip, get_session, ip_generator

class IPScanner:
    def __init__(self, config: GtdbConfig):
        self.config = config
        self.availables = []
        self.scanned = 0
        self.result_limit = config.result_limit or float('inf')
        self.running = False

    def stop(self):
        self.running = False

    async def start(self):
        self.running = True
        self.scanned = self.found = 0
        queue = asyncio.Queue(maxsize=self.config.max_connections * 2)
        async with get_session(self.config.timeout) as session:
            workers = [
                asyncio.create_task(self._worker(queue, session))
                for _ in range(self.config.max_connections)
            ]
            warmup_left = self.config.max_connections
            warmup_delay = 2 * self.config.timeout / self.config.max_connections
            for ip in ip_generator(self.config.ip_ranges, self.config.randomize):
                if not self.running or self.found >= self.result_limit:
                    break
                await queue.put(ip)
                if warmup_left > 0:
                    await asyncio.sleep(warmup_delay)
                    warmup_left -= 1
            for _ in range(self.config.max_connections):
                await queue.put(None)
            await asyncio.gather(*workers)
            self.running = False

    async def _scan_ip(self, session, ip):
        for _ in range(self.config.stability_threshold):
            ok = await check_ip(session, ip, self.config.host, self.config.testip_format)
            if not ok:
                return
        self.availables.append(ip)

    async def _worker(self, queue, session):
        while True:
            ip = await queue.get()
            if not ip:
                break
            await self._scan_ip(session, ip)
            self.scanned += 1
            queue.task_done()
