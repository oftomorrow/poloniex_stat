Poloniex_web
===
Poloniex_web is tiny multi account statistic for Poloniex. It is based on Flask 0.12.

The project includes two parts. First part receives data and stores it into database. Second part is a statistic page that shows chart and tables with data.

## Install
This instruction is written for Ubuntu 16.04

First up, install Python 3.5, Postgresql and virtualenv:

    sudo apt-get install git python3.5 postgresql python-virtualenv

Then clone project and go to project directory:

    cd poloniex_web

### 1. Database install

    cd sql_scripts
    ./create_db
    cd ..
    
### 2. Activation virtualenv

    virtualenv -p python3.5 env
    source env/bin/activate
    
### 3. Install requirements

    pip3 install -r requirements.txt
    
### 4. Create tables

    python create_tables.py
    
### 5. Config file
Add your keys and secrets to api_config.ini as follow:
    
    [poloniex1]
    key=KEY
    secret=SECRET
    
    [poloniex2]
    key=KEY
    secret=SECRET


Put a name of your account in square brackets. Call it so you can easily distinguish it on the statistic page. Names are used for separating multiple accounts.  

If you have one account then fill one block.

### 6. Setup cron

    sudo crontab -e
   
Add this line but do not forget to change paths:

    * * * * * cd /path_to_your_repository/poloniex_web && /path_to_your_repository/poloniex_web/env/bin/python3.5 /path_to_your_repository/poloniex_web/get_stat_job.py
    
And restart cron:
    
    service cron restart

### 7. Configure uwsgi and nginx

Modify `/path_to_nginx_config/sites-available/poloniex_web` like that:

    server {
        listen 80;
        server_name _;

        location / {
                include uwsgi_params;
                uwsgi_pass unix:/var/www/poloniex_web/poloniex_web.sock;
        }
    }

Create a link in `/sites-enabled/`:

    sudo ln -s /path_to_nginx_config/sites-available/poloniex /path_to_nginx_config/sites-enabled/


Create a service for uWSGI `/etc/systemd/system/poloniex_web_service`:

    [Unit]
    Description=uWSGI instance to serve poloniex_web
    After=network.target
    
    [Service]
    User=control
    Group=www-data
    WorkingDirectory=/var/www/poloniex_web
    Environment="PATH=/var/www/poloniex_web/env/bin"
    ExecStart=/var/www/poloniex_web/env/bin/uwsgi --ini poloniex_web.ini
    
    [Install]
    WantedBy=multi-user.target

Do not forget to change user and group and all paths to your own.