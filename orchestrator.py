import csv
import random
from redis_queue import Queue
import time
from constants import *

random.seed(0)

manufacturer_ids = [201 * N, 201 * N + num_manufacturers]
supplier_ids = [301 * N, 301 * N + num_suppliers]
product_ids = [1 * N, 1 * N + num_products]
retail_ids = [401 * N, 401 * N + num_retail]


def load_csv_get_offers():
    with open(dataset_folder + "offers.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row.values() for row in reader]


offers = load_csv_get_offers()


class Orchestrator:
    def __init__(self):
        self.neo_queue = Queue("neo_queue")
        self.pg_queue = Queue("pg_queue")

    def generate_order(self):
        # retailer_id = random.randint(*retail_ids)
        # product_id = random.randint(*product_ids)
        retailer_id, product_id = random.choice(offers)
        quantity = random.randint(1, 10)
        return {
            "type": "order",
            "retailer_id": int(retailer_id),
            "product_id": int(product_id),
            "quantity": quantity,
        }

    def generate_drop(self):
        is_supplier = random.random() < 0.5
        label = "Supplier" if is_supplier else "Manufacturer"
        id = (
            random.randint(*supplier_ids)
            if is_supplier
            else random.randint(*manufacturer_ids)
        )
        return {"type": "drop", "id": id, "label": label}

    def generate_action(self):
        if random.random() < 0.8:
            return self.generate_order()
        return self.generate_drop()

    def run(self):
        while True:
            action = self.generate_action()
            self.neo_queue.enqueue(str(action))
            self.pg_queue.enqueue(str(action))
            print(f"Enqueued action: {action}")
            time.sleep(1)
            if INTERACTIVE:
                input("Press Enter to continue...")


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run()
