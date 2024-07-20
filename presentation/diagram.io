// Product table
Table Product {
  ID Integer [primary key]
  Sell_Price Float
}

// Component table
Table Component {
  ID Integer [primary key]
}

// Manufacturer table
Table Manufacturer {
  ID Integer [primary key]
}

// Supplier table
Table Supplier {
  ID Integer [primary key]
  Price Float
  Time Integer
  Max_Cap Integer
}

// Retail table
Table Retail {
  ID Integer [primary key]
}

// MAKES relationship
Table MAKES {
  Manufacturer_ID Integer [ref: > Manufacturer.ID]
  Product_ID Integer [ref: > Product.ID]
  N_Stock Integer
  Cost Float
  Time Integer
  Max_Cap Integer
}

// SUPPLIES relationship
Table SUPPLIES {
  Supplier_ID Integer [ref: > Supplier.ID]
  Manufacturer_ID Integer [ref: > Manufacturer.ID]
  Max_Cap Integer
}

// COMPOSES relationship
Table COMPOSES {
  Component_ID Integer [ref: > Component.ID]
  Product_ID Integer [ref: > Product.ID]
}

// OFFERS relationship
Table OFFERS {
  Retail_ID Integer [ref: > Retail.ID]
  Product_ID Integer [ref: > Product.ID]
}



// PROVIDES relationship
Table PROVIDES {
  Supplier_ID Integer [ref: > Supplier.ID]
  Component_ID Integer [ref: > Component.ID]
}
