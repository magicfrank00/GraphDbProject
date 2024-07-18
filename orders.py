import time
from neo import Database
from order_query import order_query

db = Database()
# for p in range(30):
params = {"retailer_id": str(411), "product_id": str(18)}
start = time.time()
print(db.query(order_query, params, log=True))
print(f"Query took {time.time() - start} seconds")
db.close()
