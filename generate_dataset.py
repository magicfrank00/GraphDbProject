import random
import csv
import time


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
    assert len(product_ids) * MANUFACTURER_X_PROD <= len(manufacturers) * 6 * N
    assert len(product_ids) * MANUFACTURER_X_PROD >= len(manufacturers) * 2
    random.shuffle(manufacturers)
    # to_assign = (
    #     [*manufacturers]
    #     + [*manufacturers]
    #     + [*manufacturers]
    #     + [*manufacturers]
    #     + [*manufacturers]
    #     + [*manufacturers]
    #     *N
    # )
    to_assign = [*manufacturers] * 6 * N

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
    manufacturers, products, components, suppliers, composes, provides, makes
):
    # Create a mapping of Supplier ID to the components they provide
    provides_map = {x["Supplier_ID"]: x["Component_ID"] for x in provides}

    # Create a mapping of product ID to the components needed
    product_to_components = {p["ID"]: [] for p in products}
    for c in composes:
        product_to_components[c["Product_ID"]].append(c["Component_ID"])

    # Create a mapping of manufacturer ID to the products they make
    manufacturer_to_products = {m["ID"]: [] for m in manufacturers}
    for m in makes:
        manufacturer_to_products[m["Manufacturer_ID"]].append(m["Product_ID"])

    # Initialize a mapping of needed components to their potential suppliers
    component_to_suppliers = {c["ID"]: [] for c in components}
    for s in suppliers:
        if s["ID"] in provides_map:
            component_to_suppliers[provides_map[s["ID"]]].append(s["ID"])

    # Generate supplies list
    supplies = []
    for m in manufacturers:
        # Find all components needed by this manufacturer's products
        needed_components = set()
        for p_id in manufacturer_to_products[m["ID"]]:
            needed_components.update(product_to_components[p_id])

        # For each needed component, find suppliers who can supply this component
        for component in needed_components:
            for supplier_id in component_to_suppliers[component]:
                supplies.append(
                    {
                        "Supplier_ID": supplier_id,
                        "Manufacturer_ID": m["ID"],
                        # "Component_ID": component,
                        "Max_Cap": generate_stock(),  # Assuming generate_stock() is defined elsewhere
                    }
                )
    return supplies


def generate_ships(suppliers, manufacturers, retails, supplies, offers, makes):
    # Generate shipments from suppliers to manufacturers
    shipments_supply = [
        {
            "From_ID": supply["Supplier_ID"],
            "To_ID": supply["Manufacturer_ID"],
            "N_Items": generate_stock(),
            "Time": generate_time(),
            "Cost": generate_price(),
        }
        for supply in supplies
    ]

    # Create a hashmap for products to manufacturers
    product_to_manufacturers = {}
    for make in makes:
        if make["Product_ID"] not in product_to_manufacturers:
            product_to_manufacturers[make["Product_ID"]] = []
        product_to_manufacturers[make["Product_ID"]].append(make["Manufacturer_ID"])

    # Generate shipments from manufacturers to retailers without duplicates
    shipment_map = {}
    for offer in offers:
        product_id = offer["Product_ID"]
        retail_id = offer["Retail_ID"]

        if product_id in product_to_manufacturers:
            for manufacturer_id in product_to_manufacturers[product_id]:
                key = (manufacturer_id, retail_id)
                if key not in shipment_map:
                    shipment_map[key] = {
                        "N_Items": generate_stock(),
                        "Time": generate_time(),
                        "Cost": generate_price(),
                    }

    shipments_manufacture = [
        {
            "From_ID": key[0],
            "To_ID": key[1],
            "N_Items": value["N_Items"],
            "Time": value["Time"],
            "Cost": value["Cost"],
        }
        for key, value in shipment_map.items()
    ]

    return shipments_supply, shipments_manufacture


start = time.time()
random.seed(1)

N = 100
# Sample sizes for each entity
num_products = 30 * N
num_components = 40 * N
num_manufacturers = 20 * N
num_suppliers = 60 * N  # must be greater than num_components
num_retail = 15 * N
# Constants for relationship scaling
MANUFACTURER_X_PROD = 4 * N  # Max number of manufacturer a products  can have
COMP_X_PROD = 3 * N  # Max number of products a component can be part of
PRODUCT_PRICE_MUL = (
    12 * N
)  # Multiplier for product price to have good chances of profit

# Generate IDs for each entity
product_ids = generate_ids(1 * N, num_products)
component_ids = generate_ids(101 * N, num_components)
manufacturer_ids = generate_ids(201 * N, num_manufacturers)
supplier_ids = generate_ids(301 * N, num_suppliers)
retail_ids = generate_ids(401 * N, num_retail)

print(f"ID generation took {time.time() - start} seconds")

# Generate data for each entity type
products = generate_products(product_ids)
components = generate_components(component_ids)
manufacturers = generate_manufacturers(manufacturer_ids)
suppliers, provides = generate_suppliers(supplier_ids, component_ids)
retails = generate_retail(retail_ids)

print(f"Data generation took {time.time() - start} seconds")

# Generate relationships
makes = generate_makes(manufacturers, product_ids)
print(f"makes generation took {time.time() - start} seconds")
composes = generate_composes(component_ids, product_ids)
print(f"composes generation took {time.time() - start} seconds")
offers = generate_offers(retails, product_ids)
print(f"offers generation took {time.time() - start} seconds")
supplies = generate_supplies(
    manufacturers, products, components, suppliers, composes, provides, makes
)
print(f"supplies generation took {time.time() - start} seconds")
shipments_supply, shipments_manufacture = generate_ships(
    suppliers, manufacturers, retails, supplies, offers, makes
)
print(f"shipments generation took {time.time() - start} seconds")

print(f"Data generation took {time.time() - start} seconds")


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

print(
    "CSV  generation took",
    time.time() - start,
    "seconds",
)
