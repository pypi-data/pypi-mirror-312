import aiohttp
import random
import asyncio
import uuid
from fake_useragent import UserAgent

class AIImageGeneratorAsync:
    PROXY_API_URL = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all"
    GENERATE_URL = "https://magichour.ai/api/free-tools/v1/ai-image-generator"
    STATUS_URL = "https://magichour.ai/api/free-tools/v1/ai-image-generator/{}/status"
    
    def __init__(self):
        self.ua = UserAgent()
        self.proxy_list = []

    async def fetch_proxies(self):
        """Fetch proxies dynamically from the API."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.PROXY_API_URL) as response:
                    if response.status == 200:
                        proxy_text = await response.text()
                        self.proxy_list = proxy_text.splitlines()
                        print(f"Fetched {len(self.proxy_list)} proxies.")
                    else:
                        print(f"Failed to fetch proxies: {response.status}")
            except Exception as e:
                print(f"Error fetching proxies: {e}")

    async def get_random_proxy(self):
        """Return a random proxy."""
        if not self.proxy_list:
            await self.fetch_proxies()
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            return {"http": proxy, "https": proxy}
        return None

    async def create_task(self, prompt, proxies, orientation="landscape"):
        """Create a generation task."""
        task_id = str(uuid.uuid4())
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "application/json, text/plain, */*",
        }
        data = {
            "prompt": prompt,
            "orientation": orientation,
            "task_id": task_id,
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.GENERATE_URL, headers=headers, json=data, proxy=proxies.get("http")) as response:
                    if response.status == 200:
                        return task_id
                    else:
                        print(f"Task creation failed with status: {response.status}")
            except Exception as e:
                print(f"Error creating task: {e}")
        return None

    async def check_status(self, task_id, proxies):
        """Check the status of the generation task."""
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(self.STATUS_URL.format(task_id), proxy=proxies.get("http")) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("status") == "SUCCESS":
                                return data.get("urls", [])
                        await asyncio.sleep(5)
                except Exception as e:
                    print(f"Error checking task status: {e}")
        return []

    async def generate_image(self, prompt, orientation="portrait"):
        """Generate an image asynchronously."""
        proxies = await self.get_random_proxy()
        if not proxies:
            return []
        task_id = await self.create_task(prompt, proxies, orientation)
        if task_id:
            urls = await self.check_status(task_id, proxies)
            return urls
        return []
