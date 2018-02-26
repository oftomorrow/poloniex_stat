from config import config
from flask import Flask, render_template
import json
import psycopg2
import datetime
from psycopg2.extras import DictCursor

app = Flask(__name__)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        # return o.__str__()
        return int(o.strftime("%s")) * 1000

@app.route('/')
def hello_world():
    sql = "SELECT balance_datetime, btc " \
          "FROM balance_btc " \
          "WHERE extract('minute' from balance_datetime) = 0 " \
          "AND balance_datetime >= (CURRENT_DATE - INTERVAL '1 day') " \
          "ORDER BY balance_datetime;"

    conn = None
    hourresults = []
    try:
        params = {"host": "localhost",
                  "database": "poloniex_stat",
                  "user": "poloniex",
                  "password": "poloniex", }
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        hourresults = []
        prev = current = percent = delta = 0
        for row in rows:
            row_l = list(row)
            if row_l[1] is None:
                current = 0
            else:
                current = row_l[1]
                if prev > 0:
                    delta = current - prev
                    percent = 100 * (current - prev) / prev
                else:
                    delta = current
                    percent = 100
                row_l.append(percent)
                row_l.append(delta)
            hourresults.append(row_l)
            prev = current
        # for row in cur.fetchall():
        #     hourresults.append(dict(zip(columns, row)))
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    sql = "SELECT balance_datetime, btc " \
          "FROM balance_btc " \
          "WHERE extract('hour' from balance_datetime) = 0 AND extract('minute' from balance_datetime) = 0 " \
          "ORDER BY balance_datetime;"

    conn = None
    dayresults = []
    try:
        params = {"host": "localhost",
                  "database": "poloniex_stat",
                  "user": "poloniex",
                  "password": "poloniex", }
        conn = psycopg2.connect(**params)

        # dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # dict_cur.execute(sql)
        # dayresults = dict_cur.fetchall()
        # # close communication with the database
        # dict_cur.close()

        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        dayresults = []
        prev = current = percent = delta = 0
        for row in rows[-32:]:
            row_l = list(row)
            if row_l[1] is None:
                current = 0
            else:
                current = row_l[1]
                if prev > 0:
                    delta = current - prev
                    percent = 100 * (current - prev) / prev
                else:
                    delta = current
                    percent = 100
                row_l.append(percent)
                row_l.append(delta)
            dayresults.append(row_l)
            prev = current
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    data = {
        'hourresults': hourresults[-24:],
        'dayresults': dayresults[-31:]
    } 
    return render_template('index.html', data = data)


@app.route('/btc', methods=['GET'])
def get_btc():
    sql = "SELECT balance_datetime, btc FROM balance_btc ORDER BY balance_datetime ASC;"
    conn = None
    results = []
    try:
        # read the connection parameters
        # params = config()
        params = {"host": "localhost",
                  "database": "poloniex_stat",
                  "user": "poloniex",
                  "password": "poloniex",}
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # dict_cur.execute(sql)
        # results = dict_cur.fetchall()
        # # close communication with the database
        # dict_cur.close()

        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        # for row in cur.fetchall():
        #     results.append(dict(zip(columns, row)))
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json.dumps(results, default=myconverter)


@app.route('/hourdelta', methods=['GET'])
def get_hourdelta():
    sql = "SELECT balance_datetime, btc " \
          "FROM balance_btc " \
          "WHERE extract('minute' from balance_datetime) = 0 " \
          "ORDER BY balance_datetime;"

    conn = None
    results = []
    try:
        # read the connection parameters
        # params = config()
        params = {"host": "localhost",
                  "database": "poloniex_stat",
                  "user": "poloniex",
                  "password": "poloniex",}
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # dict_cur.execute(sql)
        # results = dict_cur.fetchall()
        # # close communication with the database
        # dict_cur.close()

        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        results = []
        prev = current = percent = 0
        for row in rows:
            row_l = list(row)
            if row_l[1] is None:
                current = 0
            else:
                current = row_l[1]
                if prev > 0:
                    percent = 100*(current-prev)/prev
                else:
                    percent = 100
                row_l.append(percent)
            results.append(row_l)
            prev = current
        # for row in cur.fetchall():
        #     results.append(dict(zip(columns, row)))
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json.dumps(results, default=myconverter)


@app.route('/daydelta', methods=['GET'])
def get_daydelta():
    sql = "SELECT balance_datetime, btc " \
          "FROM balance_btc " \
          "WHERE extract('hour' from balance_datetime) = 0 " \
          "ORDER BY balance_datetime;"

    conn = None
    results = []
    try:
        # read the connection parameters
        # params = config()
        params = {"host": "localhost",
                  "database": "poloniex_stat",
                  "user": "poloniex",
                  "password": "poloniex",}
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # dict_cur.execute(sql)
        # results = dict_cur.fetchall()
        # # close communication with the database
        # dict_cur.close()

        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        results = []
        prev = current = percent = 0
        for row in rows:
            row_l = list(row)
            if row_l[1] is None:
                current = 0
            else:
                current = row_l[1]
                if prev > 0:
                    percent = 100*(current-prev)/prev
                else:
                    percent = 100
                row_l.append(percent)
            results.append(row_l)
            prev = current
        # for row in cur.fetchall():
        #     results.append(dict(zip(columns, row)))
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return json.dumps(results, default=myconverter)

if __name__ == '__main__':
    app.run()
