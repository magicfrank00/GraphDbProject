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
    return [
        {"ID": pid, "Sell_Price": generate_price() * PRODUCT_PRICE_MUL}
        for pid in product_ids
    ]


def generate_components(component_ids):
    return [{"ID": cid} for cid in component_ids]


def generate_manufacturers(manufacturer_ids):
    return [{"ID": mid} for mid in manufacturer_ids]


def generate_suppliers(supplier_ids, component_ids):
    provides = {}  # componentID :suppliers[]

    random.shuffle(component_ids)
    granted = component_ids[: len(supplier_ids)]

    suppliers = []
    for i, sid in enumerate(supplier_ids):
        if i < len(granted):
            component_id = granted[i]
        else:
            component_id = random.choice(component_ids)
        suppliers.append(
            {
                "ID": sid,
                # "Component_ID": component_id,
                "Price": generate_price(),
                "Time": generate_time(),
                "Max_Cap": generate_max_cap(),
            }
        )
        if component_id in provides:
            provides[component_id].append(sid)
        else:
            provides[component_id] = [sid]
    providesList = []
    for key in provides:
        for value in provides[key]:
            providesList.append({"Supplier_ID": value, "Component_ID": key})
    return suppliers, providesList


def generate_retail(retail_ids):
    return [{"ID": rid} for rid in retail_ids]


def generate_ships(n):
    return [
        {"N_Items": generate_stock(), "Time": generate_time(), "Cost": generate_price()}
        for _ in range(n)
    ]


def generate_makes(manufacturers, product_ids):
    assert len(product_ids) * MANUFACTURER_X_PROD <= len(manufacturers) * 6
    assert len(product_ids) * MANUFACTURER_X_PROD >= len(manufacturers) * 2
    random.shuffle(manufacturers)
    to_assign = (
        [*manufacturers]
        + [*manufacturers]
        + [*manufacturers]
        + [*manufacturers]
        + [*manufacturers]
        + [*manufacturers]
    )
    makes = []
    for product in product_ids:
        num_manufacturers = random.randint(1, MANUFACTURER_X_PROD)
        manufacturers_chosen = to_assign[:num_manufacturers]
        to_assign = to_assign[num_manufacturers:]
        for m in manufacturers_chosen:
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


def generate_composes(components_ids, product_ids):
    composes = []
    for p in product_ids:
        num_components = random.randint(1, COMP_X_PROD)
        components_chosen = random.sample(component_ids, num_components)
        for component in components_chosen:
            composes.append({"Component_ID": component, "Product_ID": p})
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


def generate_supplies(
    manufacturers, products, components, suppliers, composes, provides
):
    provides_map = {x["Supplier_ID"]: x["Component_ID"] for x in provides}
    supplies = []
    # Create a mapping of product ID to the components needed
    product_to_components = {p["ID"]: [] for p in products}
    for c in composes:
        product_to_components[c["Product_ID"]].append(c["Component_ID"])

    # Create a mapping of manufacturer ID to the products they make
    manufacturer_to_products = {m["ID"]: [] for m in manufacturers}
    for m in makes:
        manufacturer_to_products[m["Manufacturer_ID"]].append(m["Product_ID"])

    for m in manufacturers:
        # Find all components needed by this manufacturer's products
        needed_components = set()
        for p_id in manufacturer_to_products[m["ID"]]:
            needed_components.update(product_to_components[p_id])

        # Find suppliers who can supply these components
        for needed_component in needed_components:
            for s in suppliers:
                if provides_map[s["ID"]] == needed_component:
                    supplies.append(
                        {
                            "Supplier_ID": s["ID"],
                            "Manufacturer_ID": m["ID"],
                            # "Component_ID": needed_component,
                            "Max_Cap": generate_stock(),
                        }
                    )
    return supplies


def generate_ships(suppliers, manufacturers, retails, supplies, offers):
    shipments_supply = []
    # Generate shipments from suppliers to manufacturers
    for supply in supplies:
        shipments_supply.append(
            {
                "From_ID": supply["Supplier_ID"],
                "To_ID": supply["Manufacturer_ID"],
                "N_Items": generate_stock(),
                "Time": generate_time(),
                "Cost": generate_price(),
            }
        )
    shipments_manufacture = []

    shipment_map = (
        dict()
    )  # used to prevent duplicate shipments (duplicates are for multiple products from the same manufacturer to the same retailer)
    # Generate shipments from manufacturers to retailers
    for offer in offers:
        # Find which manufacturer makes this product
        product = offer["Product_ID"]
        manufacturer_ids = [
            make["Manufacturer_ID"] for make in makes if make["Product_ID"] == product
        ]
        for manufacturer_id in manufacturer_ids:
            key = (manufacturer_id, offer["Retail_ID"])
            if key not in shipment_map:
                shipment_map[key] = {
                    "N_Items": generate_stock(),
                    "Time": generate_time(),
                    "Cost": generate_price(),
                }
    for key, value in shipment_map.items():
        shipments_manufacture.append(
            {
                "From_ID": key[0],
                "To_ID": key[1],
                "N_Items": value["N_Items"],
                "Time": value["Time"],
                "Cost": value["Cost"],
            }
        )

    return shipments_supply, shipments_manufacture


# Sample sizes for each entity
num_products = 30
num_components = 40
num_manufacturers = 20
num_suppliers = 60  # must be greater than num_components
num_retail = 15

# Generate IDs for each entity
product_ids = generate_ids(1, num_products)
component_ids = generate_ids(101, num_components)
manufacturer_ids = generate_ids(201, num_manufacturers)
supplier_ids = generate_ids(301, num_suppliers)
retail_ids = generate_ids(401, num_retail)

# Constants for relationship scaling
MANUFACTURER_X_PROD = 4  # Max number of manufacturer a products  can have
COMP_X_PROD = 3  # Max number of products a component can be part of
PRODUCT_PRICE_MUL = 12  # Multiplier for product price to have good chances of profit

# Generate data for each entity type
products = generate_products(product_ids)
components = generate_components(component_ids)
manufacturers = generate_manufacturers(manufacturer_ids)
suppliers, provides = generate_suppliers(supplier_ids, component_ids)
retails = generate_retail(retail_ids)

# Generate relationships
makes = generate_makes(manufacturers, product_ids)
composes = generate_composes(component_ids, product_ids)
offers = generate_offers(retails, product_ids)
supplies = generate_supplies(
    manufacturers, products, components, suppliers, composes, provides
)
shipments_supply, shipments_manufacture = generate_ships(
    suppliers, manufacturers, retails, supplies, offers
)


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
    ["ID", "Price", "Time", "Max_Cap"],
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
    ["Supplier_ID", "Manufacturer_ID", "Max_Cap"],
)
output_to_csv(
    shipments_supply,
    dataset_folder + "ships_supply.csv",
    ["From_ID", "To_ID", "N_Items", "Time", "Cost"],
)
output_to_csv(
    shipments_manufacture,
    dataset_folder + "ships_manufacture.csv",
    ["From_ID", "To_ID", "N_Items", "Time", "Cost"],
)
output_to_csv(
    shipments_manufacture + shipments_supply,
    dataset_folder + "ships.csv",
    ["From_ID", "To_ID", "N_Items", "Time", "Cost"],
)
output_to_csv(
    provides,
    dataset_folder + "provides.csv",
    ["Supplier_ID", "Component_ID"],
)

print("Data generation complete. CSV files have been created.")
