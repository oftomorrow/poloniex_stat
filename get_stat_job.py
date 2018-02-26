from config import config, config_all
from poloniex import poloniex
import datetime
import psycopg2


def get_account_id(conn, name):
    id = -1
    sql_select = "SELECT id FROM accounts WHERE name = %s"
    sql_insert = "INSERT INTO accounts (name) VALUES (%s) RETURNING id"

    if conn:
        cur = conn.cursor()
        cur.execute(sql_select, (name,))
        id = cur.fetchone()
        if id is None:
            cur.execute(sql_insert, (name,))
            conn.commit()
            id = cur.fetchone()[0]
        cur.close()
        return id
    else:
        return -1


def write_json_data(conn, data, account_id):
    btc = 0
    sql = "INSERT INTO balance_btc(balance_datetime, btc, account_id) VALUES(%s, %s, %s)"

    for currency in data:
        btc += float(data[currency]['btcValue'])
    now = datetime.datetime.now()

    try:
        cur = conn.cursor()
        cur.execute(sql, (now, btc, account_id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def job():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        configs = config_all(filename='api_config.ini')
        for name in configs:
            account_id = get_account_id(conn, name)
            if account_id:
                if 'key' in configs[name].keys() and 'secret' in configs[name].keys():
                    p = poloniex(configs[name]['key'],configs[name]['secret'])
                    data = p.return_complete_balances()
                    write_json_data(conn, data, account_id)
                else:
                    raise Exception('Error', 'Can not find key or secret for ['+name+'] in api_config.ini')

    except (Exception) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


job()