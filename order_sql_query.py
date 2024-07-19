order_sql_query = """
WITH
-- Retrieve the retail and product based on provided IDs
selected_retail AS (
    SELECT r.*
    FROM retails r
    WHERE r.ID = %s
),
selected_product AS (
    SELECT p.*
    FROM products p
    WHERE p.ID = %s
),

-- Find all manufacturers making the product
manufacturer_makes AS (
    SELECT m.*, mk.Cost AS manufacturing_cost, mk.Time AS manufacturing_time, mk.Max_Cap AS max_manufacturing_cap
    FROM manufacturers m
    JOIN makes mk ON mk.Manufacturer_ID = m.ID
    WHERE mk.Product_ID = %s
),

-- Find all suppliers for the components of the product
component_suppliers AS (
    SELECT c.ID AS component_id, s.ID AS supplier_id, s.Price AS supplier_price, s.Time AS supplier_time
    FROM components c
    JOIN composes cp ON cp.Component_ID = c.ID
    JOIN provides p ON p.Component_ID = c.ID
    JOIN suppliers s ON s.ID = p.Supplier_ID
    WHERE cp.Product_ID = %s
),

-- Find the supplies relationships
supplies_relationships AS (
    SELECT sup.Supplier_ID, sup.Manufacturer_ID, sup.Max_Cap
    FROM supplies sup
    JOIN suppliers s ON s.ID = sup.Supplier_ID
),

-- Find the ships relationships
ships_to_manufacturer AS (
    SELECT ss.From_ID AS supplier_id, ss.To_ID AS manufacturer_id, ss.N_Items AS ship_sup_cap, ss.Time AS ship_sup_time, ss.Cost AS ship_sup_cost
    FROM ships_supply ss
    JOIN suppliers s ON s.ID = ss.From_ID
    JOIN manufacturers m ON m.ID = ss.To_ID
),
ships_to_retail AS (
    SELECT sm.From_ID AS manufacturer_id, sm.To_ID AS retail_id, sm.N_Items AS ship_man_cap, sm.Time AS ship_man_time, sm.Cost AS ship_man_cost
    FROM ships_manufacture  sm
    JOIN manufacturers m ON m.ID = sm.From_ID
    JOIN retails r ON r.ID = sm.To_ID
),

-- Aggregate costs and times at the manufacturer level
aggregated_data AS (
    SELECT
        r.ID AS retail_id,
        p.ID AS product_id,
        mk.ID AS manufacturer_id,
        SUM(cs.supplier_price) AS total_component_cost,
        SUM(cs.supplier_time) AS total_supplier_time,
        SUM(stm.ship_sup_cost) AS total_shipping_cost_to_manufacturer,
        SUM(stm.ship_sup_time) AS total_component_delivery_time,
        MIN(sup.Max_Cap) AS max_supply_cap,
        MIN(stm.ship_sup_cap) AS max_ship_sup_cap,
        mk.manufacturing_cost,
        mk.manufacturing_time,
        mk.max_manufacturing_cap,
        str.ship_man_time AS shipping_time_to_retail,
        str.ship_man_cost AS shipping_cost_to_retail,
        str.ship_man_cap AS ship_cap_retail
    FROM
        selected_retail r
        JOIN selected_product p ON TRUE
        JOIN manufacturer_makes mk ON TRUE
        JOIN supplies_relationships sup ON mk.ID = sup.Manufacturer_ID
        JOIN component_suppliers cs ON sup.Supplier_ID = cs.supplier_id
        JOIN ships_to_manufacturer stm ON cs.supplier_id = stm.supplier_id AND mk.ID = stm.manufacturer_id
        JOIN ships_to_retail str ON mk.ID = str.manufacturer_id AND r.ID = str.retail_id
    GROUP BY
        r.ID, p.ID, mk.ID, mk.manufacturing_cost, mk.manufacturing_time, mk.max_manufacturing_cap, str.ship_man_time, str.ship_man_cost, str.ship_man_cap
),

-- Calculate total cost and profit
calculated_data AS (
    SELECT
        retail_id,
        product_id,
        manufacturer_id,
        total_component_cost + manufacturing_cost + total_shipping_cost_to_manufacturer + shipping_cost_to_retail AS total_cost,
        (SELECT Sell_Price FROM products WHERE ID = product_id) - (total_component_cost + manufacturing_cost + total_shipping_cost_to_manufacturer + shipping_cost_to_retail) AS profit,
        total_supplier_time + manufacturing_time + total_component_delivery_time + shipping_time_to_retail AS total_time
    FROM
        aggregated_data
)

-- Ensure profit is positive and return the final result
SELECT
    retail_id,
    product_id,
    manufacturer_id,
    total_cost,
    profit,
    total_time
FROM
    calculated_data
--WHERE profit > 0
ORDER BY
    total_time ASC;
"""
