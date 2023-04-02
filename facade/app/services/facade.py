import requests
import os
import random

global uuid_counter
uuid_counter = 1
logging_ms = ['LOGGING1_MICROSERVICE', 'LOGGING2_MICROSERVICE', 'LOGGING3_MICROSERVICE']

def get_all_messages():
    ms = random.choice(logging_ms)
    got = False
    while not got:
        try:
            logging = requests.get(os.environ[ms]).text[1:-1]
            got = True
        except:
            ms = random.choice(logging_ms)
    
    messages = requests.get(os.environ['MESSAGE_MICROSERVICE']).text[1:-1]
    result = logging + messages
    return result

def record_message(message:str):
    global uuid_counter
    ms = random.choice(logging_ms)
    sent = False
    while not sent:
        try:
            response = requests.post(os.environ[ms], json = {"uuid": uuid_counter, "message":message})
            sent = True
        except:
            ms = random.choice(logging_ms)
    
        
    uuid_counter += 1
    return message