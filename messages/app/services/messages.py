import os
import threading
from kafka import KafkaConsumer
import time
from consul import Consul

def get_config(consul: Consul, key: str):
    _, value = consul.kv.get(key)
    return value["Value"].decode('ascii')

running = True
messages = []
msg_consumer = None

def register_for_consul(name):
    consul_service = Consul(host='software_architecture_consul_1', port=8500)
    consul_service.agent.service.register(name, tags=['messages'])
    global msg_consumer
    msg_consumer = KafkaConsumer(get_config(consul_service, "kafka/topic"),
                                 group_id=get_config(consul_service, "kafka/group"),
                                 bootstrap_servers=get_config(consul_service, "kafka/brokers"),
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True, 
                                 )

def stop_consumer():
    global msg_consumer
    msg_consumer.stop()


def msg_loop():
    global msg_consumer
    for msg in msg_consumer:
        m = msg.value.decode()
        print(f"Message service: Got message: {m}")
        messages.append(m)
        print(messages)
    
    time.sleep(1)
    msg_consumer.commit()



def consume_loop():
    t = threading.Thread(target=msg_loop)
    t.start()


async def get_logs():
    return ','.join(messages)