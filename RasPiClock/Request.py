# -*- encoding: utf-8 -*-

import requests

def crypto(conf, pair):
	reponseCrypto = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=" + conf["CRYPTO"][pair].upper())
	return reponseCrypto
