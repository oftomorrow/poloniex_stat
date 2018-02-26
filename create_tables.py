import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    ###
    # sudo -i -u postgres
    # psql
    # CREATE ROLE poloniex PASSWORD 'poloniex';
    # CREATE DATABASE poloniex_stat OWNER = poloniex;
    # ALTER USER poloniex WITH SUPERUSER;
    # ALTER ROLE "poloniex" WITH LOGIN;
    ###
    commands = (
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(128) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS balance_btc (
            id SERIAL NOT NULL PRIMARY KEY,
            balance_datetime TIMESTAMP WITH TIME ZONE NOT NULL, 
            btc FLOAT NOT NULL,
            account_id INTEGER REFERENCES accounts(id)
        )
        """,)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()