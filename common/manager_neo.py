import time
from neo import Database
from order_query import order_query
from imanager import Manager


class ManagerNeo(Manager):
    def __init__(self):
        self.db = Database()

    def __del__(self):
        self.db.close()

    def name(self):
        return "neo"

    def order(self, retailer_id, product_id):
        params = {"retailer_id": str(retailer_id), "product_id": str(product_id)}
        best_picks = self.db.query(order_query, params)
        if not best_picks:
            return []
        dict_picks = []
        for pick in best_picks:
            dict_pick = {
                "retail_id": int(pick["retail"]["ID"]),
                "product_id": int(pick["product"]["ID"]),
                "manufacturer_id": int(pick["manufacturer"]["ID"]),
                "total_cost": pick["total_cost"],
                "profit": pick["profit"],
                "total_time": pick["total_time"],
            }
            dict_picks.append(dict_pick)
        [print(pick) for pick in dict_picks]
        return dict_picks

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
