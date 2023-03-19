import hazelcast
import time
import threading


def client_function():
    client = hazelcast.HazelcastClient(
    cluster_name="lab-hazelcast",
    ) 
    key="1"
    map = client.get_map("my-distributed-map-pessimistic").blocking()

    for k in range(1000):
        
        if k % 100 == 0:
            print("At: " + str(k))
        map.lock(key)
        try:
            value = map.get(key)
            time.sleep(0.01)
            value += 1
            map.put(key, value)
        finally:
            map.unlock(key)
        

    
    print("Finished! Result ="  + str(map.get(key)))
    client.shutdown()

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
    cluster_name="lab-hazelcast",
    ) 

    map = client.get_map("my-distributed-map-pessimistic").blocking()
    key = "1"
    map.lock(key)
    map.put(key,0)
    map.unlock(key)
    threads = list()
    for i in range(3):
        x = threading.Thread(target=client_function)
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()