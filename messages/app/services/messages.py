import asyncio
from confluent_kafka import Consumer, KafkaError, KafkaException
import sys
import os
import threading
from kafka import KafkaConsumer
import time

running = True
messages = []

# def msg_process(msg):
#     messages.append(msg)

# def commit_completed(err, partitions):
#     if err:
#         print(str(err))
#     else:
#         print("Committed partition offsets: " + str(partitions))

# conf = {'bootstrap.servers': os.environ['KAFKA_INSTANCE'],
#         'group.id': "foo",
#         'default.topic.config': {'auto.offset.reset': 'smallest'},
#         'on_commit': commit_completed}

# consumer = Consumer(conf)
msg_consumer = KafkaConsumer(os.environ['KAFKA_TOPIC'],
                                 group_id='my-group0',
                                 bootstrap_servers=os.environ['KAFKA_INSTANCE'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True, 
                                 )
def stop_consumer():
    msg_consumer.stop()


def msg_loop():

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