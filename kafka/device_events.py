import uuid
import random as rd
import datetime 
import time
import json
event_status = ['SUCCESS' , 'ERROR' , 'STRANDBY'] + [None]
customer_id = ['CI' + str(id).rjust(5 , '0') for id in range(100 , 300)] 
device_ID = ['D' + str(id).rjust(3 , '0') for id in range(1 , 9)] + [None] 
def generate_events(offset = 0) :
    event = {
        'customerId' : rd.choice(customer_id) ,
        'data' : { 'devices' : [
                { 
                    'deviceId' : rd.choice(device_ID) ,
                    'measure' : 'C' ,
                    'status' : rd.choice(event_status) ,
                    'temperature' : rd.randint(0 , 50)
                }
                for i in range(rd.randint(1,10))
            ] ,
        } ,
        'eventId' : str(uuid.uuid4()) ,
        'eventOffset' : offset , 
        'eventPublisher' : 'device' ,
        'eventTime' : str(datetime.datetime.now())
    }
    return json.dumps(event) 

if __name__ == "__main__" :
    offset = 10000
    num = 1
    while True :
        print(f'data is extracted {num} : ')
        print(generate_events(offset = offset)) 
        time.sleep(rd.randint(1,5))
        offset+=1
        num+=1
        
        
