import time
from common.redis_queue import Queue
import csv

log_queue = Queue("log_queue")


logs = []
while True:
    try:
        log = log_queue.dequeue()
        if log:
            log = eval(log)

            logs.append(log)
            print(f"Logged: {log}")
        else:
            time.sleep(0.1)
    except KeyboardInterrupt:
        break

with open("metrics.csv", "a", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["manager", "penalty"])
    writer.writeheader()

    for log in logs:
        writer.writerow(log)
