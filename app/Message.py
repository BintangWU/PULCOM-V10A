from pydantic import BaseModel

class Measurement470(BaseModel):
    cyl1: list[str] = []
    cyl2: list[str] = []
    cyl3: list[str] = []
    cyl4: list[str] = []
    
class Measurement360(BaseModel):
    j1: list[str] = []
    j2: list[str] = []
    j3: list[str] = []
    j4: list[str] = []
    j5: list[str] = []
    
class PulCom470(BaseModel):
    before: Measurement470 = Measurement470(cyl1=[], cyl2=[], cyl3=[], cyl4=[])
    after: Measurement470 = Measurement470(cyl1=[], cyl2=[], cyl3=[], cyl4=[])
    
class PulCom360(BaseModel): 
    crank: Measurement360 = Measurement360(j1=[], j2=[], j3=[], j4=[], j5=[])