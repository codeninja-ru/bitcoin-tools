#!/usr/bin/env ruby

require 'net/http'
require 'open-uri'
require 'json'

def get(url) 
  uri = URI.parse(url)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  http.start do |http|
    request = Net::HTTP::Get.new uri.request_uri
    http.request request
  end.body
end

while true do
  btc_usd = JSON.parse get('https://btc-e.com/api/2/btc_usd/ticker')
  btc_usd_sell = btc_usd["ticker"]["sell"]
  btc_usd_buy = btc_usd["ticker"]["buy"]

  usd_rur = JSON.parse get('https://btc-e.com/api/2/usd_rur/ticker')
  usd_rur_sell = usd_rur["ticker"]["sell"]

  btc_rur = JSON.parse get('https://btc-e.com/api/2/btc_rur/ticker')
  btc_rur_buy = btc_rur["ticker"]["buy"]

  btc_total = (btc_usd_sell * usd_rur_sell) / btc_rur_buy

  if btc_total > 1
    puts 'fuck yeah!!!'
    puts Time.now
    puts "BTC/USD = #{btc_usd_sell} USD/RUR = #{usd_rur_sell} BTC/RUR = #{btc_rur_buy} profit = #{btc_total}"
  end

  btc_eur = JSON.parse get('https://btc-e.com/api/2/btc_eur/ticker')
  btc_eur_sell = btc_eur["ticker"]["sell"]

  eur_usd = JSON.parse get('https://btc-e.com/api/2/eur_usd/ticker')
  eur_usd_sell = eur_usd["ticker"]["sell"]

  eur_total = (btc_eur_sell * eur_usd_sell) / btc_usd_buy

  if eur_total > 1
    puts 'fuck yeah!!!'
    puts Time.now
    puts "BTC/EUR = #{btc_eur_sell} EUR/USD = #{eur_usd_sell} BTC/USD = #{btc_usd_buy} profit = #{eur_total}"
  end

  ltc_usd = JSON.parse get('https://btc-e.com/api/2/ltc_usd/ticker')
  ltc_usd_sell = ltc_usd["ticker"]["sell"]

  ltc_rur = JSON.parse get('https://btc-e.com/api/2/ltc_rur/ticker')
  ltc_rur_buy = ltc_rur["ticker"]["buy"]

  ltc_total = (ltc_usd_sell * usd_rur_sell) / ltc_rur_buy

  if ltc_total > 1
    puts 'fuck yeah!!!'
    puts Time.now
    puts "LTC/USD = #{ltc_usd_sell} USD/RUR = #{usd_rur_sell} LTC/RUR = #{ltc_rur_buy} profit = #{ltc_total}"
  end

  sleep 3

end

