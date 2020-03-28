# encoding: UTF-8

from __future__ import print_function
import json
import time as ti
import datetime as dt
import random
from datetime import datetime, timedelta

from pymongo import MongoClient, ASCENDING
from jqdatasdk import *
from vnpy.trader.database import database_manager
from vnpy.trader.object import BarData
from vnpy.trader.constant import Interval,Exchange
import os
# 加载配置
Path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
config = open(Path)
setting = json.load(config)

MONGO_HOST = setting['MONGO_HOST']
MONGO_PORT = setting['MONGO_PORT']
JQ_IP = setting['JQ_IP']
JQ_Password = setting['JQ_Password']
SYMBOLS = setting['SYMBOLS']

auth(JQ_IP, JQ_Password)      # 历史行情服务API对象

# 数据库
# ----------------------------------------------------------------------
def generateExchange(symbol):
    """生成JQ合约代码"""
    if symbol[0:2] in ['cu', 'al', 'zn', 'pb', 'ni', 'sn', 'au', 'ag', 'rb', 'wr', 'hc', 'ss', 'fu', 'bu', 'ru', 'sp']:
        exchangesymbol = symbol.upper() + '.XSGE'
    elif symbol[0:2] in ['m2', 'y2', 'a2', 'b2', 'p2', 'c2', 'cs', 'jd', 'bb', 'fb', 'l2', 'v2', 'eg', 'pp', 'j2', 'jm',
                         'I2', 'EB']:
        exchangesymbol = symbol.upper() + '.XDCE'
    elif symbol[0:2] in ['SR', 'CF', 'CY', 'ZC', 'FG', 'TA', 'MA', 'WH', 'PM', 'LR', 'JR', 'OI', 'RM', 'SF', 'SM', 'AP',
                         'RU', 'SA', 'SJ']:
        exchangesymbol =symbol[0:2] + '2' + symbol[2:5] + '.XZCE'
    return  exchangesymbol


# ----------------------------------------------------------------------
def Exchange1(symbol):
    """返回交易所代码"""
    if symbol[0:2] in ['cu', 'al', 'zn', 'pb', 'ni', 'sn', 'au', 'ag', 'rb', 'wr', 'hc', 'ss', 'fu', 'bu', 'ru', 'sp']:
        exchange1 = 'SHFE'
    elif symbol[0:2] in ['m2', 'y2', 'a2', 'b2', 'p2', 'c2', 'cs', 'jd', 'bb', 'fb', 'l2', 'v2', 'eg', 'pp', 'j2', 'jm',
                         'I2', 'EB']:
        exchange1 = 'DCE'
    elif symbol[0:2] in ['SR', 'CF', 'CY', 'ZC', 'FG', 'TA', 'MA', 'WH', 'PM', 'LR', 'JR', 'OI', 'RM', 'SF', 'SM', 'AP',
                         'RU', 'SA', 'SJ']:
        exchange1 = 'CZCE'
    return exchange1
# ----------------------------------------------------------------------
def generateVtBar(symbol,ix,d):
    """生成K线"""
    bar = BarData(
        symbol=symbol,
        exchange=Exchange(Exchange1(symbol)),
        datetime=ix,
        interval=Interval.MINUTE,
        volume=d["volume"],
        open_price=d["open"],
        high_price=d["high"],
        low_price=d["low"],
        close_price=d["close"],
        gateway_name='DB',
    )
    return bar

#----------------------------------------------------------------------
def downMinuteBarBySymbol(symbol, num):
    """下载某一合约的分钟线数据"""
    start = ti.time()

    df = get_price(generateExchange(symbol), count=num,  frequency='1m',
                   fields=[ 'open', 'high', 'low', 'close', 'volume', 'open_interest'],
                   end_date=dt.datetime.now())
    if df.empty:
        print(u'%s数据下载失败' %symbol)
        return

    bars = []
    for ix, row in df.iterrows():
        bar = generateVtBar(symbol,ix,row)
        bars.append(bar)

    database_manager.save_bar_data(bars, symbol)

    end = ti.time()
    cost = (end - start) * 1000

    print(u'合约%s数据下载完成%s - %s，耗时%s毫秒' %(symbol, df.index[0], df.index[-1], cost))
# ----------------------------------------------------------------------
def downloadAllMinuteBar(num):
    """下载所有配置中的合约的分钟线数据"""
    print('-' * 50)
    print(u'开始下载合约分钟线数据')
    print('-' * 50)
    
    for symbol in SYMBOLS:
        downMinuteBarBySymbol(symbol, num)
        ti.sleep(1)

    print('-' * 50)
    print(u'合约分钟线数据下载完成')
    print('-' * 50)


    
