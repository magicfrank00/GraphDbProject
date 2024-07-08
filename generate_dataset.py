import random
import csv


def generate_ids(start, count):
    return list(range(start, start + count))


def generate_price():
    return round(random.uniform(10.0, 100.0), 2)


def generate_time():
    return random.randint(1, 48)


def generate_max_cap():
    return random.randint(100, 1000)


def generate_stock():
    return random.randint(50, 500)


def generate_products(product_ids):
    return [{"ID": pid, "Sell_Price": generate_price()} for pid in product_ids]


def generate_components(component_ids):
    return [{"ID": cid} for cid in component_ids]


def generate_manufacturers(manufacturer_ids):
    return [{"ID": mid} for mid in manufacturer_ids]


def generate_suppliers(supplier_ids, component_ids):
    return [
        {
            "ID": sid,
            "Component_ID": random.choice(component_ids),
            "Price": generate_price(),
            "Time": generate_time(),
            "Max_Cap": generate_max_cap(),
        }
        for sid in supplier_ids
    ]


def generate_retail(retail_ids):
    return [{"ID": rid} for rid in retail_ids]


def generate_ships(n):
    return [
        {"N_Items": generate_stock(), "Time": generate_time(), "Cost": generate_price()}
        for _ in range(n)
    ]


def generate_makes(manufacturers, product_ids):
    makes = []
    for m in manufacturers:
        num_products = random.randint(1, PROD_X_MANUFACTURER)
        products_chosen = random.sample(product_ids, num_products)
        for product in products_chosen:
            makes.append(
                {
                    "Manufacturer_ID": m["ID"],
                    "Product_ID": product,
                    "N_Stock": generate_stock(),
                    "Cost": generate_price(),
                    "Time": generate_time(),
                    "Max_Cap": generate_max_cap(),
                }
            )
    return makes


def generate_composes(components, product_ids):
    composes = []
    for c in components:
        num_products = random.randint(1, COMP_X_PROD)
        products_chosen = random.sample(product_ids, num_products)
        for product in products_chosen:
            composes.append({"Component_ID": c["ID"], "Product_ID": product})
    return composes


def generate_offers(retails, product_ids):
    offers = []
    for r in retails:
        num_products = random.randint(
            5, 15
        )  # Assuming a retail can offer between 5 and 15 products
        products_chosen = random.sample(product_ids, num_products)
        for product in products_chosen:
            offers.append({"Retail_ID": r["ID"], "Product_ID": product})
    return offers


def generate_supplies(suppliers, manufacturers, makes, composes):
    supplies = []
    # Create a mapping of components to products
    component_to_product = {
        comp["Component_ID"]: comp["Product_ID"] for comp in composes
    }
    # Create a mapping of products to manufacturers
    product_to_manufacturer = {
        make["Product_ID"]: make["Manufacturer_ID"] for make in makes
    }

    for supplier in suppliers:
        supplied_component = supplier["Component_ID"]
        assert supplied_component in component_to_product
        # Find all products that use this component
        product_ids = [
            pid
            for pid, cid in component_to_product.items()
            if cid == supplied_component
        ]
        # Find all manufacturers that make these products
        manufacturer_ids = list(
            {
                product_to_manufacturer[pid]
                for pid in product_ids
                if pid in product_to_manufacturer
            }
        )
        for manufacturer_id in manufacturer_ids:
            supplies.append(
                {
                    "Supplier_ID": supplier["ID"],
                    "Manufacturer_ID": manufacturer_id,
                    "Component_ID": supplied_component,
                    "Max_Cap": generate_max_cap(),
                }
            )
    return supplies


def generate_ships(suppliers, manufacturers, retails, supplies, offers):
    shipments = []
    # Generate shipments from suppliers to manufacturers
    for supply in supplies:
        shipments.append(
            {
                "From_ID": supply["Supplier_ID"],
                "To_ID": supply["Manufacturer_ID"],
                "N_Items": generate_stock(),
                "Time": generate_time(),
                "Cost": generate_price(),
            }
        )

    # Generate shipments from manufacturers to retailers
    for offer in offers:
        # Find which manufacturer makes this product
        if offer["Product_ID"] in [make["Product_ID"] for make in makes]:
            manufacturer_id = next(
                make["Manufacturer_ID"]
                for make in makes
                if make["Product_ID"] == offer["Product_ID"]
            )
            shipments.append(
                {
                    "From_ID": manufacturer_id,
                    "To_ID": offer["Retail_ID"],
                    "N_Items": generate_stock(),
                    "Time": generate_time(),
                    "Cost": generate_price(),
                }
            )

    return shipments


# Sample sizes for each entity
num_products = 50
num_components = 30
num_manufacturers = 10
num_suppliers = 20
num_retail = 15
num_shipments = 100

# Generate IDs for each entity
product_ids = generate_ids(1, num_products)
component_ids = generate_ids(101, num_components)
manufacturer_ids = generate_ids(201, num_manufacturers)
supplier_ids = generate_ids(301, num_suppliers)
retail_ids = generate_ids(401, num_retail)

# Constants for relationship scaling
PROD_X_MANUFACTURER = 5  # Max number of products a manufacturer can make
COMP_X_PROD = 3  # Max number of products a component can be part of

# Generate data for each entity type
products = generate_products(product_ids)
components = generate_components(component_ids)
manufacturers = generate_manufacturers(manufacturer_ids)
suppliers = generate_suppliers(supplier_ids, component_ids)
retails = generate_retail(retail_ids)

# Generate relationships
makes = generate_makes(manufacturers, product_ids)
composes = generate_composes(components, product_ids)
offers = generate_offers(retails, product_ids)
supplies = generate_supplies(suppliers, manufacturers, makes, composes)
ships = generate_ships(suppliers, manufacturers, retails, supplies, offers)


# Output data to CSV, optional
def output_to_csv(data, filename, fieldnames):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


dataset_folder = "dataset/"
# Specify the CSV filenames and fields
output_to_csv(products, dataset_folder + "products.csv", ["ID", "Sell_Price"])
output_to_csv(components, dataset_folder + "components.csv", ["ID"])
output_to_csv(manufacturers, dataset_folder + "manufacturers.csv", ["ID"])
output_to_csv(
    suppliers,
    dataset_folder + "suppliers.csv",
    ["ID", "Component_ID", "Price", "Time", "Max_Cap"],
)
output_to_csv(retails, dataset_folder + "retails.csv", ["ID"])
output_to_csv(
    makes,
    dataset_folder + "makes.csv",
    ["Manufacturer_ID", "Product_ID", "N_Stock", "Cost", "Time", "Max_Cap"],
)
output_to_csv(composes, dataset_folder + "composes.csv", ["Component_ID", "Product_ID"])
output_to_csv(offers, dataset_folder + "offers.csv", ["Retail_ID", "Product_ID"])
output_to_csv(
    supplies,
    dataset_folder + "supplies.csv",
    ["Supplier_ID", "Manufacturer_ID", "Component_ID", "Max_Cap"],
)
output_to_csv(
    ships, dataset_folder + "ships.csv", ["From_ID", "To_ID", "N_Items", "Time", "Cost"]
)

print("Data generation complete. CSV files have been created.")
