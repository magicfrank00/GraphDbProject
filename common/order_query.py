order_query = """

MATCH (retail:Retail {ID: $retailer_id})-[:OFFERS]->(product:Product {ID: $product_id})
WITH retail, product

// Find all manufacturers making the product
MATCH (manufacturer:Manufacturer)-[makes:MAKES]->(product)
WITH retail, product, manufacturer, makes ORDER BY manufacturer.ID LIMIT 6

// Find all suppliers for the components of the product
MATCH (product)<-[:COMPOSES]-(component:Component)<-[:PROVIDES]-(supplier:Supplier)
WITH retail, product, manufacturer, makes, component, supplier
MATCH (supplier)-[supplies:SUPPLIES]->(manufacturer)
WITH retail, product, manufacturer, makes, supplier, supplies

// Find the SHIPS relationships
MATCH (supplier)-[ship_sup:SHIPS]->(manufacturer)
MATCH (manufacturer)-[ship_man:SHIPS]->(retail)
WITH retail, product, manufacturer, makes, supplier, supplies, ship_sup, ship_man

// Aggregate costs and times at the manufacturer level
WITH retail, product, manufacturer, makes, 
     sum(supplier.Price) AS total_component_cost,
     sum(supplier.Time) as total_supplier_time,
     sum(ship_sup.Cost) AS total_shipping_cost_to_manufacturer,
     sum(ship_sup.Time) AS total_component_delivery_time,
     min(supplies.Max_Cap) AS max_supply_cap,
     min(ship_sup.N_Items) as max_ship_sup_cap,
     makes.Cost AS manufacturing_cost,
     makes.Time AS manufacturing_time,
     makes.Max_Cap AS max_manufacturing_cap,
     ship_man.Time AS shipping_time_to_retail,
     ship_man.Cost AS shipping_cost_to_retail,
     ship_man.N_Items as ship_cap_retail

// Calculate total cost and profit
WITH retail, product, manufacturer, 
     total_component_cost + manufacturing_cost + total_shipping_cost_to_manufacturer + shipping_cost_to_retail AS total_cost,
     product.Sell_Price - (total_component_cost + manufacturing_cost + total_shipping_cost_to_manufacturer + shipping_cost_to_retail) AS profit,
     total_supplier_time + manufacturing_time + total_component_delivery_time + shipping_time_to_retail AS total_time

// Ensure profit is positive
//WHERE profit > 0
RETURN retail, product, manufacturer, total_cost, profit, total_time
ORDER BY total_time ASC
"""
