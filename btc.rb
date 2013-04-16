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

btc_usd = JSON.parse get('https://btc-e.com/api/2/btc_usd/ticker')
btc_usd_sell = btc_usd["ticker"]["sell"]

usd_rur = JSON.parse get('https://btc-e.com/api/2/usd_rur/ticker')
usd_rur_sell = usd_rur["ticker"]["sell"]

btc_rur = JSON.parse get('https://btc-e.com/api/2/btc_rur/ticker')
btc_rur_buy = btc_rur["ticker"]["buy"]

btc_total = (btc_usd_sell * usd_rur_sell) / btc_rur_buy

#puts total

if btc_total > 1
  puts 'fuck yeah!!!'
  puts Time.now
  puts "BTC/USD = #{btc_usd_sell} USD/RUR = #{usd_rur} BTC/RUR = #{btc_rur_buy} profit = #{btc_total}"
end
