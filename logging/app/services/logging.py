from ..models.logging import Message
import hazelcast

client = hazelcast.HazelcastClient(
cluster_name="lab-micro-hazelcast",
cluster_members=["hazelcast-node-1", "hazelcast-node-2", "hazelcast-node-3"]
) 
logging_map = client.get_map("logging-map").blocking()

def return_messages():
    global logging_map
    map_values = logging_map.values()
    return (' ').join(map_values)

def record_message(message: Message):
    global logging_map
    print("Got a new message")
    print(f"UUID={message.uuid} with message={message.message}")
    logging_map.put(message.uuid, message.message)
    return message