import asyncio
import runpy

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

runpy.run_path("Charon-The-Ferryman/charonTheFerryman.py", run_name="__main__")
