import time
from drop_db import drop_db
from neo import SUPPLY_DB, Database
from constants import dataset_folder

# create_db = "CREATE DATABASE " + SUPPLY_DB
# db.query(create_db) # Not supported for community edition, using default db

# drop db
import os

drop = True

if drop:
    drop_db()
    input("DB cleared,restart the db, Press Enter to continue...")

    db = Database()

    queries = [
        "CREATE CONSTRAINT FOR (p:Product) REQUIRE p.ID IS UNIQUE;",
        "CREATE CONSTRAINT FOR (c:Component) REQUIRE c.ID IS UNIQUE;",
        "CREATE CONSTRAINT FOR (m:Manufacturer) REQUIRE m.ID IS UNIQUE;",
        "CREATE CONSTRAINT FOR (s:Supplier) REQUIRE s.ID IS UNIQUE;",
        "CREATE CONSTRAINT FOR (r:Retail) REQUIRE r.ID IS UNIQUE;",
    ]

    for query in queries:
        db.query(query)
else:
    db = Database()


import csv



start = time.time()


def load_csv_and_generate_queries(csv_filename, node_type, attributes):
    queries = []
    with open(dataset_folder + csv_filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            properties = ", ".join([f"{key}: {value}" for key, value in row.items()])
            query = f"CREATE (:{node_type} {{{properties}}})"
            queries.append(query)
    db.query("\n".join(queries), None, log=True)


# Generate queries for creating nodes
load_csv_and_generate_queries("products.csv", "Product", ["ID", "Sell_Price"])
load_csv_and_generate_queries("components.csv", "Component", ["ID"])
load_csv_and_generate_queries("manufacturers.csv", "Manufacturer", ["ID"])
load_csv_and_generate_queries(
    "suppliers.csv", "Supplier", ["ID", "Price", "Time", "Max_Cap"]
)
load_csv_and_generate_queries("retails.csv", "Retail", ["ID"])
print(f"Creating nodes took {time.time() - start} seconds")

# def generate_offers_relationship(csv_filename):
#     with open(dataset_folder + csv_filename, newline="") as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             # Debugging output
#             print(f"Row data: {row}")

#             retail_id = row["Retail_ID"].strip()  # Strip spaces to avoid issues
#             product_id = row["Product_ID"].strip()

#             # Construct and execute the Cypher query
#             query = f"""
# MATCH (r:Retail {{ID: {retail_id}}}),
#       (p:Product {{ID: {product_id}}})
# CREATE (r)-[:OFFERS]->(p);
# """
#             db.query(query)


# # Call the function for 'offers.csv'
# generate_offers_relationship("offers.csv")
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def generate_relationship_query(
    csv_filename,
    rel_type,
    source_node,
    target_node,
    source_key,
    target_key,
    rel_attributes=[],
):
    with open(dataset_folder + csv_filename, newline="") as csvfile:
        queries = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Properly format the keys for source and target based on their data type
            source_value = (
                f'"{row[source_key]}"'
                if not row[source_key].isdigit()
                else row[source_key]
            )
            target_value = (
                f'"{row[target_key]}"'
                if not row[target_key].isdigit()
                else row[target_key]
            )

            # Ensure properties are properly formatted
            properties = ", ".join(
                [
                    (
                        f'{key}: "{row[key]}"'
                        if not row[key].isdigit() and not is_float(row[key])
                        else f"{key}: {row[key]}"
                    )
                    for key in rel_attributes
                    if key in row
                ]
            )

            # Construct and execute the Cypher query
            query = f"""
                    MATCH (a:{source_node} {{ID: {source_value}}}),
                          (b:{target_node} {{ID: {target_value}}})
                    CREATE (a)-[:{rel_type} {{{properties}}}]->(b);
                    """
            # print(query)
            queries.append(query)
        db.batch_query(
            queries,
        )


start = time.time()
generate_relationship_query(
    "makes.csv",
    "MAKES",
    "Manufacturer",
    "Product",
    "Manufacturer_ID",
    "Product_ID",
    ["N_Stock", "Cost", "Time", "Max_Cap"],
)
generate_relationship_query(
    "supplies.csv",
    "SUPPLIES",
    "Supplier",
    "Manufacturer",
    "Supplier_ID",
    "Manufacturer_ID",
    ["Max_Cap"],
)
generate_relationship_query(
    "composes.csv", "COMPOSES", "Component", "Product", "Component_ID", "Product_ID"
)
generate_relationship_query(
    "offers.csv", "OFFERS", "Retail", "Product", "Retail_ID", "Product_ID"
)
generate_relationship_query(
    "ships.csv",
    "SHIPS",
    "Manufacturer",
    "Retail",
    "From_ID",
    "To_ID",
    ["N_Items", "Time", "Cost"],
)
generate_relationship_query(  # Executed twice, once for suppliers and once for manufacturers
    "ships.csv",
    "SHIPS",
    "Supplier",
    "Manufacturer",
    "From_ID",
    "To_ID",
    ["N_Items", "Time", "Cost"],
)
generate_relationship_query(
    "provides.csv",
    "PROVIDES",
    "Supplier",
    "Component",
    "Supplier_ID",
    "Component_ID",
)
print(f"Creating relationships took {time.time() - start} seconds")
