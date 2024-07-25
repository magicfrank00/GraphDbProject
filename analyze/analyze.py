import time
from redis_queue import Queue
import csv

log_queue = Queue("log_queue")

last_flush = time.time()
logs = []
while True:
    if time.time() - last_flush > 10:
        last_flush = time.time()
        with open("metrics/metrics.csv", "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["manager", "penalty"])
            writer.writeheader()

            for log in logs:
                writer.writerow(log)
        logs = []

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
