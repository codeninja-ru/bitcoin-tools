#!/usr/bin/env python
import urllib2
import json
import time

fee = .998 * .995 * .998

def get(url):
  req = urllib2.Request(url)
  opener = urllib2.build_opener()
  f = opener.open(req)
  data = f.read()
  return json.loads(data)

def get_depth(pair):
  depth = get("https://btc-e.com/api/2/%s/depth" % pair)
  return (depth['asks'][0][0], depth['bids'][0][0])

def process():
  btc_usd = get_depth('btc_usd')
  usd_rur = get_depth('usd_rur')
  btc_rur = get_depth('btc_rur')

  total = (btc_usd[1] * usd_rur[1] * fee) / btc_rur[0]
  if total > 1:
    print "%.4f <- Fuck yeah!" % total
    print "BTC/USD (%.1f) -> USD/RUR (%.1f) -> BTC/RUR (%.1f)" % (btc_usd[1],usd_rur[1], btc_rur[0])

def main():
  while True:
    try:
      process()
    except:
      print "error. ups..."
    time.sleep(3)


if __name__ == "__main__":
  main()
