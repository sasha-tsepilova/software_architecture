import hazelcast
import threading

def queue_writer():
    client = hazelcast.HazelcastClient(
        cluster_name="lab-hazelcast",
    ) 
    queue = client.get_queue("my-distributed-queue").blocking()
    for i in range(100):
        print(f"Writing {i}")
        queue.offer(i)

    queue.put(-1)

    client.shutdown()

def queue_reader(reader_name):
    client = hazelcast.HazelcastClient(
        cluster_name="lab-hazelcast",
    ) 
    queue = client.get_queue("my-distributed-queue").blocking()
    while True:
        item = queue.take()
        print(f"Reading with {reader_name} {item}")
        if item == -1:
            queue.put(-1)
            break
    print(f"Reading with {reader_name} finished")
    client.shutdown()



if __name__ == "__main__":
    client = hazelcast.HazelcastClient(
        cluster_name="lab-hazelcast",
    ) 
    queue = client.get_queue("my-distributed-queue").blocking()
    queue.clear()
    threads = [threading.Thread(target=queue_writer), threading.Thread(target=queue_reader, args=("first_reader",)),
               threading.Thread(target=queue_reader, args=("second_reader",))]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    client.shutdown()
