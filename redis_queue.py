import redis


# /etc/init.d/redis-server status
class Queue:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.r = redis.Redis(host="localhost", port=6379, db=0)

    def enqueue(self, item):
        self.r.rpush(self.queue_name, item)

    def dequeue(self):
        item = self.r.lpop(self.queue_name)
        if item:
            return item.decode("utf-8")
        return None

    def __len__(self):
        return self.r.llen(self.queue_name)


if __name__ == "__main__":
    queue_name = "my_queue"

    q = Queue(queue_name)
    q.enqueue("first")
    q.enqueue("second")
    q.enqueue("third")

    print(len(q))
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(len(q))
