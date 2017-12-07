import json
import time
import os
import MySQLdb
from pprint import pprint
import dateutil.parser
import datetime
import urllib2

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

with open('bittrex_markets.json') as data_file:
    data = json.load(data_file)

mysql_cn = MySQLdb.connect( host="xxx.xxx.xxx.xxx", user="__________", passwd="__________", db="__________" )

for r in data['result']:
    print r
    marketName = r['MarketName']
    active = r['IsActive']
    base = r['BaseCurrency']
    denom = r['MarketCurrencyLong']

    stmt = "replace into crypto.bittrex_markets (MarketName,Base,Denom,Active) values ('%s','%s','%s',%d)" % ( marketName, base, denom, active )
    print stmt
    cur = mysql_cn.cursor()
    cur.execute( stmt )
    mysql_cn.commit()
    cur.close()

    url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=%s&tickInterval=thirtyMin" % ( marketName )
    response = urllib2.urlopen( url, timeout = 5)
    content = response.read()
    f = open( "%s.json" % ( marketName ), 'w' )
    f.write( content )
    f.close()

    os.system("python parse.py %s" % ( marketName ) )
    time.sleep(5)


