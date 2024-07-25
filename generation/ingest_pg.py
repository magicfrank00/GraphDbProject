import csv
import time
from database_core_pg import DatabasePg
from constants import *

db = DatabasePg()
tables = [
    "products",
    "components",
    "manufacturers",
    "suppliers",
    "retails",
    "makes",
    "composes",
    "offers",
    "supplies",
    "ships_supply",
    "ships_manufacture",
    "ships",
    "provides",
]

for table in tables:
    db.creation_query(f"DROP TABLE IF EXISTS {table} CASCADE;")

# Create tables
db.creation_query(
    """
CREATE TABLE products (
    ID INTEGER PRIMARY KEY,
    Sell_Price DECIMAL(10, 2)
);
"""
)

db.creation_query(
    """
CREATE TABLE components (
    ID INTEGER PRIMARY KEY
);
"""
)

db.creation_query(
    """
CREATE TABLE manufacturers (
    ID INTEGER PRIMARY KEY
);
"""
)

db.creation_query(
    """
CREATE TABLE suppliers (
    ID INTEGER PRIMARY KEY,
    Price DECIMAL(10, 2),
    Time INTEGER,
    Max_Cap INTEGER
);
"""
)

db.creation_query(
    """
CREATE TABLE retails (
    ID INTEGER PRIMARY KEY
);
"""
)

db.creation_query(
    """
CREATE TABLE makes (
    Manufacturer_ID INTEGER,
    Product_ID INTEGER,
    N_Stock INTEGER,
    Cost DECIMAL(10, 2),
    Time INTEGER,
    Max_Cap INTEGER,
    FOREIGN KEY (Manufacturer_ID) REFERENCES manufacturers(ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES products(ID) ON DELETE CASCADE
);
"""
)

db.creation_query(
    """
CREATE TABLE composes (
    Component_ID INTEGER,
    Product_ID INTEGER,
    FOREIGN KEY (Component_ID) REFERENCES components(ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES products(ID) ON DELETE CASCADE
);
"""
)

db.creation_query(
    """
CREATE TABLE offers (
    Retail_ID INTEGER,
    Product_ID INTEGER,
    FOREIGN KEY (Retail_ID) REFERENCES retails(ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES products(ID) ON DELETE CASCADE
);
"""
)

db.creation_query(
    """
CREATE TABLE supplies (
    Supplier_ID INTEGER,
    Manufacturer_ID INTEGER,
    Max_Cap INTEGER,
    FOREIGN KEY (Supplier_ID) REFERENCES suppliers(ID) ON DELETE CASCADE,
    FOREIGN KEY (Manufacturer_ID) REFERENCES manufacturers(ID) ON DELETE CASCADE
);
"""
)

db.creation_query(
    """
CREATE TABLE ships_supply (
    From_ID INTEGER,
    To_ID INTEGER,
    N_Items INTEGER,
    Time INTEGER,
    Cost DECIMAL(10, 2),
    FOREIGN KEY (From_ID) REFERENCES suppliers(ID) ON DELETE CASCADE,
    FOREIGN KEY (To_ID) REFERENCES manufacturers(ID) ON DELETE CASCADE
);
"""
)

db.creation_query(
    """
CREATE TABLE ships_manufacture (
    From_ID INTEGER,
    To_ID INTEGER,
    N_Items INTEGER,
    Time INTEGER,
    Cost DECIMAL(10, 2),
    FOREIGN KEY (From_ID) REFERENCES manufacturers(ID) ON DELETE CASCADE,
    FOREIGN KEY (To_ID) REFERENCES retails(ID) ON DELETE CASCADE
);
"""
)

# db.creation_query(
#     """
# CREATE TABLE ships (
#     From_ID INTEGER,
#     To_ID INTEGER,
#     N_Items INTEGER,
#     Time INTEGER,
#     Cost DECIMAL(10, 2)
# );
# """
# )

db.creation_query(
    """
CREATE TABLE provides (
    Supplier_ID INTEGER,
    Component_ID INTEGER,
    FOREIGN KEY (Supplier_ID) REFERENCES suppliers(ID) ON DELETE CASCADE,
    FOREIGN KEY (Component_ID) REFERENCES components(ID) ON DELETE CASCADE
);
"""
)


def load_csv_to_db(filename, table_name, columns):
    start = time.time()
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:  # batch insert could be used to speed up the process
            values = [row[col] for col in columns]
            placeholders = ", ".join(["%s"] * len(columns))
            db.creation_query(
                f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})",
                values,
            )
    print(f"Loaded {table_name} in {time.time() - start} seconds")


start = time.time()
# Load data into tables

load_csv_to_db(dataset_folder + "products.csv", "products", ["ID", "Sell_Price"])
load_csv_to_db(dataset_folder + "components.csv", "components", ["ID"])
load_csv_to_db(dataset_folder + "manufacturers.csv", "manufacturers", ["ID"])
load_csv_to_db(
    dataset_folder + "suppliers.csv", "suppliers", ["ID", "Price", "Time", "Max_Cap"]
)
load_csv_to_db(dataset_folder + "retails.csv", "retails", ["ID"])
load_csv_to_db(
    dataset_folder + "makes.csv",
    "makes",
    ["Manufacturer_ID", "Product_ID", "N_Stock", "Cost", "Time", "Max_Cap"],
)
load_csv_to_db(
    dataset_folder + "composes.csv", "composes", ["Component_ID", "Product_ID"]
)
load_csv_to_db(dataset_folder + "offers.csv", "offers", ["Retail_ID", "Product_ID"])
load_csv_to_db(
    dataset_folder + "supplies.csv",
    "supplies",
    ["Supplier_ID", "Manufacturer_ID", "Max_Cap"],
)
load_csv_to_db(
    dataset_folder + "ships_supply.csv",
    "ships_supply",
    ["From_ID", "To_ID", "N_Items", "Time", "Cost"],
)
load_csv_to_db(
    dataset_folder + "ships_manufacture.csv",
    "ships_manufacture",
    ["From_ID", "To_ID", "N_Items", "Time", "Cost"],
)
# load_csv_to_db(
#     dataset_folder + "ships.csv",
#     "ships",
#     ["From_ID", "To_ID", "N_Items", "Time", "Cost"],
# )
load_csv_to_db(
    dataset_folder + "provides.csv", "provides", ["Supplier_ID", "Component_ID"]
)

db.close()

print("Database schema created and data loaded successfully.")
print(f"Time taken: {time.time() - start} seconds")
