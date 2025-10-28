import sys
import os
import asyncio
import serial_asyncio
from pydantic import BaseModel


class Measurement(BaseModel):
    cyl1: list[str]
    cyl2: list[str]
    cyl3: list[str]
    cyl4: list[str]
    
class PulCom470(BaseModel):
    before: Measurement
    after: Measurement

class Serial470(asyncio.Protocol):
    def __init__(self, callback= None):
        self.timeout_handle = None
        self.buffer = []
        self.message: PulCom470 = None
        self.callback = callback    
        
    def data_received(self, data):
        msg = data.decode('utf-8')
        if msg:
            self.buffer.append(msg)
            
        loop = asyncio.get_running_loop()
        if self.timeout_handle:
            self.timeout_handle.cancel()
        self.timeout_handle = loop.call_later(0.5, self.on_timeout)
        
    def on_timeout(self):       
        print(f"470Received: {self.buffer}")
        data = self.buffer.copy()
        data = [item.replace('\r', '&&') for item in data]
        data = ''.join(data).split('&&')
        data.pop()
        
        try:
            if self.callback:
                # Handle parsed data
                # message = self.parse_data_cyb470(data)
                # self.callback(message)
                self.callback(data)
        except Exception as e:
            print(f"Error in callback: {e}")
        finally:
            self.buffer.clear()
    

        # if (head == "DATA001") and (tail == "DATA011"):
        #     print("Before CYL 1")
        #     message.before.cyl1 = data  

        # if (head == "DATA012") and (tail == "DATA022"):
        #     print("Before CYL 2")
        #     message.before.cyl2 = data  

        # if (head == "DATA023") and (tail == "DATA033"):
        #     print("Before CYL 3")
        #     message.before.cyl3 = data  

        # if (head == "DATA034") and (tail == "DATA044"):
        #     print("Before CYL 4")
        #     message.before.cyl4 = data  
            
        # if (head == "DATA045") and (tail == "DATA059"):
        #     print("After CYL 1")
        #     message.after.cyl1 = data   
            
        # if (head == "DATA060") and (tail == "DATA074"):
        #     print("After CYL 2")
        #     message.after.cyl2 = data   
            
        # if (head == "DATA075") and (tail == "DATA089"): 
        #     print("After CYL 3")
        #     message.after.cyl3 = data
            
        # if (head == "DATA090") and (tail == "DATA104"):
        #     print("After CYL 4")
        #     message.after.cyl4 = data   
    
    def parse_data_cyb470(self, data: list[any]) -> PulCom470:
        data_range = {
            "start": str(data[0][:7]).upper(),
            "end": str(data[-1][:7]).upper()
            }
        
        cylinder_data = {
            "before": {
                "cyl1": ["DATA001", "DATA011"],
                "cyl2": ["DATA012", "DATA022"],
                "cyl3": ["DATA023", "DATA033"],
                "cyl4": ["DATA034", "DATA044"]
                },
            "after": {
                "cyl1": ["DATA045", "DATA059"],
                "cyl2": ["DATA060", "DATA074"],
                "cyl3": ["DATA075", "DATA089"],
                "cyl4": ["DATA090", "DATA104"]
            }
        }
        
        for timing in ["before", "after"]:
            for cyl, range_vals in cylinder_data[timing].items():
                if (data_range["start"] == range_vals[0]) and (data_range["end"] == range_vals[1]):
                    if timing.lower() == "before":
                        setattr(self.message.before, cyl, data)
                    elif timing.lower() == "after":
                        setattr(self.message.after, cyl, data)
                    break
        return self.message
            
# async def main():
#     loop = asyncio.get_running_loop()
#     try:
#         coro = await serial_asyncio.create_serial_connection(loop, Serial470, 'COM3', 9600)
#         await asyncio.Event().wait()
#     except Exception as e:
#         print(f"Error: {e}")           
            
if __name__ == "__main__":
    pass

