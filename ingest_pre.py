import os
import shutil
import csv
import time

start = time.time()
# Define your directories
dataset_folder = "dataset/"
ingest_folder = "dataset_ingest/"

# Ensure the ingest folder exists
if not os.path.exists(ingest_folder):
    os.makedirs(ingest_folder)

# Define your files and corresponding headers
files_headers = {
    "products.csv": ["ID:ID(Product)", "Sell_Price:float"],
    "components.csv": ["ID:ID(Component)"],
    "manufacturers.csv": ["ID:ID(Manufacturer)"],
    "suppliers.csv": [
        "ID:ID(Supplier)",
        "Price:float",
        "Time:int",
        "Max_Cap:int",
    ],
    "retails.csv": ["ID:ID(Retail)"],
    "makes.csv": [
        ":START_ID(Manufacturer)",
        ":END_ID(Product)",
        "N_Stock:int",
        "Cost:float",
        "Time:int",
        "Max_Cap:int",
    ],
    "composes.csv": [":START_ID(Component)", ":END_ID(Product)"],
    "offers.csv": [":START_ID(Retail)", ":END_ID(Product)"],
    "supplies.csv": [":START_ID(Supplier)", ":END_ID(Manufacturer)", "Max_Cap:int"],
    "ships_supply.csv": [
        ":START_ID(Supplier)",
        ":END_ID(Manufacturer)",
        "N_Items:int",
        "Time:int",
        "Cost:float",
    ],
    "ships_manufacture.csv": [
        ":START_ID(Manufacturer)",
        ":END_ID(Retail)",
        "N_Items:int",
        "Time:int",
        "Cost:float",
    ],
    "provides.csv": [":START_ID(Supplier)", ":END_ID(Component)"],
}


# Function to remove the header and create the header CSV
def process_file(file, headers):
    input_file = os.path.join(dataset_folder, file)
    output_file = os.path.join(ingest_folder, file)
    header_file = os.path.join(ingest_folder, file.replace(".csv", "-header.csv"))

    # Write the header file
    with open(header_file, "w", newline="") as hf:
        writer = csv.writer(hf)
        writer.writerow(headers)

    # Read the original file, remove header, and write to new file
    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        next(reader)  # Skip the header
        for row in reader:
            writer.writerow(row)


# Process each file
for file, headers in files_headers.items():
    process_file(file, headers)

print("Processing complete. Files have been moved and headers have been created.")

print(f"Time taken: {time.time() - start} seconds")
