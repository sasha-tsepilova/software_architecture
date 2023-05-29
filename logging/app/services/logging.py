from ..models.logging import Message
import hazelcast
from consul import Consul

def get_config(consul: Consul, key: str):
    _, value = consul.kv.get(key)
    return value["Value"].decode('ascii')

logging_map = None

def register_for_consul(name):
    consul_service = Consul(host='software_architecture_consul_1', port=8500)
    consul_service.agent.service.register(name, tags=['logging'])
    client = hazelcast.HazelcastClient(
        cluster_name=get_config(consul_service, "hazelcast/cluster_name"),
        cluster_members=get_config(consul_service, "hazelcast/cluster_members").split(',')
    )
    global logging_map
    logging_map = client.get_map(get_config(consul_service,"hazelcast/map_name")).blocking()

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