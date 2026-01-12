#Standard Library
import asyncio
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, TypedDict
from dataclasses import dataclass


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

@dataclass
class CUser:
    id: int
    name: str
    email: Optional[str]
    number: int =2


class CConfig(TypedDict):
    env: str
    debug: bool

class CConfigOptional(CConfig, total=False):
    version: str


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logging.info("%s took %.3fs", label, elapsed)

def cpu_work(x: int) -> int:
    return x * x

def main():
    user = CUser(1, "Elad", email = "somemail@gmail.com", number=2) #args, kwargs
    # some_bad_config : CConfig = {"env" : 1}
    some_config: CConfigOptional = {"env": "mock_env", "debug": True}
    p = Path("config_stdlib.json") # The full path in current folder
    p.write_text(json.dumps(some_config, ensure_ascii=False)) # Make parameter to json text format
    # We can loaded = json.loads(p.read_text())
    # But better and add afterwards checkers (try except) as in main
    with open("config_stdlib.json", "r", encoding="utf-8") as f:
        loaded = json.load(f)
    logging.info("user=%s loaded=%s", user, loaded)

    #concurrent.futures
    # 'timer' our 'contextmanager'
    with timer("Job"):
        with ThreadPoolExecutor() as ex:
            results = list(ex.map(cpu_work, range(5)))
    logging.info('results=%s', results)

    from concurrent.futures import as_completed



    with ThreadPoolExecutor() as ex:
        futures = [ex.submit(cpu_work, i) for i in range(5)]

        for fut in as_completed(futures):
            result = fut.result()
            print("first avialable result:", result)

async def jobAsync():
    async def a():
        for i in range(3):
            print("A", i)
            time.sleep(0.2)  # ❌ חוסם את הלופ

    async def b():
        for i in range(3):
            print("B", i)
            await asyncio.sleep(0.2)

    # Always top level, cannot be inside 'def'
    await asyncio.gather(a(), b())

if __name__ == '__main__':
    main()

    asyncio.run(jobAsync())

