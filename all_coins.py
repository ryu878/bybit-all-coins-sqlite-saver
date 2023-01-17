
# Ryuryu's Bybit SQLite All Coins Saver
# SQLite Edition (Production Mode 6973)
# ----------------------------------
# (c) 2023 Ryan Hayabusa 
# Github: https://github.com/ryu878 
# Web: https://aadresearch.xyz/
# Discord: ryuryu#4087
# ----------------------------------

import os
import time
import sqlite3
import pandas as pd
from inspect import currentframe
from pybit import usdt_perpetual
from config import endpoint, api_key, api_secret



title = 'Ryuryu\'s SQLite All Coins Saver'
ver = '1.0'

terminal_title = title+ver
print(f'\33]0;{terminal_title}\a', end='', flush=True)

session = usdt_perpetual.HTTP(endpoint=endpoint, api_key=api_key, api_secret=api_secret)


def get_linenumber():
    cf = currentframe()
    global line_number
    line_number = cf.f_back.f_lineno


final =  pd.DataFrame()
try:
    data = session.query_symbol()
except Exception as e:
    get_linenumber()
    print(line_number, 'exeception: {}'.format(e))
    pass
df = pd.DataFrame(data)
df2 = pd.DataFrame.from_records(df['result'])
final['pair'] = df2['name'].astype(str)
final['status'] = df2['status'].astype(str)
final['price_scale'] = df2['price_scale'].astype(float)
df3 = pd.DataFrame.from_records(df2['leverage_filter'])
final['max_leverage'] = df3['max_leverage'].astype(float)
df4 = pd.DataFrame.from_records(df2['price_filter'])
final['min_price'] = df4['min_price'].astype(float)
final['max_price'] = df4['max_price'].astype(float)
final['tick_size'] = df4['tick_size'].astype(float)
df5 = pd.DataFrame.from_records(df2['lot_size_filter'])
final['min_trading_qty'] = df5['min_trading_qty'].astype(float)
final['max_trading_qty'] = df5['max_trading_qty'].astype(float)
final['qty_step'] = df5['qty_step'].astype(float)
try:
    data2 = session.latest_information_for_symbol()
except Exception as e:
    get_linenumber()
    print(line_number, 'exeception: {}'.format(e))
    pass
df6 = pd.DataFrame(data2)
df7 = pd.DataFrame.from_records(df6['result'])
final['last_price'] = df7['last_price'].astype(float)
final['min_usdt'] = final['last_price'] * final['min_trading_qty']

df = final
# print(df)

try:

    os.remove('all_coins.db')
    os.remove('all_coins.db-journal')
    print('all_coins.db removed')

except Exception as e:
    get_linenumber()
    # print(line_number, 'exeception: {}'.format(e))
    pass


conn = sqlite3.connect('all_coins.db')
cursor = conn.cursor()
df.to_sql('all_coins', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print('Data Saved',time.strftime("%Y-%m-%d %H:%M:%S"))
