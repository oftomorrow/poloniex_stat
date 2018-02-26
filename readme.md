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


Put a name of your account in square brackets. Call it so you can easily distinguish it on the statistic page. Names are used for separating multiple accounts.  

If you have one account then fill one block.

### 6. Setup cron

    sudo crontab -e
   
Add this line but do not forget to change paths:

    * * * * * cd /path_to_your_repository/poloniex_web && /path_to_your_repository/poloniex_web/env/bin/python3.5 /path_to_your_repository/poloniex_web/get_stat_job.py
    
And restart cron:
    
    service cron restart

### 7. Configure uwsgi and nginx
