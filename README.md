# Setup

1. Create web-site directory: `mkdir /temperature_site`.
1. Create static directory: `mkdir /temperature_site/static`.
1. Set-up camera-image directory.
    1. Create the directory `mkdir /temperature_site/camera_images`.
    1. Create data-acquisition user: `sudo useradd -r -s /bin/false data_acquisition`.
    1. Change group: `sudo chgrp data_acquisition /temperature_site/camera_images`.
    1. Set group permissions: `sudo chmod g=rxw /temperature_site/camera_images`.
1. Clone temperature monitor repo: `cd /temperature_site & git clone https://github.com/SkyToGround/temperature_monitor.git`.
1. Install Python 3 and required libraries (listed in _requirements.txt_).
1. Install Postgres
2. Log on to Postgres: `sudo su postgres` and `psql`.
3. Create django user: `CREATE USER django WITH PASSWORD xxxxx;`.
1. Create the django database: `CREATE DATABASE yyyyyyy;`.
1. Populate the database with the django tables.
    1. First, set the correct database settings in the django settings file.
    1. Then run the following Python command: `cd /temperature_site/temperature_monitor & python3 manage.py migrate`.
3. Create Grafana user: `CREATE USER grafana WITH PASSWORD zzzzzzz;`.
1. Grant read permission to Grafana relevant tables.
    1. Connect to the database: `\connect yyyyyyy`.
    1. Give permission: `GRANT SELECT ON temperature_sensors_temperatures TO grafana;`
    1. Give permission: `GRANT SELECT ON temperature_sensors_temperaturesensor TO grafana;`.
1. Install owfs.
1. Copy owfs systemd unit to the correct directory: `cd /temperature_site/temperature_monitor/systemctl-services & sudo cp owfs.service /lib/systemd/system/`
1. Copy systemd units to the correct directory: `cd /temperature_site/temperature_monitor/systemctl-services & sudo cp image_acquisition.service /etc/systemd/system/ & sudo cp temperature_acquisition.service /etc/systemd/system/`.
1. Start the services: `systemctl start image_acquisition & systemctl start temperature_acquisition`.
1. Install apache2 and and mod-wsgi `apt-get install apache2 libapache2-mod-wsgi-py3`.
1. Copy the file *sparup_config.conf* to */etc/apache2/sites-available/*.
1. Enable site config by running: `a2ensite sparup_config`.