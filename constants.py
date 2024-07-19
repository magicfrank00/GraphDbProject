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