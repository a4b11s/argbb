import asyncio
import socket
from config import config

MULTICAST_IP = "239.1.1.1"
PORT = 27122
MAGIC_HASH = "IviUmHThPnxgTKH0LO790QZSAHPH4w44ojZvW6QbfSA="
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


async def broadcast_me(timeout=5):
    while True:
        message = MAGIC_HASH.encode() + b"/*\\" + str(config.get("name")).encode()
        sock.sendto(message, (MULTICAST_IP, PORT))
        await asyncio.sleep(timeout)
