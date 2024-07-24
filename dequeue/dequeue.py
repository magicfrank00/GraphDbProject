import os
from constants import INTERACTIVE, TIME_FACTOR
from redis_queue import Queue
import time
import sys
from manager_pg import ManagerPg
from manager_neo import ManagerNeo

from imanager import Manager


def log_result(result, processing_time, log_queue, manager_name):
    if not result:
        total_penalty = TIME_FACTOR * processing_time
    else:
        best_time = result[0]["total_time"]
        total_penalty = best_time + TIME_FACTOR * processing_time

    total_penalty = round(total_penalty / TIME_FACTOR, 2)
    log_queue.enqueue(str({"manager": manager_name, "penalty": total_penalty}))


def dequeue_loop(q: Queue, manager: Manager, log_queue: Queue):
    while True:
        instruction = q.dequeue()
        if instruction:
            again = True
            instruction = eval(instruction)
            print(f"Processing instruction: {instruction}")
            if INTERACTIVE:
                input("Press Enter to continue...")

            while again:
                start = time.time()
                result = None
                if instruction["type"] == "order":
                    result = manager.order(
                        instruction["retailer_id"], instruction["product_id"]
                    )
                elif instruction["type"] == "drop":
                    result = manager.drop(instruction["id"], instruction["label"])

                processing_time = time.time() - start
                print(f"Processed instruction in {processing_time} seconds")
                log_result(result, processing_time, log_queue, manager.name())

                # if INTERACTIVE:
                #     again = input("Process again? (y/n) ") == "y"
                # else:
                #     again = False
                again = False
        time.sleep(1)


if __name__ == "__main__":

    # args = sys.argv
    # if len(args) != 2:
    #     print("Usage: python dequeue.py <pg|neo>")
    #     sys.exit(1)
    db_type = os.getenv("DB_TYPE")  # , sys.argv[1])
    print(f"running {db_type} dequeue")
    if db_type == "pg":
        manager = ManagerPg()
    elif db_type == "neo":
        manager = ManagerNeo()
    else:
        print("Usage: python dequeue.py <pg|neo>")
        sys.exit(1)

    q = Queue(db_type + "_queue")
    log_queue = Queue("log_queue")
    dequeue_loop(q, manager, log_queue)
