from config import config
from flask import Flask, render_template
import json
import psycopg2
import datetime
from psycopg2.extras import DictCursor

app = Flask(__name__)


def my_converter(o):
    if isinstance(o, datetime.datetime):
        return int(o.strftime("%s")) * 1000


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/btc', methods=['GET'])
def get_btc():
    sql_accounts = "SELECT name " \
          "FROM accounts " \
          "ORDER BY name ASC;"
    sql = "SELECT a.name, b.balance_datetime, b.btc " \
          "FROM balance_btc as b " \
          "LEFT JOIN accounts as a " \
          "ON a.id = b.account_id " \
          "ORDER BY balance_datetime ASC;"
    conn = None
    results = {}
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute(sql_accounts)
        for acc in cur.fetchall():
            results[acc[0]] = []

        cur = conn.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            results[row[0]].append([row[1], row[2]])
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json.dumps(results, default=my_converter)


@app.route('/hours', methods=['GET'])
def get_hours_data():
    sql_accounts = "SELECT * " \
          "FROM accounts " \
          "ORDER BY id ASC;"

    conn = None
    dict_cur = None
    results = {}
    names = {}
    sql = ""
    select = ""
    join = ""
    try:
        params = config()
        conn = psycopg2.connect(**params)

        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cur.execute(sql_accounts)
        for acc in dict_cur:
            names[int(acc['id'])] = acc['name']
            select += ", COALESCE(b_%d.btc,0) as btc_%d " % (acc['id'],acc['id'])
            join += " LEFT JOIN balance_btc AS b_%d ON b_%d.account_id = %d " \
                    "AND extract('minute' from b_%d.balance_datetime) = 0 " \
                    "AND date_trunc('minute',b_%d.balance_datetime) = b.balance_datetime " % (acc['id'],acc['id'],acc['id'],acc['id'],acc['id'])

        dict_cur.close()

        sql = "SELECT b.balance_datetime" + select + \
              "FROM (SELECT DISTINCT date_trunc('hour', balance_datetime) as balance_datetime FROM balance_btc) as b " + join + \
              "WHERE b.balance_datetime >= (CURRENT_DATE - INTERVAL '1 day') " \
              "ORDER BY b.balance_datetime DESC;"

        results['names'] = names

        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cur.execute(sql)
        prev = {}
        current = {}
        percent = {}
        delta = {}
        result = []
        for row in dict_cur:
            for id, name in names.items():
                id = str(id)
                index = 'btc_'+id
                # check whether current value exists
                if row[index] is None:
                    current[index] = 0
                    percent[index] = 0
                    delta[index] = 0
                else:
                    current[index] = row[index]
                    # if previous value exists and greater than 0 then calculate %
                    # else set % to 100
                    if index in prev.keys() and prev[index] > 0:
                        delta[index] = current[index] - prev[index]
                        percent[index] = 100 * (current[index] - prev[index]) / prev[index]
                    else:
                        delta[index] = current[index]
                        percent[index] = 100
                row['percent_'+id] = percent[index]
                row['delta_' + id] = delta[index]

                # set previous value to current for next iteration
                prev[index] = current[index]

            result.append(row)

        dict_cur.close()
        results['data'] = result[-24:]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json.dumps(results, default=my_converter)


@app.route('/days', methods=['GET'])
def get_days_data():
    sql_accounts = "SELECT * " \
          "FROM accounts " \
          "ORDER BY id ASC;"

    conn = None
    results = {}
    names = {}
    select = ""
    join = ""
    try:
        params = config()
        conn = psycopg2.connect(**params)

        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cur.execute(sql_accounts)
        for acc in dict_cur:
            names[int(acc['id'])] = acc['name']
            select += ", COALESCE(b_%d.btc,0) as btc_%d " % (acc['id'],acc['id'])
            join += " LEFT JOIN balance_btc AS b_%d ON b_%d.account_id = %d " \
                    "AND extract('hour' from b_%d.balance_datetime) = 0 " \
                    "AND extract('minute' from b_%d.balance_datetime) = 0 " \
                    "AND date_trunc('day',b_%d.balance_datetime) = b.balance_datetime " % (acc['id'],acc['id'],acc['id'],acc['id'],acc['id'],acc['id'])

        dict_cur.close()

        sql = "SELECT b.balance_datetime" + select + \
              "FROM (SELECT DISTINCT date_trunc('day', balance_datetime) as balance_datetime FROM balance_btc WHERE balance_datetime >= (CURRENT_DATE - INTERVAL '32 day')) as b " + join + \
              "ORDER BY b.balance_datetime DESC;"

        results['names'] = names

        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dict_cur.execute(sql)
        prev = {}
        current = {}
        percent = {}
        delta = {}
        result = []
        for row in dict_cur:
            for id, name in names.items():
                id = str(id)
                index = 'btc_'+id
                # check whether current value exists
                if row[index] is None:
                    current[index] = 0
                    percent[index] = 0
                    delta[index] = 0
                else:
                    current[index] = row[index]
                    # if previous value exists and greater than 0 then calculate %
                    # else set % to 100
                    if index in prev.keys() and prev[index] > 0:
                        delta[index] = current[index] - prev[index]
                        percent[index] = 100 * (current[index] - prev[index]) / prev[index]
                    else:
                        delta[index] = current[index]
                        percent[index] = 100
                row['percent_'+id] = percent[index]
                row['delta_' + id] = delta[index]

                # set previous value to current for next iteration
                prev[index] = current[index]

            result.append(row)

        dict_cur.close()
        results['data'] = result[-31:]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json.dumps(results, default=my_converter)


if __name__ == '__main__':
    app.run()
