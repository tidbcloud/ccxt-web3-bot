# coding=utf-8

import os
import time
import json
import pymysql
import ccxt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
CREATE_TABLE_SQL_FILE = os.path.join(BASE_DIR, "create_table.sql")

def process():
    config_info = load_config(CONFIG_FILE)
    db_conn = connect_db(config_info)
    crypto_list = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'XRP/USDT:USDT', 'BNB/USDT:USDT','SOL/USDT:USDT']
    limit_days = 120
    create_crypto_table_if_non_exist(db_conn)
    import_crypto_data(db_conn, crypto_list, limit_days)

def import_crypto_data(db_conn, crypto_list, limit_days):
    exchange = ccxt.binanceusdm({'enableRateLimit' : True, 'timeout' : 30000})
    exchange.load_markets()
    segment_days = 90
    time_start = (int(time.time()) / 86400 - limit_days) * 86400 * 1000
    current_time = int(time.time()) * 1000
    segment_duration = segment_days * 86400 * 1000
    for crypto in crypto_list:
        print(f"Preparing to import data for {crypto}")
        for segment_start in range(current_time - limit_days * 86400 * 1000, current_time, segment_duration):
            time.sleep(exchange.rateLimit / 1000)
            segment_end = min(segment_start + segment_duration, current_time)
            res_lists = exchange.fetch_ohlcv(crypto, timeframe='1d', since=segment_start, limit=limit_days)
            insert_crypto_trends_data(db_conn, crypto, res_lists)
            print(f" - Imported data for {crypto} from {time.strftime('%Y-%m-%d', time.gmtime(segment_start / 1000))} to {time.strftime('%Y-%m-%d', time.gmtime(segment_end / 1000))}.")
            pass
        print(f"Data for {crypto} imported successfully.")
        pass
    return


def insert_crypto_trends_data(db_conn, crypto_id, res_lists):
    sql = """INSERT IGNORE INTO `crypto_demo`.`crypto_trends` 
             (`crypto`, `time`, `open_price`, `high_price`, `low_price`, `close_price`) 
             VALUES (%s, FROM_UNIXTIME(%s / 1000), %s, %s, %s, %s)"""
    values = [(crypto_id, data[0], data[1], data[2], data[3], data[4]) for data in res_lists]
    with db_conn.cursor() as cursor:
        cursor.executemany(sql, values)
    db_conn.commit()

def load_config(config_file):
    with open(config_file, 'r') as f:
        data = json.load(f)
    return data

def connect_db(config_info):
    connect = pymysql.connect(
        host=config_info["db_host"],
        port=config_info["db_port"],
        user=config_info["db_user"],
        password=config_info["db_password"],
        ssl={"ca": "/etc/ssl/cert.pem"}
    )
    run_sql(connect, "SET SESSION tidb_multi_statement_mode='ON';")
    return connect

def run_sql(db_conn, sql):
    with db_conn.cursor() as cursor:
        cursor.execute(sql)
    db_conn.commit()

def create_crypto_table_if_non_exist(db_conn):
    with open(CREATE_TABLE_SQL_FILE, 'r') as file:
        sql = file.read()
    run_sql(db_conn, sql)

if __name__ == '__main__':
    process()

