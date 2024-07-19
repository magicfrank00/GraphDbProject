First intsall neo4j from https://neo4j.com/docs/operations-manual/current/installation/linux/debian/
run neo `sudo neo4j console` and go to `http://localhost:7474/browser/` and login with `neo4j` and `galileo-ski-watch-orchid-plate-1558` as password

To be able to reset the db
sudo nano /etc/neo4j/neo4j.conf

> server.directories.data={current_folder}/neo_db_data

with N=100
ID generation took 0.00028252601623535156 seconds
Data generation took 0.01282501220703125 seconds
makes generation took 11.92164134979248 seconds
composes generation took 12.076957702636719 seconds
offers generation took 12.084388256072998 seconds
supplies generation took 19.831711292266846 seconds
shipments generation took 38.25122594833374 seconds
Data generation took 38.25127339363098 seconds
CSV generation took 112.11900305747986 seconds

pre_ingest
20 sec

import
IMPORT DONE in 3m 25s 782ms.
Imported:
16500 nodes
26967152 relationships
56100211 properties
Peak memory usage: 1.033GiB

query
Query took 3.716399669647217 seconds

SQL
load
Loaded products in 0.17006468772888184 seconds
Loaded components in 0.22091960906982422 seconds
Loaded manufacturers in 0.11222052574157715 seconds
Loaded suppliers in 0.34847593307495117 seconds
Loaded retails in 0.08329415321350098 seconds
Loaded makes in 42.54539155960083 seconds
Loaded composes in 30.9894118309021 seconds
Loaded offers in 1.0592100620269775 seconds
Loaded supplies in 861.0971403121948 seconds
Loaded ships_supply in 917.5884292125702 seconds
Loaded ships_manufacture in 144.45423984527588 seconds
Loaded provides in 0.4373443126678467 seconds
Database schema created and data loaded successfully.
Time taken: 1999.1335005760193 seconds

query
Query took 6.560936212539673 seconds
