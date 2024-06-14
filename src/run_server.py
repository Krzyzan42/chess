import random
with open('port', 'w') as file:
    file.write(str(random.randint(50000, 60000)))

from networking.server.server import Server
import asyncio
from PySide6 import QtAsyncio
import logging

logging.getLogger().setLevel(logging.DEBUG)

async def main():
    server = Server()
    await server.run()

if __name__ == '__main__':
    asyncio.run(main())