#!/usr/bin/env python
import urllib2 
import json
import time
import hashlib

fee1 = .998 * .995 * .998
fee2 = .998 * .998 * .998

def get(url):
  req = urllib2.Request(url)
  opener = urllib2.build_opener()
  f = opener.open(req)
  data = f.read()
  return json.loads(data)

def get_depth(name, pair):
  depth = get("https://btc-e.com/api/2/%s/depth" % pair)
  asks = depth['asks'][:10]
  bids = depth['bids'][:10]
  #asks = filter(lambda x: x[1] >= 1, asks)
  #bids = filter(lambda x: x[1] >= 1, bids)
  return [(name, (asks[idx][0], bids[idx][0], asks[idx][1], bids[idx][1])) for idx in range(0, 10)]

def calc_profit(cur1, cur2, cur3, fee):
  n1, c1 = cur1
  n2, c2 = cur2
  n3, c3 = cur3
  c1_buy, c1_sell, c1_buy_amount, c1_sell_amount = c1
  c2_buy, c2_sell, c2_buy_amount, c2_sell_amount = c2
  c3_buy, c3_sell, c3_buy_amount, c3_sell_amount = c3
  total = (c1_sell * c2_sell * fee) / c3_buy
  min_amount = min(c1_sell_amount, c2_sell_amount, c3_buy_amount)
  if total > 1:
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    print "%.4f <- Fuck yeah! (%s)" % (total, t)
    print "%s (%.1f x %.1f) -> %s (%.1f x %.1f) -> %s (%.1f x %.1f), min amount -> %.2f" % (n1, c1_sell, c1_sell_amount, n2, c2_sell, c2_sell_amount, n3, c3_buy, c3_buy_amount, min_amount)

  def calc_max_amount():
    a1 = c1_sell_amount
    a2 = min(c2_sell_amount, a1 * c2_sell)
    a3 = min(c3_buy_amount, a2 / c3_buy) / total
    return min(a1, a2 / c1_sell, a3) * fee
  return (total > 1, calc_max_amount(), c1_sell, c2_sell, c3_buy)


def process():
  btc_usd_list = get_depth('BTC/USD', 'btc_usd')
  usd_rur_list = get_depth('USD/RUR', 'usd_rur')
  btc_rur_list = get_depth('BTC/RUR', 'btc_rur')
  ltc_usd_list = get_depth('LTC/USD', 'ltc_usd')
  ltc_rur_list = get_depth('LTC/RUR', 'ltc_rur')
  ltc_btc_list = get_depth('LTC/BTC', 'ltc_btc')

  depth_list = zip(btc_usd_list, usd_rur_list, btc_rur_list, ltc_usd_list, ltc_rur_list, ltc_btc_list)

  def trade(item, pairs):
    is_ok, max_amount, c1_sell, c2_sell, c3_buy = item
    p1, p2, p3 = pairs
    if is_ok:
      amount = sell(max_amount, c1_sell, p1)
      amount = sell(amount, c2_sell, p2)
      print buy(amount, c3_buy, p3)
  for item in depth_list:
    btc_usd, usd_rur, btc_rur, ltc_usd, ltc_rur, ltc_btc = item
    trade(calc_profit(btc_usd, usd_rur, btc_rur, fee1), ('btc_usd', 'usd_rur', 'btc_rur'))
    trade(calc_profit(ltc_usd, usd_rur, ltc_rur, fee1), ('ltc_usd', 'usd_rur', 'ltc_rur'))
    trade(calc_profit(ltc_btc, btc_rur, ltc_rur, fee2), ('ltc_btc', 'ltc_rur', 'ltc_rur'))
    trade(calc_profit(ltc_btc, btc_usd, ltc_usd, fee2), ('ltc_btc', 'btc_usd', 'ltc_usd'))

  # mistaken orders check
  def is_mistaken_order(order):
    name, (sell_price, buy_price, _, _) = order
    return sell_price < buy_price
  def show_mistaken_orders(orders):
    if (len(orders) > 0):
      print "buy buy buy!!!!"
      print orders

  show_mistaken_orders(filter(is_mistaken_order, btc_usd_list))
  show_mistaken_orders(filter(is_mistaken_order, usd_rur_list))
  show_mistaken_orders(filter(is_mistaken_order, btc_rur_list))
  show_mistaken_orders(filter(is_mistaken_order, ltc_usd_list))
  show_mistaken_orders(filter(is_mistaken_order, ltc_rur_list))
  show_mistaken_orders(filter(is_mistaken_order, ltc_btc_list))


def sell(amount, price, pair):
  print "sell %.2f * %.2f %s" % (amount, price, pair)
  return price * amount
def buy(amount, price, pair):
  print "buy %.2f * %.2f %s" % (amount, price, pair)
  return amount / price


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
