### Nodes

1. **Product**

    - ID (Integer): Unique identifier for each product.
    - Sell_Price (Float): The selling price of the product.

2. **Component**

    - ID (Integer): Unique identifier for each component.

3. **Manufacturer**

    - ID (Integer): Unique identifier for each manufacturer.

4. **Supplier**

    - ID (Integer): Unique identifier for each supplier.
    - Component_ID (Integer): ID of the component they supply. This creates a direct link to the Component node.
    - Price (Float): Price at which the supplier provides the component.
    - Time (Integer): Time taken to deliver the component.
    - Max_Cap (Integer): Maximum capacity of components the supplier can deliver in a specific time frame.

5. **Retail**
    - ID (Integer): Unique identifier for each retail entity.

### Relationships

1. **MAKES** (Manufacturer to Product)

    - N_Stock (Integer): Number of units of the product currently in stock at the manufacturer.
    - Cost (Float): Manufacturing cost per unit of the product.
    - Time (Integer): Time taken to manufacture the product.
    - Max_Cap (Integer): Maximum production capacity of the manufacturer for the product.

2. **SUPPLIES** (Supplier to Manufacturer)

    <!-- - Component_ID (Integer): ID of the component being supplied, linking back to the Component node. -->

    - Max_Cap (Integer): Number of units supplied per delivery.

3. **COMPOSES** (Component to Product)

    - No attributes, simply indicates which components are part of a product.

4. **OFFERS** (Retail to Product)

    - No attributes, indicating which products are offered by a retail entity.

5. **SHIPS** (Either from Supplier to Manufacturer or from Manufacturer to Retail)
    - N_Items (Integer): Number of items per container.
    - Time (Integer): Time taken for the shipment from source to destination.
    - Cost (Float): Cost of the shipment.

6 **PROVIDES** (Supplier to component)

    - No attributes, simply indicates which component is provided by a supplier.
