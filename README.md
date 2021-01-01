# Setup

1. Install Postgres
2. Log on to Postgres: `sudo su postgres` and `psql`.
3. Create django user: `CREATE USER django WITH PASSWORD xxxxx;`.
1. Create the django database: `CREATE DATABASE yyyyyyy;`.
1. Populate the database with the django tables.
    1. First, set the correct database settings in the django settings file.
    1. Then run the following Python command: `python3 manage.py migrate`.
3. Create Grafana user: `CREATE USER grafana WITH PASSWORD zzzzzzz;`.
1. Grant read permission to Grafana relevant tables.
    1. Connect to the database: `\connect yyyyyyy`.
    1. Give permission: `GRANT SELECT ON temperature_sensors_temperatures TO grafana;`
    1. Give permission: `GRANT SELECT ON temperature_sensors_temperaturesensor TO grafana;`

