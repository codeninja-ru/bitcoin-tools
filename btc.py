#!/usr/bin/env python
import urllib2
import json
import time

fee1 = .998 * .995 * .998
fee2 = .998 * .998 * .998

def get(url):
  req = urllib2.Request(url)
  opener = urllib2.build_opener()
  f = opener.open(req)
  data = f.read()
  return json.loads(data)

def get_depth(pair):
  depth = get("https://btc-e.com/api/2/%s/depth" % pair)
  asks = depth['asks']
  bids = depth['bids']
  #asks = filter(lambda x: x[1] >= 1, asks)
  #bids = filter(lambda x: x[1] >= 1, bids)
  return (asks[0][0], bids[0][0], asks[0][1], bids[0][1])

def calc_profit(cur1, cur2, cur3, fee):
  n1, c1 = cur1
  n2, c2 = cur2
  n3, c3 = cur3
  total = (c1[1] * c2[1] * fee) / c3[0]
  min_amount = min(c1[3], c2[3], c3[2])
  if total > 1:
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    print "%.4f <- Fuck yeah! (%s)" % (total, t)
    print "%s (%.1f) -> %s (%.1f) -> %s (%.1f), min amount -> %.2f" % (n1, c1[1], n2, c2[1], n3, c3[0], min_amount)
  return total

def process():
  def rev(t):
    name = '/'.join(t[0].split('/')[::-1])
    return (name, (1/t[1][1], 1/t[1][0]))

  btc_usd = ('BTC/USD', get_depth('btc_usd'))
  usd_rur = ('USD/RUR', get_depth('usd_rur'))
  btc_rur = ('BTC/RUR', get_depth('btc_rur'))
  ltc_usd = ('LTC/USD', get_depth('ltc_usd'))
  ltc_rur = ('LTC/RUR', get_depth('ltc_rur'))
  ltc_btc = ('LTC/BTC', get_depth('ltc_btc'))

  calc_profit(btc_usd, usd_rur, btc_rur, fee1)
  calc_profit(ltc_usd, usd_rur, ltc_rur, fee1)
  calc_profit(ltc_btc, btc_rur, ltc_rur, fee2)
  calc_profit(ltc_btc, btc_usd, ltc_usd, fee2)

  #calc_profit(rev(btc_rur), rev(usd_rur), btc_usd, fee2)


def main():
  while True:
    try:
      process()
    except Exception as ex:
      print "error. ups..."
      print ex
    time.sleep(3)


if __name__ == "__main__":
  main()
