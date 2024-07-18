python3 ingest_pre.py
neo4j-admin database import full neo4j --overwrite-destination \
  --nodes=Product=dataset_ingest/products-header.csv,dataset_ingest/products.csv \
  --nodes=Component=dataset_ingest/components-header.csv,dataset_ingest/components.csv \
  --nodes=Manufacturer=dataset_ingest/manufacturers-header.csv,dataset_ingest/manufacturers.csv \
  --nodes=Supplier=dataset_ingest/suppliers-header.csv,dataset_ingest/suppliers.csv \
  --nodes=Retail=dataset_ingest/retails-header.csv,dataset_ingest/retails.csv \
  --relationships=MAKES=dataset_ingest/makes-header.csv,dataset_ingest/makes.csv \
  --relationships=COMPOSES=dataset_ingest/composes-header.csv,dataset_ingest/composes.csv \
  --relationships=OFFERS=dataset_ingest/offers-header.csv,dataset_ingest/offers.csv \
  --relationships=SUPPLIES=dataset_ingest/supplies-header.csv,dataset_ingest/supplies.csv \
  --relationships=PROVIDES=dataset_ingest/provides-header.csv,dataset_ingest/provides.csv \
  --relationships=SHIPS=dataset_ingest/ships_supply-header.csv,dataset_ingest/ships_supply.csv \
  --relationships=SHIPS=dataset_ingest/ships_manufacture-header.csv,dataset_ingest/ships_manufacture.csv \
