import requests
import os
import random
from kafka import KafkaProducer, errors
from kafka import KafkaAdminClient
from kafka.admin import NewPartitions
from consul import Consul

def get_config(consul: Consul, key: str):
    _, value = consul.kv.get(key)
    return value["Value"].decode('ascii')


global uuid_counter
uuid_counter = 1

consul = Consul(host='software_architecture_consul_1', port=8500)

producer = KafkaProducer(
    bootstrap_servers=get_config(consul, "kafka/brokers")
)


admin_client = KafkaAdminClient(bootstrap_servers=get_config(consul, "kafka/brokers"))
topic_partitions = {}
topic_partitions[get_config(consul, "kafka/topic")] = NewPartitions(total_count=2)
try:
    admin_client.create_partitions(topic_partitions)
except:
    pass

def get_url(consul, key):
    all_services = consul.agent.services()
    random_service = random.choice(list(service_name for service_name in all_services if key in all_services[service_name]['Tags']))
    return "http://"+ random_service+":8000/"+key


def get_all_messages():
    ms = get_url(consul, "logging")
    got = False
    while not got:
        try:
            logging = requests.get(ms).text[1:-1]
            got = True
        except:
            ms = get_url(consul, "logging")
    
    ms = get_url(consul,  "messages")
    got = False
    while not got:
        try:
            messages = requests.get(ms).text[1:-1]
            got = True
        except:
            ms = get_url(consul,  "messages")

    result = "FROM LOGGING: " + logging + " FROM MESSAGES: " + messages
    return result

def record_message(message:str):
    global uuid_counter
    ms = get_url(consul, "logging")
    sent = False
    while not sent:
        try:
            response = requests.post(ms, json = {"uuid": uuid_counter, "message":message})
            sent = True
        except:
            ms = get_url(consul, "logging")
    print("BEFORE_PRODUCER")
    future = producer.send(
        get_config(consul, "kafka/topic"),
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