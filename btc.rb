#!/usr/bin/env ruby

require 'net/http'
require 'open-uri'
require 'json'

def get(url) 
  uri = URI.parse(url)
  Net::HTTP.start(uri.host, uri.port, {:use_ssl => true}) do |http|
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

total = (btc_usd_sell * usd_rur_sell) / btc_rur_buy

#puts total

if total > 1.04
  puts 'fuck yeah!!!'
  puts "BTC/USD = #{btc_usd_sell} USD/RUR = #{usd_rur} BTC/RUR = #{btc_rur_buy}"
end
