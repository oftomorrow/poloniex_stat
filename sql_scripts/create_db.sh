#!/usr/bin/env bash
sudo -u postgres psql -c "CREATE USER poloniex WITH PASSWORD 'poloniex';"

sudo -u postgres psql -c "CREATE DATABASE poloniex_stat OWNER = poloniex WITH ENCODING 'UTF8';"

sudo -u postgres psql -c "ALTER ROLE poloniex SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE poloniex SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE poloniex SET timezone TO 'UTC';"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE poloniex_stat TO poloniex;"

sudo -u postgres psql -c "ALTER ROLE poloniex SUPERUSER;"

#to be able to run tests and login:
sudo -u postgres psql -c "ALTER USER poloniex LOGIN CREATEDB;"
