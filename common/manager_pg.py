import time
from database_core_pg import DatabasePg
from imanager import Manager
from order_sql_query import order_sql_query


class ManagerPg(Manager):
    def __init__(self):
        self.db = DatabasePg()

    def __del__(self):
        self.db.close()

    def name(self):
        return "pg"

    def order(self, retailer_id, product_id):
        params = (retailer_id, product_id, product_id, product_id)
        best_picks = self.db.query(order_sql_query, params)
        if not best_picks:
            return []
        # [print(pick) for pick in best_picks]
        return best_picks

    def drop(self, id, label):
        sql_label = label.lower() + "s"
        query = f"DELETE FROM {sql_label} WHERE ID = {id}"
        self.db.query(query)


if __name__ == "__main__":
    orchestrator = ManagerPg()
    retailer_id = 41536
    product_id = 119
    start = time.time()
    records = orchestrator.order(retailer_id, product_id)
    to_drop = records[0]["manufacturer_id"]
    orchestrator.drop(to_drop, "Manufacturer")
    records = orchestrator.order(retailer_id, product_id)

    print(f"Query took {time.time() - start} seconds")
