import asyncio
import serial_asyncio
import sys  
import os
import typing
from fastapi import FastAPI, File, UploadFile, Query, applications
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fastapi_offline_swagger_ui

class Response(BaseModel):
    status: bool = False
    message: str = None
    data: typing.Any = None

sys.path.insert(0, os.path.dirname(__file__))
import CYB360
import CYB470

# Change according to your serial port and baudrate
config = ['COM2', 9600] 
async_lock: asyncio.Lock
message_cyb360: typing.Any = None
message_cyb470: typing.Any = None

app = FastAPI(
    title="MII Tracebility API CYB360", 
    version="1.0.0", 
    description="API CYB360 for MII Tracebility System")

assets_path = fastapi_offline_swagger_ui.__path__[0]
if os.path.exists(assets_path + "/swagger-ui.css") and os.path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")
    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )
    applications.get_swagger_ui_html = swagger_monkey_patch

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status", response_model= Response, summary="Get Server Status")
async def status():
    async with async_lock:
        return Response(
            status= True,
            message= "server is running",
            data= {
                "comPort": f"{config[0]}", 
                "baudrate": config[1]})

@app.get("/status-cyb360", response_model= Response, summary="Get CYB360 Data")
async def status_cyb360():
    global message_cyb360
    
    async with async_lock:
        try:
            if message_cyb360 is not None:        
                return Response(
                    status= True, 
                    message= "success",
                    data= message_cyb360)    
            else:
                return Response(
                    status= False, 
                    message= "no data",
                    data= None)
            
        except Exception as e:
            return Response(
                status= False, 
                message= f"error: {e}",
                data= None)

@app.get("/status-cyb470", response_model= Response, summary="Get CYB470 Data")
async def status_cyb470():
    async with async_lock:
        return Response(
            status= False, 
            message= "not implemented",
            data= None)


def cyb360(data):
    global message_cyb360
    message_cyb360 = data
    return message_cyb360

def cyb470(data):
    global message_cyb470
    message_cyb470 = data
    return message_cyb470

async def start_server():
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, headers= [("Server", "MII-Tracebility")])
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    loop = asyncio.get_running_loop()
    tasks = []
    
    try:
        tasks.append(serial_asyncio.create_serial_connection(loop, lambda: CYB360.Serial360(callback= cyb360), str(config[0]).upper(), baudrate= int(config[1])))
        tasks.append(start_server())
    
        await asyncio.gather(*[loop.create_task(task) for task in tasks])
        await asyncio.Event().wait()
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    asyncio.run(main())