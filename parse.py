import json
import MySQLdb
from pprint import pprint
import dateutil.parser
import datetime
import sys

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

if( len( sys.argv) == 1 ):
  print 'Need parameter.'
  sys.exit(1)

symbol = sys.argv[1]

with open("%s.json" % ( symbol )) as data_file:
    data = json.load(data_file)

mysql_cn = MySQLdb.connect( host="xxx.xxx.xxx.xxx", user="__________", passwd="__________", db="__________" )

for r in data['result']:
    print r
    ts = r['T']
    d = dateutil.parser.parse(ts)
    stmt = "replace into crypto.bittrex (`timestamp`, symbol, C, H, L, O, BV, V) values (%d,'%s',%f,%f,%f,%f,%f,%f)" % ( unix_time_millis(d), symbol, r['C'], r['H'], r['L'], r['O'], r['BV'], r['V'] )
    print stmt

    cur = mysql_cn.cursor()
    cur.execute( stmt )
    mysql_cn.commit()
    cur.close()
