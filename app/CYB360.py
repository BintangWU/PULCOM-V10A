import sys
import os
import asyncio
import serial_asyncio

sys.path.insert(0, os.path.dirname(__file__))
from Message import Measurement360, PulCom360

message = PulCom360(
    crank= Measurement360(
        j1=[], 
        j2=[], 
        j3=[], 
        j4=[], 
        j5=[]))

class Serial360(asyncio.Protocol):
    def __init__(self):
        self.timeout_handle = None
        self.buffer = []
        
    def data_received(self, data):
        msg = data.decode('utf-8')
        if msg:
            self.buffer.append(msg)
            
        loop = asyncio.get_running_loop()
        if self.timeout_handle:
            self.timeout_handle.cancel()
        self.timeout_handle = loop.call_later(0.5, self.on_timeout)
        
    def on_timeout(self):
        global message
        
        print(f"360Received: {self.buffer}")
        data = self.buffer.copy()
        data = [item.replace('\r', '&&') for item in data]
        data = ''.join(data).split('&&')
        data.pop()
        
        head = str(data[0][:7]).upper()
        tail = str(data[-1][:7]).upper()
        print(f"Message: {data}")
        print(f"Head: {head}, Tail: {tail}")
        
        self.buffer.clear()

# async def main():
#     loop = asyncio.get_running_loop()
#     try:
#         coro = await serial_asyncio.create_serial_connection(loop, Serial470, 'COM3', 9600)
#         await asyncio.Event().wait()
#     except Exception as e:
#         print(f"Error: {e}")           
            
# if __name__ == "__main__":
#     asyncio.run(main())