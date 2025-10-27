import os
import sys
import json
from pydantic import BaseModel

class Measurement(BaseModel):
    x: str  
    y: str
    avg: str

class CYB360(BaseModel):
    measurement: list[Measurement]
    grade: list[int]

message= ['DATA005    -0.0085 2    4JA1    ', 'DATA006    -0.0107 2    4JA1    ', 'DATA007    -0.0138 2    4JA1    ', 'DATA008    -0.0098 2    4JA1    ', 'DATA009    -0.0183 3    4JA1    ', 'DATA013    -0.0107      4JA1    ', 'DATA014    -0.0064      4JA1    ', 'DATA015    -0.0130      4JA1    ', 'DATA016    -0.0085      4JA1    ', 'DATA017    -0.0135      4JA1    ', 'DATA018    -0.0142      4JA1    ', 'DATA019    -0.0118      4JA1    ', 'DATA020    -0.0078      4JA1    ', 'DATA021    -0.0219      4JA1    ', 'DATA022    -0.0147      4JA1    ']

def measurement_cyb360(data: list[any]) -> CYB360:
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
        return CYB360(
            measurement= measurement, 
            grade= grade)


if __name__ == "__main__":
    data = measurement_cyb360(message)
    print(data.model_dump())
    
    