# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware


# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


import asyncio
import serial_asyncio
import sys  
import os

sys.path.insert(0, os.path.dirname(__file__))
import CYB360
import CYB470

ports = ['COM1', 'COM3']

async def main():
    loop = asyncio.get_running_loop()
    tasks = []
    
    tasks.append(serial_asyncio.create_serial_connection(loop, CYB360.Serial360, ports[0], baudrate=9600))
    tasks.append(serial_asyncio.create_serial_connection(loop, CYB470.Serial470, ports[1], baudrate=9600))
    
    await asyncio.gather(*[loop.create_task(task) for task in tasks])
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())