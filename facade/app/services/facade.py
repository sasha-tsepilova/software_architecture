import requests
import os
import random
from kafka import KafkaProducer, errors
from kafka import KafkaAdminClient
from kafka.admin import NewPartitions

global uuid_counter
uuid_counter = 1
logging_ms = ['LOGGING1_MICROSERVICE', 'LOGGING2_MICROSERVICE', 'LOGGING3_MICROSERVICE']
messaging_ms = ['MESSAGE1_MICROSERVICE', 'MESSAGE2_MICROSERVICE']
producer = KafkaProducer(
    bootstrap_servers=os.environ["KAFKA_INSTANCE"]
)


admin_client = KafkaAdminClient(bootstrap_servers=os.environ["KAFKA_INSTANCE"])
topic_partitions = {}
topic_partitions[os.environ["KAFKA_TOPIC"]] = NewPartitions(total_count=2)
try:
    admin_client.create_partitions(topic_partitions)
except:
    pass


def get_all_messages():
    ms = random.choice(logging_ms)
    got = False
    while not got:
        try:
            logging = requests.get(os.environ[ms]).text[1:-1]
            got = True
        except:
            ms = random.choice(logging_ms)
    
    ms = random.choice(messaging_ms)
    got = False
    while not got:
        try:
            messages = requests.get(os.environ[ms]).text[1:-1]
            got = True
        except:
            ms = random.choice(messaging_ms)

    result = "FROM LOGGING: " + logging + " FROM MESSAGES: " + messages
    return result

def record_message(message:str):
    global uuid_counter
    ms = random.choice(logging_ms)
    sent = False
    while not sent:
        print(ms)
        try:
            response = requests.post(os.environ[ms], json = {"uuid": uuid_counter, "message":message})
            sent = True
        except:
            ms = random.choice(logging_ms)
    print("BEFORE_PRODUCER")
    future = producer.send(
        os.environ["KAFKA_TOPIC"],
        str.encode(message)
    )
    print("AFTER_PRODUCER")

    try:
        record_metadata = future.get(timeout=10)
        print(record_metadata)
    except errors.KafkaError as err:
        print(err)
        pass
    
        
    uuid_counter += 1
    return message