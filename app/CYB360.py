import sys
import os
import asyncio
import serial_asyncio
from pydantic import BaseModel

# sys.path.insert(0, os.path.dirname(__file__))
# from Message import Measurement, PulCom360

class Measurement(BaseModel):
    x: str  
    y: str
    avg: str

class PulCom360(BaseModel):
    measurement: list[Measurement]
    grade: list[int]

class Serial360(asyncio.Protocol):
    def __init__(self, callback= None):
        self.timeout_handle = None
        self.buffer = []
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
        data = self.buffer.copy()
        data = [item.replace('\r', '&&') for item in data]
        data = ''.join(data).split('&&')
        data.pop()
        
        try:
            if self.callback:
                # message = self.parse_data_cyb360(data)  
                # self.callback(message)
                self.callback(data)
        except Exception as e:
            print(f"Error in callback: {e}")
        finally:
            self.buffer.clear()
    
    def parse_data_cyb360(self, data: list[any]) -> PulCom360:
        measurement = []
        average = []
        grade = []
        tmp_measurement = []
    
        try:
            for item in data[0:5]:
                tmp = item.strip().split(' ')
                tmp = [x for x in tmp if x]
                average.append(tmp[1])
                grade.append(tmp[2])
    
            for i in range(len(data[5:])):
                tmp = data[5:][i].strip().split(' ')
                tmp = [x for x in tmp if x]
                tmp_measurement.append(tmp.pop(1))
    
            for i in range(len(tmp_measurement)):
                if (i % 2 ==  0):
                    measurement.append(Measurement(
                        x= tmp_measurement[i], 
                        y= tmp_measurement[i + 1],
                        avg = average[i % 5]))
        
        except Exception as e:
            raise Exception("Error processing measurement_cyb360") from e
        finally:
            return PulCom360(
                measurement= measurement, 
                grade= grade)

def handle_serial_data(data):
    print(f"Processed Data: {data}")

def get_valid_baudrate():
    while True:
        try:
            baudrate = input("Baudrate (default 9600): ") or "9600"
            if baudrate.isdigit():
                return int(baudrate)
            else:
                print("Please enter a valid number for baudrate.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

async def main(comPort: str, baudrate: int = 9600):
    loop = asyncio.get_running_loop()
    
    try:
        coro = await serial_asyncio.create_serial_connection(
            loop, 
            lambda: Serial360(callback= handle_serial_data), 
            str(comPort).upper(), 
            int(baudrate))
        
        await asyncio.Event().wait()
    except Exception as e:
        print(f"Error: {e}")           
            
if __name__ == "__main__":
    comPort = input("Your Port: ")
    baudrate = get_valid_baudrate()
            
    asyncio.run(main(comPort= comPort, baudrate= baudrate))