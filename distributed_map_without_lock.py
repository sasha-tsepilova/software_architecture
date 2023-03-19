import hazelcast
import time
import threading


def client_function():
    client = hazelcast.HazelcastClient(
    cluster_name="lab-hazelcast",
    ) 
    key="1"
    map = client.get_map("my-distributed-map-without-lock")

    for k in range(1000):
        if k % 100 == 0:
            print("At: " + str(k))
        value = map.get(key)
        
        time.sleep(0.01)
        value = value.result() + 1
        map.put(key, value)
    
    print("Finished! Result ="  + str(map.get(key).result()))
    client.shutdown()

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
    cluster_name="lab-hazelcast",
    ) 

    map = client.get_map("my-distributed-map-without-lock")
    map.put("1",0)
    threads = list()
    for i in range(3):
        x = threading.Thread(target=client_function)
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()