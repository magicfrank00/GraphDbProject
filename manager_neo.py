import time
from neo import Database
from order_query import order_query
from imanager import Manager


class ManagerNeo(Manager):
    def __init__(self):
        self.db = Database()

    def __del__(self):
        self.db.close()

    def order(self, retailer_id, product_id):
        params = {"retailer_id": str(retailer_id), "product_id": str(product_id)}
        best_picks = self.db.query(order_query, params)
        if not best_picks:
            return []
        [print(pick) for pick in best_picks]
        return best_picks

    def drop(self, id, label):
        query = f"MATCH (n:{label} {{ID: '{str(id)}'}}) DETACH DELETE n"
        self.db.query(query)


if __name__ == "__main__":
    orchestrator = ManagerNeo()
    retailer_id = 41536
    product_id = 119
    start = time.time()
    records = orchestrator.order(retailer_id, product_id)
    # to_drop = records[0]["manufacturer"]["ID"]
    # orchestrator.drop(to_drop, "Manufacturer")
    # records = orchestrator.order(retailer_id, product_id)

    print(f"Query took {time.time() - start} seconds")
