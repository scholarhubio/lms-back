
from concurrent.futures import ThreadPoolExecutor
import asyncio
import json
from typing import Any, Dict

# Global ThreadPoolExecutor to reuse across calls
executor = ThreadPoolExecutor()

# Asynchronously load JSON data using json.loads
async def async_json_loads(data: str) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, json.loads, data)

# Asynchronously dump JSON data using json.dumps
async def async_json_dumps(data: Any) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, json.dumps, data)
