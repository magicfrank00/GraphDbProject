First intsall neo4j from https://neo4j.com/docs/operations-manual/current/installation/linux/debian/
run neo `sudo neo4j console` and go to `http://localhost:7474/browser/` and login with `neo4j` and `galileo-ski-watch-orchid-plate-1558` as password

To be able to reset the db
sudo nano /etc/neo4j/neo4j.conf

> server.directories.data={current_folder}/neo_db_data
