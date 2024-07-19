from redis_queue import Queue
import time

from imanager import Manager


def dequeue_loop(q: Queue, manager: Manager):
    while True:
        instruction = q.dequeue()
        if instruction:
            instruction = eval(instruction)
            print(f"Processing instruction: {instruction}")
            input("Press Enter to continue...")
            start = time.time()
            if instruction["type"] == "order":
                manager.order(instruction["retailer_id"], instruction["product_id"])
            elif instruction["type"] == "drop":
                manager.drop(instruction["id"], instruction["label"])
            print(f"Processed instruction in {time.time() - start} seconds")
        time.sleep(1)


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) != 2:
        print("Usage: python dequeue.py <pg|neo>")
        sys.exit(1)
    db_type = args[1]
    if db_type == "pg":
        from manager_pg import ManagerPg

        manager = ManagerPg()
    elif db_type == "neo":
        from manager_neo import ManagerNeo

        manager = ManagerNeo()
    else:
        print("Usage: python dequeue.py <pg|neo>")
        sys.exit(1)

    q = Queue(db_type + "_queue")
    dequeue_loop(q, manager)
