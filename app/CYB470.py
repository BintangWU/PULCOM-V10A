import sys
import os
import asyncio
import serial_asyncio

sys.path.insert(0, os.path.dirname(__file__))
from Message import Measurement470, PulCom470

message = PulCom470(
    before = Measurement470(
        cyl1=[], 
        cyl2=[], 
        cyl3=[], 
        cyl4=[]),
    after = Measurement470(
        cyl1=[], 
        cyl2=[], 
        cyl3=[], 
        cyl4=[]
    )
)

class Serial470(asyncio.Protocol):
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
        
        print(f"470Received: {self.buffer}")
        data = self.buffer.copy()
        data = [item.replace('\r', '&&') for item in data]
        data = ''.join(data).split('&&')
        data.pop()
        
        head = str(data[0][:7]).upper()
        tail = str(data[-1][:7]).upper()

        if (head == "DATA001") and (tail == "DATA011"):
            print("Before CYL 1")
            message.before.cyl1 = data  

        if (head == "DATA012") and (tail == "DATA022"):
            print("Before CYL 2")
            message.before.cyl2 = data  

        if (head == "DATA023") and (tail == "DATA033"):
            print("Before CYL 3")
            message.before.cyl3 = data  

        if (head == "DATA034") and (tail == "DATA044"):
            print("Before CYL 4")
            message.before.cyl4 = data  
            
        if (head == "DATA045") and (tail == "DATA059"):
            print("After CYL 1")
            message.after.cyl1 = data   
            
        if (head == "DATA060") and (tail == "DATA074"):
            print("After CYL 2")
            message.after.cyl2 = data   
            
        if (head == "DATA075") and (tail == "DATA089"): 
            print("After CYL 3")
            message.after.cyl3 = data
            
        if (head == "DATA090") and (tail == "DATA104"):
            print("After CYL 4")
            message.after.cyl4 = data   
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

