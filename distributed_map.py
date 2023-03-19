import hazelcast
from tqdm import tqdm
import asyncio

async def put_in_map(map_name, key, val):
    map_name.put(key,val)

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
    cluster_name="lab-hazelcast",
    ) 

    map = client.get_map("my-distributed-map")
    for i in tqdm(range(1001)):
        
        asyncio.run(put_in_map(map,i,str(i)))
    client.shutdown()