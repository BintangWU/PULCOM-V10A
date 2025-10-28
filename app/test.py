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
message_cyb470 = ['DATA001    95.0194 OK2 ','DATA002    95.0204 OK2 ','DATA003    95.0179 OK2 ','DATA004    95.0243 OK3 ','DATA005    95.0133 OK2 ','DATA006    95.0270 OK3 ','DATA007    95.0204 OK2 ','DATA008     0.0009 OK ','DATA009     0.0064 OK ','DATA010     0.0137 OK ','DATA011     0.0137 OK ']

def parse_data_cyb360(data: list[any]) -> CYB360:
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
        
def parse_data_cyb470(data: list[any]):
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
                    print(f"Data belongs to BEFORE {cyl.upper()} {data}")
    

if __name__ == "__main__":
    parse_data_cyb470(message_cyb470)
    
    