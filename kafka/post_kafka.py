from kafka import KafkaProducer 
from device_events import generate_events
import uuid
import time
import json  
import random as rd
producer = KafkaProducer(
    bootstrap_servers = '172.23.152.231:9092' , 
 )
def post_kafka(data) :
    print("="*90)
    print('data : ' ,  data)
    print("="*90)
    producer.send('device-data' , key = bytes(str(uuid.uuid4()) , 'utf-8') , value = data)
    producer.close
    print('Data is posted ') 

if __name__ == "__main__" :
    offset = 10000 
    while True :
        post_kafka(bytes(str(generate_events(offset = offset)) , 'utf-8'))
        time.sleep(rd.randint(1,6))
        offset+=1


